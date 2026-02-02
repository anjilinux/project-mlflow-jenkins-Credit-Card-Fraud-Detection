from pydantic import BaseModel, Field
from pydantic import ConfigDict

class Transaction(BaseModel):
    V1: float = Field(..., example=0.1)
    V2: float = Field(..., example=-1.2)
    ...
    V28: float = Field(..., example=-0.1)
    Amount: float = Field(..., example=123.45)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "V1": 0.1, "V2": -1.2, "V3": 0.3, "V4": 0.4,
                "V5": -0.5, "V6": 1.1, "V7": 0.7, "V8": -0.8,
                "V9": 0.9, "V10": -1.0, "V11": 0.2, "V12": -0.4,
                "V13": 0.6, "V14": -0.9, "V15": 0.8, "V16": -0.7,
                "V17": 0.5, "V18": -0.6, "V19": 0.1, "V20": -0.2,
                "V21": 0.3, "V22": -0.4, "V23": 0.5, "V24": -0.6,
                "V25": 0.7, "V26": -0.8, "V27": 0.9, "V28": -0.1,
                "Amount": 123.45
            }
        }
    )
