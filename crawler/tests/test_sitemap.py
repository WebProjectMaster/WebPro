import os
import urllib.request
from lxml import etree
import pytest
import sitemap as tm
from test_sitemap_fixtures import *

def describe_sitemap_module():
    def describe__esc_apm():
        def it_replace_apm():
            test_str = '&test and & but &amp; &&'
            assert tm._esc_amp(test_str) == '&amp;test and &amp; but &amp; &amp;&amp;'

    def describe__select_items():
        def it_return_list_of_urls(xml_sitemap_clean, urls_list):
            xml_tree = etree.fromstring(xml_sitemap_clean)
            xpath = 'url/loc'
            assert tm._select_items(xml_tree, xpath) == urls_list

    def describe__parse_xml():
        def it_return_list_of_urls(xml_sitemap, urls_list):
            assert tm._parse_xml(xml_sitemap,  'url/loc') == urls_list

    def describe__parse_txt():
        def it_return_list_of_urls(txt_sitemap, urls_list):
            assert tm._parse_txt(txt_sitemap) == urls_list

    def describe__parse_html():
        def it_return_list_of_urls(html_sitemap, html_urls_list):
            assert tm._parse_html(html_sitemap) == html_urls_list

    def describe__get_sitemap_type():
        def it_return_type_of_sitemap_xml(xml_sitemap):
            assert tm.get_file_type(xml_sitemap) == tm.SM_TYPE_XML

        def it_return_type_of_sitemap_html(html_sitemap):
            assert tm.get_file_type(html_sitemap) == tm.SM_TYPE_HTML

        def it_return_type_of_sitemap_txt(txt_sitemap):
            assert tm.get_file_type(txt_sitemap) == tm.SM_TYPE_TXT

    def describe_get_urls():
        def it_return_tuple_of_urls_xml(xml_sitemap, site_url, urls_list):
            assert tm._get_urls(xml_sitemap, site_url, tm.get_file_type(xml_sitemap)) == (urls_list)

        def it_return_tuple_of_urls_html(html_sitemap, site_url, urls_list):
            assert tm._get_urls(html_sitemap, site_url, tm.get_file_type(html_sitemap)) == (urls_list)

        def it_return_tuple_of_urls_txt(txt_sitemap, site_url, urls_list):
            assert tm._get_urls(txt_sitemap, site_url, tm.get_file_type(txt_sitemap)) == (urls_list)

        def it_return_tuple_of_urls_rec(rec_sitemap, site_url, rec_list):
            assert tm._get_urls(rec_sitemap, site_url, tm.get_file_type(rec_sitemap)) == (rec_list)

        def it_logging_warning_if_broken_file(xml_sitemap_bad, site_url, caplog):
            res = tm._get_urls(xml_sitemap_bad, site_url, tm.get_file_type(xml_sitemap_bad))
            print('caplog.text()', caplog.text())
            assert 'sitemap.get_urls' in caplog.text()
            assert res == ([])