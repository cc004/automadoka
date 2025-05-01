#type: ignore
from re import T
from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel
from ..constants import APP_SM

class ServerError(BaseModel):
    domain: str
    code: int
    field: str
    reason: str

class ResponseBase(BaseModel):
    status: int = None
    async def update(self, mgr: "datamgr", request): ...

TResponse = TypeVar('TResponse', bound=ResponseBase, covariant=True)

class Response(GenericModel, Generic[TResponse]):
    payload: Optional[TResponse] = None
    url: str = None
    status: int = None
    errors: Optional[List[ServerError]] = None

from pydantic.main import validate_model, object_setattr
from typing import Any

class RequestBase(Generic[TResponse], BaseModel):
    lastHomeAccessTime: str = ''
    sm: str = APP_SM
    @property
    def url(self) -> str:
        raise NotImplementedError()
    
    def __init__(__pydantic_self__, **data: Any) -> None:
        """
        Create a new model by parsing and validating input data from keyword arguments.

        Raises ValidationError if the input data cannot be parsed to form a valid model.
        """
        # Uses something other than `self` the first arg to allow "self" as a settable attribute
        values, fields_set, validation_error = validate_model(__pydantic_self__.__class__, data)
        try:
            object_setattr(__pydantic_self__, '__dict__', values)
        except TypeError as e:
            raise TypeError(
                'Model values must be a dict; you may not have returned a dictionary from a root validator'
            ) from e
        object_setattr(__pydantic_self__, '__fields_set__', fields_set)
        __pydantic_self__._init_private_attributes()

TMstType = TypeVar('TMstType', bound=Any, covariant=True)

class MstResponse(GenericModel, Generic[TMstType], ResponseBase):
    mstList: List[TMstType] = None
    
class MstRequestBase(Generic[TMstType], RequestBase[MstResponse[TMstType]]):
    pass

class Request(Generic[TResponse], BaseModel):
    payload: RequestBase[TResponse]
    uuid: str
    userId: int
    sessionId: Optional[str]
    actionToken: Optional[str]
    ctag: Optional[str]
    actionTime: int
