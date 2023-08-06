from enum import Enum

class FileTypes(str, Enum):
    MODEL = "MODEL",
    CONFIG = "CONFIG",
    PREPROCESS = "PREPROCESS",
    POSTPROCESS = "POSTPROCESS"
    REQUIREMENTS = "REQUIREMENTS"


class SeriliazeType(str,Enum):
    preprocess = "preprocess"
    postprocess = "postprocess"

    @staticmethod
    def has_value(item):
        return item in [v.value for v in SeriliazeType.__members__.values()]