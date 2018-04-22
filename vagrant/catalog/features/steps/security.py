#!/usr/bin/env python2

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
    # Explicit wait for page to load
    explicit_wait(context, 'ID', 'username')


@then("I should see a message saying the user has been created")
def step_impl(context):
    explicit_wait(context, 'ID', 'user_message')
    message = context.browser.find_element(By.ID, 'user_message').text
    assert (message == 'New user created')


@when('I enter the username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.find_element(By.ID, 'username').send_keys(username)
    context.browser.find_element(By.ID, 'password').send_keys(password)
    context.browser.find_element(By.ID, 'submit').click()


@given("I am on the login page")
def step_impl(context):
    url = '/login'
    context.browser.get(domain + url)
    explicit_wait(context, 'ID', '___signin_0')


@when('I enter my username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.find_element(By.ID, 'username').send_keys(username)
    context.browser.find_element(By.ID, 'password').send_keys(password)
    context.browser.find_element(By.ID, 'submit').click()


@then("I should be logged in to TestingBoK")
def step_impl(context):
    explicit_wait(context, 'CLASS_NAME', 'heading')
    assert (context.browser.find_element(By.ID, 'logout').text == "Logout")
    logout(context)


@step("The user logs out")
def step_impl(context):
    """
    Used to log the user out after a test has been run
    """
    logout(context)


def logout(context):
    explicit_wait(context, 'ID', 'logout')
    context.browser.find_element(By.ID, 'logout').click()
    explicit_wait(context, 'LINK_TEXT', 'Take me home!')
    context.browser.find_element(By.ID, 'logout').click()
    explicit_wait(context, 'LINK_TEXT', 'Login')


def explicit_wait(context, matcher, identifier):
    if matcher == 'ID':
        element = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.ID, identifier)))
    elif matcher == 'LINK_TEXT':
        element = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, identifier)))
    elif matcher == 'CLASS_NAME':
        element = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, identifier)))


@when("I enter just a username")
def step_impl(context):
    context.browser.find_element(By.ID,
                                 'username').send_keys("just a username")
    context.browser.find_element(By.ID,
                                 'submit').click()


@when("I enter just a password")
def step_impl(context):
    context.browser.find_element(By.ID,
                                 'password').send_keys("just a password")
    context.browser.find_element(By.ID,
                                 'submit').click()


@then('I should get an error message saying "{error_message}"')
def step_impl(context, error_message):
    explicit_wait(context, 'LINK_TEXT', 'Home')
    assert (context.browser.find_element(By.ID,
                                         'user_message').text == error_message)
