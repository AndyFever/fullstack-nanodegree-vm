# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step
from behave   import given, when, then
from hamcrest import assert_that, equal_to


@given(u'I am on the new user page')
def step_impl(context):
    context.browser.visit('/new_user')
    message = context.browser.find_by_id('auth_message')
    assert message.text == 'Please enter a username and password to create a new user:'


@when(u'I enter the username "{username}" and password "{password}" and submit')
def step_impl(context, username, password):
    username_field = context.browser.find_by_id('username')
    password_field = context.browser.find_by_id('password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_button = context.browser.find_by_id('submit')
    submit_button.click()


@given(u'I am on the login page')
def step_impl(context):
    context.browser.visit('/login')
    message = context.browser.find_by_id('google_login')
    assert message.text == 'Login with google'


@then(u'I should be logged in with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    # User should be redirected to the homepage
    message = context.browser.find_by_link('Logout')
    message.text == 'Logout'

@then(u'I should see a message saying "user succesfully created"')
def step_impl(context):
    pass

@given(u'I am on the homepage')
def step_impl(context):
    context.browser.visit('/')

@then(u'I should see the following categories')
def step_impl(context):
    categorys = context.browser.find_elements_by_id('categorys')
    print(categorys)
    assert_that(categorys(categorys. has_item('Tools')))
