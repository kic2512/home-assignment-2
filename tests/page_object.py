# coding=utf-8
# charset utf-8

import urlparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from os import getcwd

__author__ = 'kic'

LINK_TO_HABR = 'http://habrahabr.ru/post/114772/'
LINK_TO_KITTY = 'http://wpapers.ru/wallpapers/animals/Cats/8597/PREV_%D0%A1%D0%B5%D1%80%D1%8B%D0%B9-%D0%BA%D0%BE%D1%82%D1%91%D0%BD%D0%BE%D0%BA.jpg'
USER_NAME_FOR_LINK = u'Господин Губернатор'


def down_keys(driver, text):
        ActionChains(driver).send_keys(text).perform()


class Page(object):
    BASE_URL = 'http://ftest.stud.tech-mail.ru/'
    PATH = ''
    USERNAME = '//a[@class="username"]'

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)

    def get_username_from_settings(self):
        return WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USERNAME).text
        )

    def get_user_href_from_settings(self):
        return WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USERNAME).get_attribute('href')
        )


class Topic(Page):

    FIRST_LINK_IN_CONTENT = '//div[@class="topic-content text"]/p/a'

    DELETE_BUTTON = '//a[@class="actions-delete"]'
    DELETE_BUTTON_CONFIRM = '//input[@value="Удалить"]'

    def get_link_text(self):
        return self.driver.find_element_by_xpath(self.FIRST_LINK_IN_CONTENT).text

    def get_link_href(self):
        return self.driver.find_element_by_xpath(self.FIRST_LINK_IN_CONTENT).get_attribute('href')

    def delete(self):
        self.driver.find_element_by_xpath(self.DELETE_BUTTON).click()
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.DELETE_BUTTON_CONFIRM)
        )
        self.driver.find_element_by_xpath(self.DELETE_BUTTON_CONFIRM).click()


class AuthPage(Page):
    PATH = ''
    LOGIN = '//input[@name="login"]'
    PASSWORD = '//input[@name="password"]'
    SUBMIT = '//span[text()="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход для участников"]'

    def open_auth_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).clear()
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).clear()
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class CreateTopicPage(Page):
    PATH = '/blog/topic/create/'
    BLOGSELECT = '//a[@class="chzn-single"]'
    OPTION = '//li[text()="{}"]'
    TITLE = '//input[@name="title"]'
    CREATE_BUTTON = '//button[contains(text(),"Создать")]'

    AREA_SHORT_AROUND_CLC = '(//div[@class="CodeMirror-sizer"])[1]'
    AREA_MAIN_AROUND_CLC = '(//div[@class="CodeMirror-sizer"])[2]'

    QUIZ_CHECK = '//p/label[contains(text()[normalize-space()], "Добавить опрос к топику")]'
    QUIZ_TITLE = '//input[@name="question"]'
    QUIZ_VAR0 = '//input[@name="form-0-answer"]'
    QUIZ_VAR1 = '//input[@name="form-1-answer"]'

    BLOCK_COMMENT = '//input[@name="forbid_comment"]'

    ERRORS_MESSAGES = '//ul[@class="system-message-error"]/li[contains(text(),"Это поле обязательно для заполнения")]'

    BOLD_MAIN_BTN = '(//a[@class="markdown-editor-icon-bold"])[2]'
    ITALIC_MAIN_BTN = '(//a[@class="markdown-editor-icon-italic"])[2]'
    LIST_MAIN_BTN = '(//a[@class="markdown-editor-icon-unordered-list"])[2]'
    ORDERED_LIST_MAIN_BTN = '(//a[@class="markdown-editor-icon-ordered-list"])[2]'
    LINK_MAIN_BTN = '(//div[@class="editor-toolbar"]/a[@title="Вставить ссылку"])[2]'
    IMG_LINK_MAIN_BTN = '(//div[@class="editor-toolbar"]/a[@title="Вставить изображение"])[2]'
    IMG_LOCAL_MAIN_BTN = '(//div[@class="editor-toolbar"]/a[@title="Загрузить изображение"])[2]'
    USR_LINK_MAIN = '(//div[@class="editor-toolbar"]/a[@title="Добавить пользователя"])[2]'
    USR_INPUT_FIELD = '//div/input[@id="search-user-login-popup"]'
    USR_INPUT_CHOICE = '//*[@id="list-body"]/tr[1]/td/div/p[2]/a'
    NOT_PUBLIC = '//input[@name="publish"]'
    FILE_MAIN_INPUT = '(//input[@name="filedata"])[2]'
    MIRROR_MAIN_CODE = '(//div[@class="CodeMirror-code"]/pre/span)[2]'

    def blog_select_open(self):
        self.driver.find_element_by_xpath(self.BLOGSELECT).click()

    def blog_select_set_option(self, option_text):
        self.driver.find_element_by_xpath(self.OPTION.format(option_text)).click()

    def set_title(self, title):
        self.driver.find_element_by_xpath(self.TITLE).send_keys(title)

    def submit(self):
        self.driver.find_element_by_xpath(self.CREATE_BUTTON).click()

    def set_not_public(self):
        self.driver.find_element_by_xpath(self.NOT_PUBLIC).click()

    def activate_short_text(self):
        self.driver.find_element_by_xpath(self.AREA_SHORT_AROUND_CLC).click()

    def activate_main_text(self):
        self.driver.find_element_by_xpath(self.AREA_MAIN_AROUND_CLC).click()

    def add_quiz(self):
        self.driver.find_element_by_xpath(self.QUIZ_CHECK).click()

    def set_quiz_title(self, title):
        self.driver.find_element_by_xpath(self.QUIZ_TITLE).send_keys(title)

    def set_quiz_var0(self, text):
        self.driver.find_element_by_xpath(self.QUIZ_VAR0).send_keys(text)

    def set_quiz_var1(self, text):
        self.driver.find_element_by_xpath(self.QUIZ_VAR1).send_keys(text)

    def set_block_for_comment(self):
        self.driver.find_element_by_xpath(self.BLOCK_COMMENT).click()

    def get_error_message(self):
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.ERRORS_MESSAGES)
        )
        return self.driver.find_element_by_xpath(self.ERRORS_MESSAGES).text

    def set_main_bold(self):
        self.driver.find_element_by_xpath(self.BOLD_MAIN_BTN).click()

    def set_main_italic(self):
        self.driver.find_element_by_xpath(self.ITALIC_MAIN_BTN).click()

    def set_main_list(self):
        self.driver.find_element_by_xpath(self.LIST_MAIN_BTN).click()

    def set_main_ordered_list(self):
        self.driver.find_element_by_xpath(self.ORDERED_LIST_MAIN_BTN).click()

    def set_link(self):
        self.driver.find_element_by_xpath(self.LINK_MAIN_BTN).click()
        Alert(driver=self.driver).send_keys(LINK_TO_HABR)
        Alert(driver=self.driver).accept()

    def set_img_link(self):
        self.driver.find_element_by_xpath(self.IMG_LINK_MAIN_BTN).click()
        Alert(driver=self.driver).send_keys(LINK_TO_KITTY)
        Alert(driver=self.driver).accept()

    def set_usr_link(self):
        self.driver.find_element_by_xpath(self.USR_LINK_MAIN).click()
        find_by = USER_NAME_FOR_LINK.split(' ')[1]
        self.driver.find_element_by_xpath(self.USR_INPUT_FIELD).send_keys(find_by)
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USR_INPUT_CHOICE).text
        )
        self.driver.find_element_by_xpath(self.USR_INPUT_CHOICE).click()

    def set_img_local(self):
        path = getcwd() + "/kitty.jpg"
        self.driver.execute_script('$(".markdown-upload-photo-container").show()')
        self.driver.find_element_by_xpath(self.FILE_MAIN_INPUT).send_keys(path)
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MIRROR_MAIN_CODE)
        )


class TopicPage(Topic):
    BLOG = '//*[@class="topic-blog"]'
    QUIZ_TITLE = '//ul[@class="poll-vote"]/li/label'
    QUIZ_VAR0 = '(//ul[@class="poll-vote"]/li/label)[1]'
    QUIZ_VAR1 = '(//ul[@class="poll-vote"]/li/label)[2]'
    ADD_COMMENT_LNK = '//a[text() = "Оставить комментарий"]'
    COMMENT_AREA = '//div[@class="CodeMirror-sizer"]'
    COMMENT_SEND = '//button[text() = "добавить"]'
    COMMENT_TEXT = '//div[@class="comment-rendered"]/p'

    USERNAME = '//a[@class="username"]'
    TITLE = '//*[@class="topic-title"]/a'
    TEXT = '//*[@class="topic-content text"]/p'

    BOLD_TEXT = '//div[@class="topic-content text"]/p/strong'
    ITALIC_TEXT = '//div[@class="topic-content text"]/p/em'
    LIST_TEXT = '//div[@class="topic-content text"]/ul/li'
    ORDERED_LIST_TEXT = '//div[@class="topic-content text"]/ol/li'
    LINK = '//div[@class="topic-content text"]/p/a'
    IMG = '//div[@class="topic-content text"]/p/img'
    LINK_TO_USER = '//div[@class="topic-content text"]/p/a[contains(text(),"Господин Губернатор")]'

    def get_title(self):
        return self.driver.find_element_by_xpath(self.TITLE).text

    def get_text(self):
        return self.driver.find_element_by_xpath(self.TEXT).text

    def open_main_page(self):
        self.driver.find_element_by_xpath(self.BLOG).click()

    def get_first_quiz_var(self):
        return self.driver.find_element_by_xpath(self.QUIZ_VAR0).text

    def get_second_quiz_var(self):
        return self.driver.find_element_by_xpath(self.QUIZ_VAR1).text

    def get_quiz_title(self):
        return self.driver.find_element_by_xpath(self.QUIZ_TITLE).text

    def get_quiz_answers(self):
        return self.driver.find_element_by_xpath(self.QUIZ_TITLE)

    def add_comment(self):
        self.driver.find_element_by_xpath(self.ADD_COMMENT_LNK).click()

    def comment_activate(self):
        self.driver.find_element_by_xpath(self.COMMENT_AREA).click()

    def comment_send(self):
        self.driver.find_element_by_xpath(self.COMMENT_SEND).click()

    def get_comment(self):
        return self.driver.find_element_by_xpath(self.COMMENT_TEXT).text

    def get_bold(self):
        return self.driver.find_element_by_xpath(self.BOLD_TEXT).text

    def get_italic(self):
        return self.driver.find_element_by_xpath(self.ITALIC_TEXT).text

    def get_list(self):
        return self.driver.find_element_by_xpath(self.LIST_TEXT).text

    def get_ordered_list(self):
        return self.driver.find_element_by_xpath(self.ORDERED_LIST_TEXT).text

    def get_src_img(self):
        return self.driver.find_element_by_xpath(self.IMG).get_attribute('src')

    def get_user_link_name(self):
        return self.driver.find_element_by_xpath(self.LINK_TO_USER).text

    def get_user_link_href(self):
        return self.driver.find_element_by_xpath(self.LINK_TO_USER).get_attribute('href')


class FludilkaPage(Topic):
    PATH = '/blog/show/2544/fludilka/'
    TOPIC_TITLE = '//h1[@class="topic-title"]/a'
    TOPIC_PUBLIC = '//h1[@class="topic-title"]/a[contains(text(),"Создание топика с публикацией")]'
    TOPIC_PUBLIC_SHORT_MESSAGE = '//div[@class="topic-content text"]/p[contains(text(),"Короткий текст")]'
    TOPIC_NOT_PUBLIC_TITLE = '//h1[@class="topic-title"]/a[contains(text(),"Создание топика без публикации")]'
    TOPIC_PUBLIC_SHORT_USR_LINK = '//div[@class="topic-content text"]/p/a[contains(text(),"Господин Губернатор")]'

    def get_not_public_topic(self):
        return self.driver.find_element_by_xpath(self.TOPIC_NOT_PUBLIC_TITLE).text

    def get_public_topic_title(self):
        return self.driver.find_element_by_xpath(self.TOPIC_PUBLIC).text

    def get_public_topic_short_message(self):
        return self.driver.find_element_by_xpath(self.TOPIC_PUBLIC_SHORT_MESSAGE).text

    def get_public_topic_short_user_link_txt(self):
        return self.driver.find_element_by_xpath(self.TOPIC_PUBLIC_SHORT_USR_LINK).text

    def get_public_topic_short_user_link_href(self):
        return self.driver.find_element_by_xpath(self.TOPIC_PUBLIC_SHORT_USR_LINK).get_attribute('href')


class DraftsPage(Topic):
    PATH = '/blog/topics/draft/'

    def get_not_public_topic(self):
        return self.driver.find_element_by_xpath(FludilkaPage.TOPIC_NOT_PUBLIC_TITLE).text