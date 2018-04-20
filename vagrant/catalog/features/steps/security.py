from behave import *
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import unittest
from selenium.webdriver.support import expected_conditions as EC
import time

domain = "http://localhost:5000"

@given("I am on the create new user page")
def step_impl(context):
    context.browser.get(domain)
    time.sleep(3)
    context.browser.find_element(By.ID, 'create_user').click()
    element = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "username")))


@then("I should see a message saying the user has been created")
def step_impl(context):
    pass


@when('I enter the username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.find_element(By.ID, 'username').send_keys(username)
    context.browser.find_element(By.ID, 'password').send_keys(password)
    context.browser.find_element(By.ID, 'submit').click()
    element = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "user_message")))
    message = context.browser.find_element(By.ID, 'user_message').text
    assert(message == 'New user created')


@given("I am on the login page")
def step_impl(context):
    url = '/login'

    context.browser.get(domain + url)
    time.sleep(1)


@when('I enter my username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.find_element(By.ID, 'username').send_keys(username)
    context.browser.find_element(By.ID, 'password').send_keys(password)
    context.browser.find_element(By.ID, 'submit').click()
    time.sleep(1)
    assert (context.browser.find_element(By.ID, 'logout').text == "Logout")


@then("I should be logged in to TestingBoK")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass

def logout(context):
    time.sleep(3)
    context.browser.find_element(By.ID, 'logout').click()


@step("The user logs out")
def step_impl(context):
    """
    Used to log the user out after a test has been run
    """
    context.browser.get(domain)
    time.sleep(2)
    # Go to the logout page
    context.browser.find_element(By.ID, 'logout').click()
    # Click the logout button
    context.browser.find_element(By.ID, 'logout').click()