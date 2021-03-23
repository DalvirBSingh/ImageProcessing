from myapp.forms import UploadFileForm
from PIL import Image, ImageOps,ImageFilter
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
import random
from myapp.s3upload import upload_file, delete_from_s3

def applyfilter(filename, preset):
    inputfile = settings.ROOT_PATH + 'media/' + filename

    f=filename.split('.')
    outputfilename = f[0] + "-id-" + str(random.randint(1,10000000))+ '-output.jpg'

    outputfile = settings.ROOT_PATH + 'myapp/templates/static/output/' + outputfilename 

    im = Image.open(inputfile)
    if preset=='gray':
        im = ImageOps.grayscale(im)

    if preset=='edge':
        im = ImageOps.grayscale(im)
        im = im.filter(ImageFilter.FIND_EDGES)

    if preset=='poster':
        im = ImageOps.posterize(im,3)

    if preset=='solar':
        im = ImageOps.solarize(im, threshold=80) 

    if preset=='blur':
        im = im.filter(ImageFilter.BLUR)
    
    if preset=='sepia':
        sepia = []
        r, g, b = (239, 224, 185)
        for i in range(255):
            #update
            sepia.extend((r*i//255, g*i//255, b*i//255))
        im = im.convert("L")
        im.putpalette(sepia)
        im = im.convert("RGB")

    im.save(outputfile)
    return (outputfilename, outputfile)

def handle_uploaded_file(f,preset):
    context={}
    uploadfilename='media/' + f.name
    with open(uploadfilename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    outputfilename=applyfilter(f.name, preset)
    upload_file(outputfilename[1], "image-processed-bucket", outputfilename[0])

    return outputfilename[0]

def home(request):
    context={}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            preset=request.POST['preset']
            outputfilename = handle_uploaded_file(request.FILES['myfilefield'],preset)
            return render(request, 'process.html',{'outputfilename': outputfilename}, context)
    else:
        form = UploadFileForm() 
    return render(request, 'index.html',{'form': form}, context)

def process(request):
    return render(request,'process.html', {}, {})

def process_delete(request):
    filename = request.GET.get('file')
    delete_from_s3("image-processed-bucket", filename)
    context={}
    form = UploadFileForm() 
    # Deleted so go back to main page
    return render(request, 'index.html',{'form': form}, context)
    
def process_download(request):
    filename = request.GET.get('file')
    download_from_s3("image-processed-bucket", filename)
    context={}
    form = UploadFileForm() 
    return render(request, 'index.html',{'form': form}, context)