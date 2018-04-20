from behave import *
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import unittest
from selenium.webdriver.support import expected_conditions as EC
import time
import re

use_step_matcher("re")

domain = "http://localhost:5000"
@given("I am on the homepage")
def step_impl(context):
    context.browser.get(domain)
    assert (context.browser.title == "TestingBoK")
    time.sleep(2)



@then("I should see the current list of categories")
def step_impl(context):
    # Setup the default categories
    categories = ['Tools', 'Process', 'Techniques',
                  'Resources','Technologies', 'Stories']

    elements = context.browser.find_elements(By.ID, 'categorys')

    # Check there aren't any categories we don't know about
    assert len(elements) == len(categories)

    for e in elements:
        assert(e.text in categories)


@then("I should see the latest articles")
def step_impl(context):
    # Setup the default articles
    articles = ['Cucumber Automation', 'Behavioral Driven Development',
                'Equivalence Partitioning', 'Project Management BoK',
                'Restfull APIs', 'Agile Testing', 'Keyword Driven Testing',
                'Pair Programming', 'Boundary Analysis', 'ISTQB Guide']

    elements = context.browser.find_elements(By.ID, 'article_list')

    # Check there aren't any categories we don't know about
    assert len(elements) == len(articles)

    for e in elements:
        assert(e.text in articles)


@when('I select the "(?P<category>.+)"')
def step_impl(context, category):
    context.browser.find_element(By.LINK_TEXT, category).click()


@then('I should see the "(?P<articles>.+)"')
def step_impl(context, articles):
    # element = context.browser.find_element(By.ID, 'sub_article').text()

    list_articles = articles.split(',')

    # Remove preceding whitespace
    sub_articles = []
    for item in list_articles:
        sub_articles.append(re.sub(r"^\s+", "", item, flags=re.UNICODE))

    page_articles = context.browser.find_elements(By.ID, 'sub_article')

    for p in page_articles:
        assert(p.text in sub_articles)


@given('I have selected the category (?P<category>.+)')
def step_impl(context, category):
    category = category.replace('"', '')
    context.browser.find_element(By.LINK_TEXT, category).click()


@step('I have selected the article (?P<article>.+)')
def step_impl(context, article):
    context.browser.find_element(By.LINK_TEXT, article).click()



@then("I should see the article text")
def step_impl(context):
    article_text = 'Pair Programming'

    text = context.browser.find_element(By.CLASS_NAME, "article_text").text

    assert(article_text in text)


@given("I am logged in and on the add article page")
def step_impl(context):
    # TODO setup a default user or a global login system
    context.browser.get(domain + '/login')
    time.sleep(3)
    context.browser.find_element(By.ID, 'username').send_keys('andy')
    context.browser.find_element(By.ID, 'password').send_keys('fever')
    context.browser.find_element(By.ID, 'submit').click()
    time.sleep(1)
    assert (context.browser.find_element(By.ID, 'logout').text == "Logout")

    context.browser.get(domain + '/catalog/add_article')


@step("I give the article a title, some text and a category")
def step_impl(context):
    for row in context.table:
        title = row['title']
        text = row['text']
        category = row['category']

        context.browser.find_element(By.NAME, 'title').send_keys(title)

        context.browser.find_element(By.NAME, 'description').send_keys(text)

        all_options = context.browser.find_element(By.NAME, 'category')

        for option in all_options.find_elements(By.TAG_NAME, 'option'):
            if option.text == category:
                option.click()
                break

        context.browser.find_element(By.ID, 'submit').click()

@then("I should see my article listed under the Category")
def step_impl(context):
    for row in context.table:
        title = row['title']
        category = row['category']

    context.browser.get(domain)
    context.browser.find_element(By.LINK_TEXT, category).click()

    elements = context.browser.find_elements(By.ID, 'sub_article')

    sub_elements = []

    for el in elements:
        sub_elements.append(el.text)

    assert(title in sub_elements)



@then("I should not be able to go to the add article page")
def step_impl(context):
    context.browser.get(domain + '/catalog/add_article')
    # Check I have been redirected
    time.sleep(3)
    assert(context.browser.find_element(By.ID, 'google_login').text == 'Login with google')


@given('I am logged in as <"special_user">')
def step_impl(context):
    context.browser.get(domain + '/login')
    time.sleep(3)
    context.browser.find_element(By.ID, 'username').send_keys('andy')
    context.browser.find_element(By.ID, 'password').send_keys('fever')
    context.browser.find_element(By.ID, 'submit').click()
    time.sleep(1)
    assert (context.browser.find_element(By.ID, 'logout').text == "Logout")


@step("I can see the Add Category link")
def step_impl(context):
    context.browser.find_element(By.LINK_TEXT, 'Add Category').click()



@when('I add the category (?P<category>.+)')
def step_impl(context, category):
    context.browser.find_element(By.NAME, 'category').send_keys(category)
    context.browser.find_element(By.NAME, 'submit').click()



@then('I should see (?P<category>.+) listed on the homepage')
def step_impl(context, category):
    context.browser.find_element(By.LINK_TEXT, category).click()


@when("I select edit article from the article page")
def step_impl(context):
    context.browser.find_element(By.LINK_TEXT, 'Edit Article').click()


@then("I should be able to edit the article")
def step_impl(context):
    context.browser.find_element(By.NAME, 'title').send_keys(' 2')
    context.browser.find_element(By.ID, 'submit').click()

    # Check the article title has been updated
    assert(context.browser.find_element(By.ID, 'user_message').text == 'Article has been successfully edited')
