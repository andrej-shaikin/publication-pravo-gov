from logging import getLogger
from typing import Iterable

import httpx
from fastapi_utils.httpx.logic.getters import get_httpx_request_proxies
from pydantic import BaseModel, constr
from starlette import status

from apps.section.models import NpaSection

logger = getLogger(__name__)


class _NpaSection(BaseModel):
    code: constr(max_length=64, min_length=1, strip_whitespace=True)
    name: constr(max_length=512, min_length=1, strip_whitespace=True)
    description: str | None = None
    is_agencies_of_state_authorities: bool


class _NpaSubSection(BaseModel):
    code: constr(max_length=64, min_length=1, strip_whitespace=True)
    name: constr(max_length=512, min_length=1, strip_whitespace=True)
    description: str | None = None
    is_agencies_of_state_authorities: bool
    npa_section: _NpaSection


async def get_npa_sections_from_source() -> Iterable[_NpaSection] | None:
    """Получение блоков НПА из источника http://publication.pravo.gov.ru/"""
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp = await client.get("http://publication.pravo.gov.ru/api/PublicBlock/Get")
        if resp.status_code != status.HTTP_200_OK:
            logger.exception(resp.text)
            return
        return (
            _NpaSection(
                code=item["Code"],
                name=item["Name"],
                description=item["Description"],
                is_agencies_of_state_authorities=item["IsAgenciesOfStateAuthorities"],
            )
            for item in resp.json()
        )


async def get_npa_section_subsection_from_source(npa_section: NpaSection) -> Iterable[_NpaSubSection] | None:
    """Получение подблоков НПА из источника http://publication.pravo.gov.ru/"""
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp = await client.get(f"http://publication.pravo.gov.ru/api/SubBlock/Get?code={npa_section.code}")
        if resp.status_code != status.HTTP_200_OK:
            logger.exception(resp.text)
            return
        return (
            _NpaSubSection(
                code=item["Code"],
                name=item["Name"],
                description=item["Description"],
                is_agencies_of_state_authorities=item["IsAgenciesOfStateAuthorities"],
                npa_section=_NpaSection(
                    code=npa_section.code,
                    name=npa_section.name,
                    description=npa_section.description,
                    is_agencies_of_state_authorities=npa_section.is_agencies_of_state_authorities,
                )
            )
            for item in resp.json()
        )
