from pydantic import BaseModel

class Config(BaseModel):
    x_rpc_device_fp: str|int = "38d80bb76ee47"