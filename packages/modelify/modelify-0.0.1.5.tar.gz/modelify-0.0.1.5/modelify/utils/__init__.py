
import socket
import os
import sys
from contextlib import closing
import yaml
import os
from modelify.utils.constants import APP_FOLDER, ModelifyFile
from modelify.utils.types import SeriliazeType
import cloudpickle
import uuid

def message(text):
    print(text,  end='\n', flush=True)

def get_env(variable_name):
    return os.environ.get(variable_name)

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def create_folder():
    os.makedirs(APP_FOLDER, exist_ok=True)


def save_requirements_file( packages):
    requirements_file = os.path.join(APP_FOLDER, "requirements.txt")
    with open(requirements_file, 'w') as f:
        f.write('\n'.join(packages))

def save_config(config_metadata):
    model_file = os.path.join(APP_FOLDER, ModelifyFile.CONFIG.file_name)
    with open(model_file, 'w') as outfile:
        yaml.dump(config_metadata, outfile)

def save_onnx_model( onnx_model, built_in=False):

    file_name =  "model.onnx"
    output_file = os.path.join(APP_FOLDER, file_name)

    if built_in:
        onnx_model.save_model(output_file, format="onnx")
    else:
        with open(output_file, "wb") as f:
            f.write(onnx_model.SerializeToString())

    return output_file 


def serialize(function_name, seriliaze_type):
    """_summary_

    Args:
        function_name (function): the function you implemented
        seriliaze_type (SeriliazeType): postprocess or preprocess

    Raises:
        Exception: _description_
    """
    app_folder = get_app_folder() 
    if not SeriliazeType.has_value(seriliaze_type):
        raise Exception("Avaiable types: 'preprocess' and 'postprocess'  ")
    pickle_name = f"{seriliaze_type}.pkl"
    object_path = os.path.join(APP_FOLDER , pickle_name)
    with open(object_path, mode='wb') as file:
        cloudpickle.dump(function_name, file)


def create_config(inputs, preprocess, postprocess, requirements: list, **kwargs):
    config_metadata = dict()
    for key,value in kwargs.items():
        config_metadata[key] = value
    # export configs
    input_list = inputs.to_list()
    config_metadata["inputs"] = input_list
    config_metadata['input_type'] =  inputs.type

    if preprocess is not None:
        config_metadata["preprocess"] = True
    else:
        config_metadata["preprocess"] = False
    if postprocess is not None:
        config_metadata["postprocess"] = True
    else:
        config_metadata["postprocess"] = False

    if len(requirements) > 0 :
        config_metadata["requirements"] = requirements

    return config_metadata

def get_base_upload_types():
    return {"MODEL": True, "CONFIG": True, "PREPROCESS": False, "POSTPROCESS": False, "REQUIREMENTS": False }
