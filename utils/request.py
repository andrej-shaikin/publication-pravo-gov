from conf import settings


def get_httpx_request_proxies() -> dict[str, str]:
    """Получение настроек прокси для отправки запроса"""
    proxies = {}
    if settings.HTTP_PROXY:
        proxies["http://"] = settings.HTTP_PROXY
    if settings.HTTPS_PROXY:
        proxies["https://"] = settings.HTTPS_PROXY
    return proxies
