from logging import getLogger
from typing import Iterable
from uuid import UUID

import httpx
from fastapi_utils.httpx.logic.getters import get_httpx_request_proxies
from pydantic import BaseModel, constr
from starlette import status

logger = getLogger(__name__)


class _SignatoryAuthorityDto(BaseModel):
    uuid: UUID
    name: constr(max_length=512, min_length=1, strip_whitespace=True)


async def get_signatory_authorities_from_source() -> Iterable[_SignatoryAuthorityDto] | None:
    """Получение подписывающих органов из источника http://publication.pravo.gov.ru/"""
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp = await client.get("http://publication.pravo.gov.ru/api/SignatoryAuthority/Get")
        if resp.status_code != status.HTTP_200_OK:
            logger.exception(resp.text)
            return
        return (_SignatoryAuthorityDto(uuid=item["Id"], name=item["Name"]) for item in resp.json())
