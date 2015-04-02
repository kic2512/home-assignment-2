# coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from page_object import AuthPage, CreateTopicPage, TopicPage, down_keys, LINK_TO_HABR, LINK_TO_KITTY,\
    USER_NAME_FOR_LINK, FludilkaPage, DraftsPage

__author__ = 'kic'

import os
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote

MY_NAME = u'Господин Губернатор'


class TestWithAuth(TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self.current_topic_page = TopicPage(self.driver)
        self.is_delete = False

        user_email = 'ftest11@tech-mail.ru'
        password = os.environ.get('TTHA2PASSWORD')

        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_page.open_auth_form()
        auth_page.set_login(user_email)
        auth_page.set_password(password)
        auth_page.submit()
        current_name = auth_page.get_username_from_settings()
        self.assertEqual(MY_NAME, current_name)

    def tearDown(self):
        if self.is_delete:
            self.current_topic_page.delete()
            self.current_topic_page.get_username_from_settings()
        self.driver.quit()


class CreateTopic(TestWithAuth):
    # В этом кейсе проверяется функционал
    # создания топика и отображения топика

    def is_comment_available(self, topic_page):
        try:
            topic_page.add_comment()
        except NoSuchElementException:
            return False
        return True

    def check_not_public_topic(self, fludilka_page):
        try:
            fludilka_page.get_not_public_topic()
        except NoSuchElementException:
            return False
        return True

    def open_and_set_text_to_topic(self, fields):
        create_page = CreateTopicPage(self.driver)
        create_page.open()

        create_page.blog_select_open()
        create_page.blog_select_set_option(fields['blog'])
        create_page.set_title(fields['title'])

        create_page.activate_short_text()
        down_keys(create_page.driver, fields['short_text'])

        create_page.activate_main_text()
        down_keys(create_page.driver, fields['main_text'])
        return create_page

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

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(fields['title'], topic_title)
        self.assertEqual(fields['main_text'], topic_text)

    def test_create_topic_with_public(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с публикацией',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_text_to_topic(fields)
        create_page.submit()

        fludilka_page = FludilkaPage(self.driver)
        fludilka_page.open()
        fludilka_page.get_username_from_settings()

        topic_text = fludilka_page.get_public_topic_title()
        short_text = fludilka_page.get_public_topic_short_message()

        self.current_topic_page = fludilka_page
        self.is_delete = True

        self.assertEqual(fields['title'], topic_text)
        self.assertEqual(fields['short_text'], short_text)

    def test_create_topic_with_quiz(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика c опросом',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        quiz_title = 'QuizTitle'
        quiz_first = 'first'
        quiz_second = 'second'

        create_page = self.open_and_set_text_to_topic(fields)

        create_page.add_quiz()
        create_page.set_quiz_title(quiz_title)
        create_page.set_quiz_var0(quiz_first)
        create_page.set_quiz_var1(quiz_second)
        create_page.submit()

        topic_page = TopicPage(self.driver)

        first_quiz_answer = topic_page.get_first_quiz_var()
        second_quiz_answer = topic_page.get_second_quiz_var()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(quiz_first, first_quiz_answer)
        self.assertEqual(quiz_second, second_quiz_answer)

    def test_create_topic_add_comment(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика c комментарием',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }

        comment_text = u"Мой комментарий"

        create_page = self.open_and_set_text_to_topic(fields)
        create_page.submit()

        topic_page = TopicPage(self.driver)
        topic_page.add_comment()
        topic_page.comment_activate()
        down_keys(self.driver, comment_text)
        topic_page.comment_send()

        self.current_topic_page = topic_page
        self.is_delete = True

        real_comment = topic_page.get_comment()
        self.assertEqual(comment_text, real_comment)

    def test_create_topic_block_comments(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика c опросом',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }

        create_page = self.open_and_set_text_to_topic(fields)
        create_page.set_block_for_comment()
        create_page.submit()

        topic_page = TopicPage(self.driver)
        check = self.is_comment_available(topic_page)

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertFalse(check)

    def test_create_topic_without_title(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }

        create_page = self.open_and_set_text_to_topic(fields)
        create_page.submit()

        error = create_page.get_error_message()  # ERROR TEXT CAN CHANGE, BUT ERROR TEXT MUST EXIST
        self.assertTrue(error)

    def test_create_topic_without_main_text(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с ошибкой',
            'short_text': u'Короткий текст',
            'main_text': u''
        }

        create_page = self.open_and_set_text_to_topic(fields)
        create_page.submit()

        error = create_page.get_error_message()  # ERROR TEXT CAN CHANGE, BUT ERROR TEXT MUST EXIST
        self.assertTrue(error)

    def test_create_topic_without_short_text(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с ошибкой',
            'short_text': u'',
            'main_text': u'Текст'
        }

        create_page = self.open_and_set_text_to_topic(fields)
        create_page.submit()

        error = create_page.get_error_message()  # ERROR TEXT CAN CHANGE, BUT ERROR TEXT MUST EXIST
        self.assertTrue(error)

    def test_create_topic_not_public(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика без публикации',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_text_to_topic(fields)
        create_page.set_not_public()
        create_page.submit()

        fludilka_page = FludilkaPage(self.driver)
        fludilka_page.open()
        fludilka_page.get_username_from_settings()

        is_topic_exists = self.check_not_public_topic(fludilka_page)
        self.assertFalse(is_topic_exists)

        draft_page = DraftsPage(self.driver)
        draft_page.open()
        draft_page.get_username_from_settings()
        topic_title = draft_page.get_not_public_topic()

        self.current_topic_page = draft_page
        self.is_delete = True

        self.assertEqual(fields['title'], topic_title)


class TestBBCode(TestWithAuth):
    # В этом кейсе проверяется функционал
    # стороннего элемента BB-Code

    def set_effect_func(self, create_page, effect):
        effects = {
            'main_bold': create_page.set_main_bold,
            'main_italic': create_page.set_main_italic,
            'main_list': create_page.set_main_list,
            'main_ordered_list': create_page.set_main_ordered_list,
            'main_link': create_page.set_link,
            'main_img_link': create_page.set_img_link,
            'main_img_local': create_page.set_img_local,  # NOT WORK NOW
            'main_usr_link': create_page.set_usr_link,
        }
        if effect in effects:
            effects[effect]()

    def open_and_set_effects_to_topic(self, fields, effect_for_short=None, effect_for_main=None, is_main_txt=True):
        create_page = CreateTopicPage(self.driver)
        create_page.open()

        create_page.blog_select_open()
        create_page.blog_select_set_option(fields['blog'])
        create_page.set_title(fields['title'])

        create_page.activate_short_text()
        if effect_for_short:
            self.set_effect_func(create_page, effect_for_short)
        down_keys(create_page.driver, fields['short_text'])

        create_page.activate_main_text()
        if effect_for_main:
            self.set_effect_func(create_page, effect_for_main)
        if is_main_txt:
            down_keys(create_page.driver, fields['main_text'])
        return create_page

    def check_img(self, page):
        try:
            page.get_src_img()
        except NoSuchElementException:
            return False
        return True

    def test_create_topic_with_bold(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с жирным текстом',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_bold')
        create_page.submit()

        topic_page = TopicPage(self.driver)
        bold_txt = topic_page.get_bold()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(fields['main_text'], bold_txt)

    def test_create_topic_with_italic(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с текстом italic',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_italic')
        create_page.submit()

        topic_page = TopicPage(self.driver)
        italic_txt = topic_page.get_italic()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(fields['main_text'], italic_txt)

    def test_create_topic_with_list(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика со списком',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_list')
        create_page.submit()

        topic_page = TopicPage(self.driver)
        list_txt = topic_page.get_list()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(fields['main_text'], list_txt)

    def test_create_topic_with_ordered_list(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с сортированным списком',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_ordered_list')
        create_page.submit()

        topic_page = TopicPage(self.driver)
        ordered_list_txt = topic_page.get_ordered_list()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(fields['main_text'], ordered_list_txt)

    def test_create_topic_with_link(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика со ссылкой',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_link')

        create_page.submit()

        topic_page = TopicPage(self.driver)
        link_txt = topic_page.get_link_text()
        link_href = topic_page.get_link_href()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(fields['main_text'], link_txt)
        self.assertEqual(LINK_TO_HABR, link_href)

    def test_create_topic_with_img_link(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика со ссылкой',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_img_link')

        create_page.submit()

        topic_page = TopicPage(self.driver)
        img_link_src = topic_page.get_src_img()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(LINK_TO_KITTY, img_link_src)

    def test_create_topic_with_user_link(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика со ссылкой на пользователя',
            'short_text': u'Короткий текст',
            'main_text': u'Текст'
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_usr_link')

        create_page.submit()

        topic_page = TopicPage(self.driver)
        topic_page.get_username_from_settings()

        user_link_href = topic_page.get_user_link_href()
        current_user_href = topic_page.get_user_href_from_settings()

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertEqual(current_user_href, user_link_href)

    def test_create_topic_with_img_local(self):
        fields = {
            'blog': 'Флудилка',
            'title': u'Создание топика с локальной картинкой',
            'short_text': u'Короткий текст',
        }
        create_page = self.open_and_set_effects_to_topic(fields, effect_for_main='main_img_local', is_main_txt=False)

        create_page.submit()

        topic_page = TopicPage(self.driver)
        topic_page.get_username_from_settings()
        is_img_exist = self.check_img(topic_page)

        self.current_topic_page = topic_page
        self.is_delete = True

        self.assertTrue(is_img_exist)