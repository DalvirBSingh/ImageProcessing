import boto3
import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL':'public-read'})
    except ClientError as e:
        logging.error(e)
        return False
    return True
def delete_from_s3(bucketname,filename):
    print("Bucket name:: ", bucketname)
    print("File name:: ", filename)

    s3_client = boto3.client('s3')
    try:
        response = s3_client.delete_object(Bucket=bucketname, Key=filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# def percent_cb(complete, total):
#     print ('.')

# def upload_to_s3_bucket_path(bucketname, path, filename):
# 	mybucket = conn.get_bucket(bucketname)
# 	fullkeyname=os.path.join(path,filename)
# 	key = mybucket.new_key(fullkeyname)
# 	key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
# 	#key.make_public(recursive=False)

# def upload_to_s3_bucket_root(bucketname, filename):
# 	mybucket = conn.get_bucket(bucketname)
# 	key = mybucket.new_key(filename)
# 	key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)

# def getuserfiles(bucketname,username):
# 	mybucket = conn.get_bucket(bucketname)
# 	keys = mybucket.list(username)
# 	totalsize=0.0
# 	userfiles = {}
# 	for key in keys:
# 		value=[]
# 		#value.append(key.name)
# 		filename = key.name
# 		filename=filename.replace(username+'/media/','')
# 		value.append(key.last_modified)
# 		keysize = float(key.size)/1000.0
# 		value.append(str(keysize))
# 		userfiles[filename]=value
# 		totalsize = totalsize + float(key.size)
# 	totalsize = totalsize/1000000.0
# 	return userfiles,totalsize


