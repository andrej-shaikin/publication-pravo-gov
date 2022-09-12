from apps.section.logic.getters import get_npa_sections_from_source, get_npa_section_subsection_from_source
from apps.section.models import NpaSection, NpaSubSection


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


async def refresh_npa_sections_subsections_from_source() -> None:
    for npa_section in await NpaSection.objects.all():
        await refresh_npa_section_subsection_from_source(npa_section)
