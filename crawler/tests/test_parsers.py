from lxml import etree
import pytest
import parsers as tm
from test_parsers_fixtures import *

def describe_parsers_module():
    def describe__extract_text():
        def it_should_return_text_of_page(page_content, html_text):
            assert ''.join(tm._extract_text(page_content).split()) == ''.join(html_text.split())
    
    def describe__count_words():
        def it_should_return_dict_with_counts(words_list, words_dict):
            assert tm._count_words(words_list, words_dict) == {'0': 1, '1': 3, '2': 2}

    def describe__split_text():
        def it_sould_return_list_of_words(html_text):
            min_len = 3
            assert len(tm._split_text(html_text, min_len)) == 73
    
    def describe_parse_html():
        def it_should_return_dict(page_content, words_dict):
            """
                page_content - контент страницы
                words_dict - {"person_id":[words_list]}
                возвращает словарь {"person_id": "rank"}
            """
            assert tm.parse_html(page_content, words_dict) == {'0': 1, '1': 3, '2': 2}