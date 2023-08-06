from onnxmltools import convert
import os
from modelify.utils.constants import MODELIFY_TOKEN_VALIDATION_URL
import requests
import json
from modelify.utils.credential import Credential
from modelify.utils import message
from modelify.schema import InputList
from pyngrok import ngrok
import nest_asyncio
import uvicorn

from modelify.core.frameworks import Frameworks
from modelify.core.client import ModelifyClient
import modelify.helpers  as helpers
import modelify.version as __version__
from modelify.app import create_fastapi


from modelify.utils import find_free_port , create_folder, get_base_upload_types, save_onnx_model, serialize, save_config, save_requirements_file, create_config


client = ModelifyClient()



def connect(api_key):
    """ Function to connect with Modelify Cloud
    Args:
        api_key (str): API Token Key (provided by Modelify Cloud)
    """
    client.credential.api_key = api_key
    headers = {"api-token": f"{client.credential.api_key}", "Content-Type": "application/json"}
    req = requests.get(MODELIFY_TOKEN_VALIDATION_URL, headers =headers)
    if req.status_code == 200:
        print("Connection established. ")
    else:
        print("Token is not valid.")

def export_model( framework:Frameworks, model, inputs:InputList, target_opset):
    create_folder() 
    initial_type = inputs.convert_onnx()
    built_in = False
    if framework == Frameworks.SKLEARN:
        model = convert.convert_sklearn(model, initial_types=initial_type, target_opset=target_opset)
    elif framework == Frameworks.LIGHTGBM:
        model = convert.convert_lightgbm(model, initial_types=initial_type, target_opset=target_opset)
    elif framework == Frameworks.H2O:
        model = convert.convert_h2o(model, initial_types=initial_type, target_opset=target_opset)
    elif framework == Frameworks.KERAS:
        model = convert.convert_keras(model)
    elif framework == Frameworks.XGBOOST:
        model = convert.convert_xgboost(model, initial_types=initial_type, target_opset=target_opset)
    elif framework == Frameworks.CATBOOST:
        built_in = True
        
    save_onnx_model(model, built_in=built_in)

 


def deploy( framework: Frameworks, app_uid, model, inputs:InputList,  title:str="Modelify Application", preprocess_function=None, postprocess_function=None, requirements:list=[],target_opset=9):
    message("Model is converting...")
    export_model(framework, model, inputs=inputs, target_opset=target_opset)
    # zip_folder()
       # seriliaze functions
    upload_types = get_base_upload_types()
    if preprocess_function:
        serialize(preprocess_function, 'preprocess')
        upload_types["PREPROCESS"] = True
  
    if postprocess_function:
        serialize(postprocess_function, 'postprocess')
        upload_types["POSTPROCESS"] = True

    if len(requirements) > 0 :
        save_requirements_file(requirements)
        upload_types["REQUIREMENTS"] = True

    configs = create_config(inputs, preprocess_function, postprocess_function, requirements, title=title)
    save_config(configs)
    message("Model converted successfully")
    client.upload_pipeline(upload_types=upload_types, app_uid=app_uid, configs=configs)
    message("Done")
        


def run(framework: Frameworks, model,  inputs:InputList, title:str="Modelify Application", preprocess_function=None, postprocess_function=None, requirements=[],target_opset=9):
    """ This function creates an application on your local environment
    Args:
        name (str): _description_. Defaults 'Modelify Application'
        model (_type_): _description_
        inputs (InputList): _description_
        target_opset (int, optional): _description_. Defaults to 9.
    """
    message("Model is converting...")    
    export_model(framework=framework, model=model, inputs=inputs, target_opset=target_opset)   
    

    # seriliaze functions
    if preprocess_function:
        serialize(preprocess_function, 'preprocess')
  
    if postprocess_function:
        serialize(postprocess_function, 'postprocess')

    if len(requirements) > 0 :
        save_requirements_file(requirements)

    configs = create_config(inputs, preprocess_function, postprocess_function, requirements, title=title)
    save_config(configs)
    message("Modelify API is creating...") 
    run_server()  


def run_server(port:int=None, tunnel = True, host="0.0.0.0", proxy_headers=True):
    app = create_fastapi()
    if not port:
        port = find_free_port()
    if tunnel:
        ngrok_tunnel = ngrok.connect(port)
        nest_asyncio.apply()
    uvicorn.run(app, port=port, host=host, proxy_headers=proxy_headers)


__all__ = [
    "connect",
    "deploy",
    "run",
    "run_server",
    "Frameworks",
    "__version__"
]







