import asyncio
from datetime import date, datetime
from logging import getLogger
from typing import Iterable
from uuid import UUID

import httpx
from fastapi_utils.files import NamedBytesIO
from fastapi_utils.httpx.logic.getters import get_httpx_request_proxies
from pydantic import BaseModel, constr
from starlette import status

from apps.document_types.logic.getters import _DocumentTypeDto
from apps.section.models import NpaSection
from apps.signatory_authority.logic.getters import _SignatoryAuthorityDto

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


async def get_npa_document_source_url(eo_number: str) -> str | None:
    """получени ссылки на страницу с документа на сайте publication.pravo.gov.ru"""
    url = f"http://publication.pravo.gov.ru/Document/View/{eo_number}"
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp = await client.get(url)
        if resp.status_code != status.HTTP_200_OK:
            logger.exception(resp.text)
            return
        return url


async def get_npa_document_content(eo_number: str) -> NamedBytesIO | None:
    """получени содержимого документа с сайта publication.pravo.gov.ru"""
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp = await client.get(f"http://publication.pravo.gov.ru/File/GetFile/{eo_number}")
        if resp.status_code != status.HTTP_200_OK:
            logger.exception(resp.text)
            return
        return NamedBytesIO(resp.content, name=f"{eo_number}.pdf")


class _NpaDocumentDto(BaseModel):
    uuid: UUID
    eo_number: constr(max_length=16, strip_whitespace=True)
    number: constr(max_length=128, strip_whitespace=True) | None = None
    complex_name: constr(max_length=5000, strip_whitespace=True)
    name: constr(max_length=5000, strip_whitespace=True)
    document_date: date
    has_pdf: bool
    publish_date_short: datetime
    document_type: _DocumentTypeDto
    signatory_authority: _SignatoryAuthorityDto


async def get_npa_documents_from_source_by_page_number(
        start_page: int = 1,
        end_page: int = 5,
) -> Iterable[_NpaDocumentDto] | None:
    """получение списка НПА из источника по номеру страницы"""
    npa_documents = []
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        while True:
            # PubDateType=single&PubDateSingle=15.10.2022 - для конкретной даты
            url = f"http://publication.pravo.gov.ru/api/Document/Get?RangeSize=200&CurrentPageNumber={start_page}"
            resp = await client.get(url)
            if resp.status_code != status.HTTP_200_OK:
                logger.exception(resp.text)
                return
            data = resp.json()
            npa_documents.extend(
                _NpaDocumentDto(
                    complex_name=document["ComplexName"],
                    name=document["Name"],
                    uuid=document["Id"],
                    eo_number=document["EoNumber"],
                    number=document["Number"],
                    document_date=datetime.strptime(document["DocumentDate"], "%Y-%m-%dT%H:%M:%S"),
                    has_pdf=document["HasPdf"],
                    publish_date_short=datetime.strptime(document["PublishDateShort"], "%Y-%m-%dT%H:%M:%S"),
                    document_type=_DocumentTypeDto(uuid=document['DocumentTypeId'], name=document["DocumentTypeName"]),
                    signatory_authority=_SignatoryAuthorityDto(
                        uuid=document["SignatoryAuthorityId"],
                        name=document["SignatoryAuthorityName"],
                    )
                )
                for document in data["Documents"]
            )
            if start_page > end_page:
                break
            print(f"Обработано {start_page}/{data['MaxPageNumber']} [{end_page}]")
            start_page += 1
            await asyncio.sleep(15)

    return npa_documents
