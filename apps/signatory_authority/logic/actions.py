from apps.signatory_authority.logic.getters import get_signatory_authorities_from_source
from apps.signatory_authority.models import SignatoryAuthority


async def refresh_signatory_authority() -> None:
    for signatory_authority in await get_signatory_authorities_from_source():
        await SignatoryAuthority.objects.update_or_create(
            uuid=signatory_authority.uuid,
            defaults={"name": signatory_authority.name},
        )
