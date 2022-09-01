from typing import Iterable

import httpx
from pydantic import BaseModel, constr
from starlette import status

from utils.request import get_httpx_request_proxies


class _NpaSection(BaseModel):
    code: constr(max_length=64, min_length=1, strip_whitespace=True)
    name: constr(max_length=512, min_length=1, strip_whitespace=True)
    description: str | None = None
    is_agencies_of_state_authorities: bool


async def get_npa_sections_from_source() -> Iterable[_NpaSection]:
    """Получение блоков НПА из источника http://publication.pravo.gov.ru/"""
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp = await client.get("http://publication.pravo.gov.ru/api/PublicBlock/Get")
        assert resp.status_code == status.HTTP_200_OK
        return (
          _NpaSection(
              code=item["Code"],
              name=item["Name"],
              description=item["Description"],
              is_agencies_of_state_authorities=item["IsAgenciesOfStateAuthorities"],
          )
          for item in resp.json()
        )
