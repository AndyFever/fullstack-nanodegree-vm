from selenium import webdriver


domain = "http://localhost:5000"

def before_all(context):
    context.browser = webdriver.Firefox()
    # context.browser = webdriver.Chrome() if you have set chromedriver in your PATH
    context.browser.set_page_load_timeout(25)
    context.browser.implicitly_wait(25)
    context.browser.maximize_window()


def after_all(context):
    context.browser.quit()

