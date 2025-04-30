from .modelbase import MstRequestBase
from pydantic import BaseModel

class MasterDataRecord(BaseModel):
    language: str
    name: str
    size: int
    revision: str

class GetResourceMasterDataMstListRequest(MstRequestBase[MasterDataRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_resource_master_data_mst_list"