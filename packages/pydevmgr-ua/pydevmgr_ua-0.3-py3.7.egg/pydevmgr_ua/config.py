from pydantic import BaseModel, AnyUrl
from typing import Optional, Dict, Union

class UAConfig(BaseModel):
    # default namespace 
    namespace: int = 4
    # this is a global mapping allowing to change the opc.tcp address on the fly 
    # usefull when switching from real PLC to simulated one without having to 
    # edit the config files. The key should be the full address to replce (including port)
    # e.g. host_mapping = {"opc.tcp://134.171.59.99:4840": "opc.tcp://192.168.1.11:4840"}
    host_mapping: Dict[Union[str,AnyUrl], AnyUrl] = {}
    default_address: Optional[AnyUrl] = "opc.tcp://localhost:4840"
    
    class Config:
        validate_assignment = True
    
uaconfig = UAConfig()    