import asyncio

from apps.document_types.models import DocumentType
from apps.section.logic.getters import (
    get_npa_sections_from_source,
    get_npa_section_subsection_from_source,
    get_npa_documents_from_source_by_page_number
)
from apps.section.models import NpaSection, NpaSubSection, NpaDocument
from apps.signatory_authority.models import SignatoryAuthority


async def refresh_npa_sections_from_source() -> None:
    for npa_section in await get_npa_sections_from_source():
        await NpaSection.objects.update_or_create(
            code=npa_section.code,
            defaults={
                "name": npa_section.name,
                "description": npa_section.description,
                "is_agencies_of_state_authorities": npa_section.is_agencies_of_state_authorities,
            }
        )


async def refresh_npa_section_subsection_from_source(npa_section: NpaSection) -> None:
    for npa_subsection in await get_npa_section_subsection_from_source(npa_section):
        await NpaSubSection.objects.update_or_create(
            code=npa_subsection.code,
            npa_section=npa_section.pk,
            defaults={
                "name": npa_subsection.name,
                "description": npa_subsection.description,
                "is_agencies_of_state_authorities": npa_subsection.is_agencies_of_state_authorities,
            }
        )


async def refresh_npa_documents_from_source(start_page: int = 1, end_page: int = 3) -> None:
    for npa_document in await get_npa_documents_from_source_by_page_number(start_page=start_page, end_page=end_page):
        document_type, _ = await DocumentType.objects.update_or_create(
            uuid=npa_document.document_type.uuid,
            defaults={"name": npa_document.document_type.name},
        )
        signatory_authority, _ = await SignatoryAuthority.objects.update_or_create(
            uuid=npa_document.signatory_authority.uuid,
            defaults={"name": npa_document.signatory_authority.name}
        )
        await NpaDocument.objects.update_or_create(
            complex_name=npa_document.complex_name,
            defaults={
                "name": npa_document.name,
                "document_date": npa_document.document_date,
                "publish_date_short": npa_document.publish_date_short,
                "eo_number": npa_document.eo_number,
                "has_pdf": npa_document.has_pdf,
                "number": npa_document.number,
                "document_type": getattr(document_type, "pk", None),
                "signatory_authority": getattr(signatory_authority, "pk", None),
            }
        )


async def refresh_npa_sections_subsections_from_source() -> None:
    for npa_section in await NpaSection.objects.all():
        await refresh_npa_section_subsection_from_source(npa_section)
