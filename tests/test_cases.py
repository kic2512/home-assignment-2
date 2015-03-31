# coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from page_object import AuthPage, CreateTopicPage, TopicPage, down_keys

__author__ = 'kic'

import os
from unittest import TestCase

from selenium.webdriver import DesiredCapabilities, Remote
from time import sleep


class CreateMessage(TestCase):
    def is_comment_available(self, topic_page):
        try:
            topic_page.add_comment()
        except NoSuchElementException:
            return False
        return True

    def get_effect_func(self, create_page, effect):
        effects = {
            'bold': create_page.set_bold(),
        }
        if effect in effects:
            effects[effect]

    def open_and_set_text_to_topic(self, fields, effect_for_short=None, effect_for_main=None):
        create_page = CreateTopicPage(self.driver)
        create_page.open()

        create_page.blog_select_open()
        create_page.blog_select_set_option(fields['blog'])
        create_page.set_title(fields['title'])

        create_page.activate_short_text()
        if effect_for_short:
            self.get_effect_func(create_page, effect_for_short)
        down_keys(create_page.driver, fields['short_text'])

        create_page.activate_main_text()
        if effect_for_main:
            self.get_effect_func(create_page, effect_for_main)
        down_keys(create_page.driver, fields['main_text'])
        return create_page

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        user_email = 'ftest11@tech-mail.ru'
        password = os.environ.get('TTHA2PASSWORD')

        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_page.open_auth_form()
        auth_page.set_login(user_email)
        auth_page.set_password(password)
        auth_page.submit()
        auth_page.get_username()

    def tearDown(self):
        self.driver.quit()

    def test_topic_create_right(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание простого топика',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }

        create_page = self.open_and_set_text_to_topic(fields)
        create_page.submit()  # Redirect

        topic_page = TopicPage(self.driver)
        topic_title = topic_page.get_title()
        topic_text = topic_page.get_text()
        self.assertEqual(fields['title'], topic_title)
        self.assertEqual(fields['main_text'], topic_text)

        topic_page.delete()
        topic_title = topic_page.get_title()
        topic_text = topic_page.get_text()
        self.assertNotEqual(fields['title'], topic_title)
        self.assertNotEqual(fields['short_text'], topic_text)

    # def test_create_topic_with_quiz(self):
    #     fields = {
    #         'blog': 'Флудилка',
    #         'title': u'Создание топика c опросом',
    #         'short_text': u'Короткий текст',
    #         'main_text': u'Текст'
    #     }
    #     quiz_title = 'QuizTitle'
    #     quiz_first = 'first'
    #     quiz_second = 'second'
    #
    #     create_page = self.open_and_set_text_to_topic(fields)
    #
    #     create_page.add_quiz()
    #     create_page.set_quiz_title(quiz_title)
    #     create_page.set_quiz_var0(quiz_first)
    #     create_page.set_quiz_var1(quiz_second)
    #     create_page.submit()
    #
    #     topic_page = TopicPage(self.driver)
    #
    #     first_quiz_answer = topic_page.get_first_quiz_var()
    #     second_quiz_answer = topic_page.get_second_quiz_var()
    #
    #     self.assertEqual(quiz_first, first_quiz_answer)
    #     self.assertEqual(quiz_second, second_quiz_answer)
    #
    #     topic_page.delete()

    # def test_create_topic_add_comment(self):
    #     fields = {
    #         'blog': 'Флудилка',
    #         'title': u'Создание топика c комментарием',
    #         'short_text': u'Короткий текст',
    #         'main_text': u'Текст'
    #     }
    #
    #     comment_text = u"Мой комментарий"
    #
    #     create_page = self.open_and_set_text_to_topic(fields)
    #     create_page.submit()
    #
    #     topic_page = TopicPage(self.driver)
    #     topic_page.add_comment()
    #     topic_page.comment_activate()
    #     down_keys(self.driver, comment_text)
    #     topic_page.comment_send()
    #
    #     real_comment = topic_page.get_comment()
    #     self.assertEqual(comment_text, real_comment)
    #     topic_page.delete()
    #
    # def test_create_topic_block_comments(self):
    #     fields = {
    #         'blog': 'Флудилка',
    #         'title': u'Создание топика c опросом',
    #         'short_text': u'Короткий текст',
    #         'main_text': u'Текст'
    #     }
    #
    #     create_page = self.open_and_set_text_to_topic(fields)
    #     create_page.set_block_for_comment()
    #     create_page.submit()
    #
    #     topic_page = TopicPage(self.driver)
    #     check = self.is_comment_available(topic_page)
    #     self.assertFalse(check)
    #     topic_page.delete()
    #
    # def test_create_topic_without_title(self):
    #     fields = {
    #         'blog': 'Флудилка',
    #         'title': u'',
    #         'short_text': u'Короткий текст',
    #         'main_text': u'Текст'
    #     }
    #
    #     create_page = self.open_and_set_text_to_topic(fields)
    #     create_page.submit()
    #
    #     error = create_page.get_error_message()  # ERROR TEXT CAN CHANGE, BUT ERROR TEXT MUST EXIST
    #     self.assertTrue(error)
    #
    # def test_create_topic_without_main_text(self):
    #     fields = {
    #         'blog': 'Флудилка',
    #         'title': u'Создание топика с ошибкой',
    #         'short_text': u'Короткий текст',
    #         'main_text': u''
    #     }
    #
    #     create_page = self.open_and_set_text_to_topic(fields)
    #     create_page.submit()
    #
    #     error = create_page.get_error_message()  # ERROR TEXT CAN CHANGE, BUT ERROR TEXT MUST EXIST
    #     self.assertTrue(error)
    #
    # def test_create_topic_without_short_text(self):
    #     fields = {
    #         'blog': 'Флудилка',
    #         'title': u'Создание топика с ошибкой',
    #         'short_text': u'',
    #         'main_text': u'Текст'
    #     }
    #
    #     create_page = self.open_and_set_text_to_topic(fields)
    #     create_page.submit()
    #
    #     error = create_page.get_error_message()  # ERROR TEXT CAN CHANGE, BUT ERROR TEXT MUST EXIST
    #     self.assertTrue(error)

    def test_create_topic_with_bold(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с жирным текстом',
            'short_text': u'шорты',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_text_to_topic(fields, effect_for_main='bold')
        create_page.submit()

        topic_page = TopicPage(self.driver)
        bold_txt = topic_page.get_bold()
        self.assertEqual(fields['main_text'], bold_txt)
        topic_page.delete()