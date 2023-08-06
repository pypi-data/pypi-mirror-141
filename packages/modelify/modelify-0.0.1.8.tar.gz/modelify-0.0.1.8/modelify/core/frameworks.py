from enum import Enum


class Frameworks(str,Enum):
    SKLEARN = "SKLEARN"
    KERAS = "KERAS"
    H2O = "H2O"
    LIGHTGBM = "LIGHTGBM"
    XGBOOST = "XGBOOST"
    CATBOOST = "CATBOOST"