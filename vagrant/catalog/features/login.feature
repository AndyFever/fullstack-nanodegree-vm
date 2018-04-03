#  --File: features/login.feature

Feature:

  Scenario: Create a new user
    Given I am on the new user page
    When I enter the username "andy" and password "fever" and submit
    Then I should see a message saying "user succesfully created"

  Scenario: Login to TestingBoK using a username and password
    Given I am on the login page
    When I enter the username "andy" and password "fever" and submit
    Then I should be logged in with username "andy" and password "fever"

  Scenario: The homepage should display the correct topics
    Given I am on the homepage
    Then I should see the following categories
      | Tools        |
      | Process      |
      | Techniques   |
      | Resources    |
      | Technologies |
      | Stories      |

  Scenario: The techniques category should contain the correct articles
    Given I am on the homepage
    When I have selected the category "Techniques"
    Then I should be shown the articles
      | Equivalence Partioning |
      | Boundary Analysis      |

  Scenario: Selecting an item shows you specific information about that item
    Given I am on the homepage
    And I have selected the category "Process"
    When I select the article "Behavioral Driven Development"
    Then I should see the article "Behavioral Driven Development"

  Scenario: A user should be able to add an article once logged in
    Given I am logged in as "Admin"
    And I have selected Add Article
    Then I should be able to save a new article

  Scenario: A user should be able to delete an article once logged in
    Given I am logged in as "Admin"
    When I have selected the category "Resources"
    And I select the article "ISTQB Guide"
    Then I should be able to delete the article

  Scenario: A user should be able to edit an artilce once logged in
    Given I am logged in as "Admin"
    When I have selected the category "Stories"
    And I select the article "Agile Testing"
    Then I should be able to edit the article
