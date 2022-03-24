#users/picture_handler.py 
# upload pictures 

from fileinput import filename
import os 
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    # uploading a mypicture.jpg - here we will split on the . and grab the last str 
    # this is important to check the file types later 
    ext_type = filename.split('.')[-1]
    # we are gonna convert their upload to their unique username.jpg file basically 
    storage_filename = str(username)+'.'+ext_type
    #grab the root path and look for static folder file 
    filepath = os.path.join(current_app.root_path, 'statis/profile_pics', storage_filename)
    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename