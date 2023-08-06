import onnx
import onnxruntime as rt
import os
import cloudpickle
from modelify.utils.constants import ModelifyFile


class Model:
    def __init__(self, modelify_path , preprocess, postprocess):
        self.modelify_path = modelify_path
        self.model_path = os.path.join(modelify_path, ModelifyFile.MODEL.file_name)
        self.preprocess_path = os.path.join(modelify_path, ModelifyFile.PREPROCESS.file_name)
        self.postprocess_path = os.path.join(modelify_path, ModelifyFile.POSTPROCESS.file_name)
        self.model = rt.InferenceSession(self.model_path)
        self.preprocess = preprocess
        self.postprocess = postprocess
        self.preprocess_function = None
        self.postprocess_function = None
        self.initialize()

    def initialize(self):
        files = os.listdir(self.modelify_path)
        if self.preprocess:
            if ModelifyFile.PREPROCESS.file_name not in files:
                raise Exception("Preprocess object does tot exists")
            with open(self.preprocess_path, mode='rb') as file:
                self.preprocess_function = cloudpickle.load(file)

        if self.postprocess:
            if ModelifyFile.POSTPROCESS.file_name not in files:
                raise Exception("Postprocess object does tot exists")
            with open(self.postprocess_path, mode='rb') as file:
                self.postprocess_function = cloudpickle.load(file)


    def predict(self, inputs):
     
        input_name = self.model.get_inputs()[0].name
        label_name = self.model.get_outputs()[0].name
        pred_onx = self.model.run(None, {input_name: inputs})[0]
        output = pred_onx.tolist()
        return output
        
        
    def run(self, inputs):
        if self.preprocess:
            inputs = self.preprocess_function(inputs)
        output = self.predict(inputs)
        if self.postprocess:
            output = self.postprocess_function(output)
        return output
        
        