# coding=utf-8
# charset utf-8

import urlparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

__author__ = 'kic'


def down_keys(driver, text):
        ActionChains(driver).send_keys(text).perform()


class Page(object):
    BASE_URL = 'http://ftest.stud.tech-mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = ''
    LOGIN = '//input[@name="login"]'
    PASSWORD = '//input[@name="password"]'
    SUBMIT = '//span[text()="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход для участников"]'
    USERNAME = '//a[@class="username"]'

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

    def get_username(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USERNAME).text
        )


class CreateTopicPage(Page):
    PATH = '/blog/topic/create/'
    BLOGSELECT = '//a[@class="chzn-single"]'
    OPTION = '//li[text()="{}"]'
    TITLE = '//input[@name="title"]'
    CREATE_BUTTON = '//button[contains(text(),"Создать")]'

    AREA_SHORT_AROUND_CLC = '//*[@id="content"]/div/div[1]/form/div/div[3]/div[6]/div[1]/div/div/div/div[3]/pre[1]'  # TODO CHANGE
    AREA_MAIN_AROUND_CLC = '//*[@id="content"]/div/div[1]/form/div/div[6]/div[6]/div[1]'  # TODO CHANGE

    QUIZ_CHECK = '//*[@id="content"]/div/div[1]/form/div/p[7]/label'  # TODO CHANGE
    QUIZ_TITLE = '//input[@name="question"]'
    QUIZ_VAR0 = '//input[@name="form-0-answer"]'
    QUIZ_VAR1 = '//input[@name="form-1-answer"]'

    BLOCK_COMMENT = '//input[@name="forbid_comment"]'

    ERRORS_MESSAGES = '//ul[@class="system-message-error"]/li[contains(text(),"Это поле обязательно для заполнения")]'

    BOLD_BTN = '//a[@class="markdown-editor-icon-bold"]'

    def blog_select_open(self):
        self.driver.find_element_by_xpath(self.BLOGSELECT).click()

    def blog_select_set_option(self, option_text):
        self.driver.find_element_by_xpath(self.OPTION.format(option_text)).click()

    def set_title(self, title):
        self.driver.find_element_by_xpath(self.TITLE).send_keys(title)

    def submit(self):
        self.driver.find_element_by_xpath(self.CREATE_BUTTON).click()

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
        return self.driver.find_element_by_xpath(self.ERRORS_MESSAGES).text

    def set_bold(self):
        self.driver.find_element_by_xpath(self.BOLD_BTN).click()


class TopicPage(Page):
    BLOG = '//*[@class="topic-blog"]'
    DELETE_BUTTON = '//a[@class="actions-delete"]'
    DELETE_BUTTON_CONFIRM = '//input[@value="Удалить"]'
    QUIZ_TITLE = '//ui[class="pool-vote"]/li/label'
    QUIZ_VAR0 = '//*[@id="content"]/div/div[1]/article/div/div[1]/form/ul/li[1]/label'  # TODO CHANGE
    QUIZ_VAR1 = '//*[@id="content"]/div/div[1]/article/div/div[1]/form/ul/li[2]/label'  # TODO CHANGE
    ADD_COMMENT_LNK = '//a[text() = "Оставить комментарий"]'
    COMMENT_AREA = '//div[@class="CodeMirror-sizer"]'
    COMMENT_SEND = '//button[text() = "добавить"]'
    COMMENT_TEXT = '//div[@class="comment-rendered"]/p'

    USERNAME = '//a[@class="username"]'
    TITLE = '//*[@class="topic-title"]/a'
    TEXT = '//*[@class="topic-content text"]/p'

    BOLD_TEXT = '//div[@class="topic-content text"]/p/strong'

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

    def delete(self):
        self.driver.find_element_by_xpath(self.DELETE_BUTTON).click()
        self.driver.find_element_by_xpath(self.DELETE_BUTTON_CONFIRM).click()