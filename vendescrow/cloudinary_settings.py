import cloudinary.api

cloudinary.config(cloud_name="",api_key="",api_secret="")
cloudinary_url = "https://api.cloudinary.com/v1_1/{unsigned_upload_name}/upload".format(unsigned_upload_name="")
cloudinary_upload_preset = ""
