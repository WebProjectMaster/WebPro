#!/usr/bin/python3
from urllib.parse import urlparse, ParseResult
from lxml import etree
import io
import re
import logging
import datetime
from log import log_with
import database as db


SM_TYPE_XML = 0
SM_TYPE_HTML = 1
SM_TYPE_TXT = 2
SM_TYPE_REC = 3 # рекурсивный sitemap содержит ссылки на другие sitemap


def _esc_amp(text):
    """ text строка, возвращает строку с замененными & """ 
    # замена & на &amp;
    return re.sub(r'&(?!amp;)', r'&amp;', text, re.MULTILINE)


def _get_nsless_xml(xml):
    """ xml - bytes[], возращает root ETreeElement """
    # убираем namespaces из xml
    it = etree.iterparse(xml) # it = etree.iterparse(xml, recover=True) если хотим чтобы не падало на неправильных xml
    for _, el in it:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        for at in el.attrib.keys(): # strip namespaces of attributes too
            if '}' in at:
                newat = at.split('}', 1)[1]
                el.attrib[newat] = el.attrib[at]
                del el.attrib[at]
    return it.root


def get_file_type(sitemap):
    xml_pattern = "<urlset"
    html_pattern = "<!DOCTYPE"
    rec_pattern = "<sitemapindex"
    
    if sitemap.find(xml_pattern) >= 0:
        return SM_TYPE_XML
    elif sitemap.find(html_pattern) >= 0:
        return SM_TYPE_HTML
    elif sitemap.find(rec_pattern) >= 0:
        return SM_TYPE_REC
    else:
        return SM_TYPE_TXT


def _select_items(xml_elem, xpath):
    """ xml_elem ETreeElement, xpath - путь поиска, возвращает список урлов в элементе """
    items = [x.text.strip() for x in xml_elem.xpath(xpath)]
    return items


def _select_attrs(xml_elem, xpath):
    """ xml_elem ETreeElement, xpath - путь поиска с выбором атрибутов, возвращает список урлов """
    attrs = [x.strip() for x in xml_elem.xpath(xpath)]
    return attrs


def _parse_txt(content):
    """
        content - содержимое sitemap в текстовом виде
    """
    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(pattern, content, re.MULTILINE)


def _parse_html(content):
    """
        content - содержимое sitemap в html, для парсинга страниц на ссылки
    """
    parser = etree.HTMLParser()
    html_root = etree.parse(io.BytesIO(content.encode()), parser).getroot()
    xpath = './/a/@href'
    return _select_attrs(html_root, xpath)


def _parse_xml(content, xpath):
    """
        content - содержимое sitemap в текстовом xml
        xpath - путь поиска для sitemap ('url/loc'), для рекурсивного ('sitemap/loc')
    """
    xml = _esc_amp(content)
    xml_root = _get_nsless_xml(io.BytesIO(xml.encode()))
    return _select_items(xml_root, xpath)


def _normalize_url(url, base_url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    bs_url = urlparse(base_url)
    if scheme == '':
        scheme = bs_url.scheme
    if netloc == '':
        netloc = bs_url.netloc
    return ParseResult(scheme, netloc, path, params, query, fragment).geturl()


def _get_urls(content, base_url, sitemap_type):
    urls_list = []
    try:
        if sitemap_type == SM_TYPE_XML:
            urls_list = _parse_xml(content, 'url/loc')
        elif sitemap_type == SM_TYPE_HTML:
            urls_list = [_normalize_url(url, base_url) for url in _parse_html(content)]
        elif sitemap_type == SM_TYPE_TXT:
            urls_list = _parse_txt(content)
        elif sitemap_type == SM_TYPE_REC:
            urls_list = _parse_xml(content, 'sitemap/loc')
    except Exception as ex:
        logging.error("sitemap.get_urls: site %s, error %s", base_url, ex)
    return urls_list


def _filter_robots(urls, robots):
    # TODO: реализовать фильтр по robots.txt
    if robots is None:
        return urls
    return urls


def _filter_domain(urls, base_url):
    return [url for url in urls if url.startswith(base_url)]


def add_urls(urls, page, page_type):
    page_id, page_url, site_id, base_url = page
    new_pages_data = [{
        'site_id': site_id,
        'url': url,
        'found_date_time': datetime.datetime.now(),
        'last_scan_date': None
        } for url in urls]
    urls_count = db.add_urls(new_pages_data)
    if page_type != SM_TYPE_HTML:
        db.update_last_scan_date(page_id)
    return urls_count

#@log_with
def scan_urls(content, page, robots):
    """
        content - содержимое сайтмэпа или html str,
        page - tuple с инфой о странице page_id, url, site_id, base_url
        robots - класс с парсером robots.txt
        возвращает tuple c типом контента и списком ссылок
    """
    page_id, page_url, site_id, base_url = page
    page_type = get_file_type(content)
    urls = _get_urls(content, base_url, page_type)

    # удаляем пустые
    urls = [url for url in urls if url]
    urls = _filter_domain(urls, base_url)
    urls = _filter_robots(urls, robots)
    urls_count = add_urls(urls, page, page_type)
    return (page_type, urls_count)
