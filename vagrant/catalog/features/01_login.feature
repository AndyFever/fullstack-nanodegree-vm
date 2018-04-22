Feature: Creating a new user

  Note - the google login in not implemented as it requires a full
  user id

  Scenario: Successfully creating a new user
    Given I am on the create new user page
    When I enter the username "python" and password "flask"
    Then I should see a message saying the user has been created

  Scenario: I should be able to log in with the newly created user
    Given I am on the login page
    When I enter my username "python" and password "flask"
    Then I should be logged in to TestingBoK

  Scenario: I should get an error message when I don't enter a password
    Given I am on the create new user page
    When I enter just a username
    Then I should get an error message saying "Please enter a valid username and password"

  Scenario: I should get an error message when I don't enter a username
    Given I am on the create new user page
    When I enter just a password
    Then I should get an error message saying "Please enter a valid username and password"

    
  Scenario: I should get an error message when I log in with a user who already exists
    Given I am on the create new user page
    When I enter my username "python" and password "flask"
    Then I should get an error message saying "User already exists"