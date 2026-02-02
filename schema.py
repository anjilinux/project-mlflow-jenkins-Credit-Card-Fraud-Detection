from pydantic import BaseModel, Field, ConfigDict

class Transaction(BaseModel):
    V1: float = Field(...)
    V2: float = Field(...)
    V3: float = Field(...)
    V4: float = Field(...)
    V5: float = Field(...)
    V6: float = Field(...)
    V7: float = Field(...)
    V8: float = Field(...)
    V9: float = Field(...)
    V10: float = Field(...)
    V11: float = Field(...)
    V12: float = Field(...)
    V13: float = Field(...)
    V14: float = Field(...)
    V15: float = Field(...)
    V16: float = Field(...)
    V17: float = Field(...)
    V18: float = Field(...)
    V19: float = Field(...)
    V20: float = Field(...)
    V21: float = Field(...)
    V22: float = Field(...)
    V23: float = Field(...)
    V24: float = Field(...)
    V25: float = Field(...)
    V26: float = Field(...)
    V27: float = Field(...)
    V28: float = Field(...)
    Amount: float = Field(...)

    # Pydantic V2: JSON schema example
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
