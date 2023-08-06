
import shutil
import uuid
import os
import uuid
import requests
import json
from modelify.utils.constants import MODELIFY_PRESIGNED_URL, MODELIFY_DEPLOY_URL
from modelify.utils.credential import Credential
from modelify.utils import message
import yaml
from enum import Enum
from modelify.utils.constants import APP_FOLDER
from modelify.utils.types import FileTypes

""" 
storage
  - $USER_ID
        - $APP_ID
            - versions
                - 1
                    - config.yaml
                    - model.onnx
                    - preprocess.pkl
                    - postprocess.pkl
                    - requirements.txt
                    - custom_ui.html
                - 2
                    - config.yaml
                ....
"""

class ModelifyClient:
    def __init__(self):
        self.credential = Credential()

 
    def upload_pipeline(self, upload_types: dict, app_uid, configs):
        # filter upload types
        filetypes = list(map(lambda x: x[0], filter(lambda item: item[1]==True, upload_types.items())))
        upload_urls = self.get_presigned_url(app_uid, filetypes)
        print(upload_urls)
        for item in upload_urls:
            self.upload_model_storage(item["url"], item["type"])
        self.register_model(app_uid, configs)

    def get_presigned_url(self ,app_uid, filetypes:list):
        data = {'app_uid': app_uid, 'filetypes': filetypes}
        headers = {"api-token": f"{self.credential.api_key}", "Content-Type": "application/json"}
        req = requests.post(MODELIFY_PRESIGNED_URL, json=data, headers = headers)

        if req.status_code == 200:
            return req.json()["urls"]
        raise Exception("Upload url could not generated")

    def upload_model_storage(self,url, file_type):
        if file_type == FileTypes.MODEL:
            blob_name = "model.onnx"
            content_type = "application/octet-stream"
        elif file_type == FileTypes.PREPROCESS:
            blob_name = "preprocess.pkl"
            content_type = "application/octet-stream"
        elif file_type == FileTypes.POSTPROCESS:
            blob_name = "postprocess.pkl"
            content_type = "application/octet-stream"
        elif file_type == FileTypes.CONFIG:
            blob_name = "config.yaml"
            content_type = "text/yaml"
        elif file_type == FileTypes.REQUIREMENTS:
            blob_name = "requirements.txt"
            content_type = "text/plain"
        
        file_path = os.path.join(APP_FOLDER, blob_name)
        req = requests.put(url, open(file_path, 'rb') , headers= {'Content-Type': content_type})
        
        if req.status_code != 200:
            raise Exception("There is something wrong in model upload stage")

        message("Model uploaded successfully")


    def register_model(self, app_uid, configs):
        message("Model is registering to your account")
        data = {'app_uid': app_uid,  'model_metadata': configs}
        headers = {"api-token": f"{self.credential.api_key}", "Content-Type": "application/json"}
        req = requests.post(MODELIFY_DEPLOY_URL, json=data, headers = headers)
        if req.status_code == 201:
            print("Model has been sent.")
        else:
            print(req.text)
            response_dict = json.loads(req.text)

            for i in response_dict:
                print("key: ", i, "val: ", response_dict[i])
            print("Something went wrong while model sending.")

