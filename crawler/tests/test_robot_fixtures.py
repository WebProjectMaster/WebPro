import pytest


@pytest.fixture
def list_ya_sitemaps():
    return [
        'https://yandex.ru/pogoda/sitemap_index.xml',
        'https://yandex.ru/support/sitemap.xml',
        'https://yandex.ru/blog/sitemap.xml'
        ]
