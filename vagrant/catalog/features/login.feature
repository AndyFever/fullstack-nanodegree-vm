#  --File: features/login.feature

Feature:

  Scenario: Create a new user
    Given I am on the new user page
    When I enter the username "admin" and password "admin" and submit
    Then I should be logged in with username "admin" and password "admin"

  Scenario: Login to TestingBoK using a username and password
    Given I am on the login page
    When I enter the username "admin" and password "admin" and submit
    Then I should be logged in with username "admin" and password "admin"
