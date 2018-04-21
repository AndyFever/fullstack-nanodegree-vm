Feature: Creating a new user

  Note - the google login in not impelemented as it requires a full id

  Scenario: Successfully creating a new user
    Given I am on the create new user page
    When I enter the username "andy" and password "fever"
    Then I should see a message saying the user has been created

  Scenario: I should be able to log in with the newly created user
    Given I am on the login page
    When I enter my username "andy" and password "fever"
    Then I should be logged in to TestingBoK
