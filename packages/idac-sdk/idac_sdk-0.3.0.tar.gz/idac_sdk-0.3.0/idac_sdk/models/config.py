from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Extra


class Defaults(BaseModel, extra=Extra.allow):
    idac_fqdn: str
    idac_proto: str
    auth_type: str
    auth: Optional[str]
    api_version: str


class iDACConfig(BaseModel, extra=Extra.allow):
    defaults: Defaults
