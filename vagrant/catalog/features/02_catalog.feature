# Created by andyfever at 13/04/2018
Feature: The user should be able to browse the catalog for articles

  In this project, you will be developing a web application that provides a list of
  items within a variety of categories and integrate third party user registration
  and authentication. Authenticated users should have the ability to post, edit,
  and delete their own items

  Scenario: The homepage displays all the current categories
    Given I am on the homepage
    Then I should see the current list of categories

  Scenario: The homepage displays the latest articles
    Given I am on the homepage
    Then I should see the latest articles

  Scenario Outline: Selecting a specific category shows the available articles
    Given I am on the homepage
    When I select the "<category>"
    Then I should see the "<articles>"

    Examples: Articles for Tools and Techniques
      | category   | articles                                    |
      | Tools      | Cucumber Automation, Keyword Driven Testing |
      | Techniques | Equivalence Partitioning, Boundary Analysis |

  Scenario: Selecting a specific article should show the article text
    Given I am on the homepage
    And I have selected the category Process
    And I have selected the article Pair Programming
    Then I should see the article text

  Scenario: The user if logged in should be able to add a new article
    Given I am logged in and on the add article page
    And I give the article a title, some text and a category
      | title        | text                                  | category |
      | Kanban Teams | # Introduction to Kanban Teams        | Process  |
    Then I should see my article listed under the Category
      | title        | category |
      | Kanban Teams | Process  |
    And The user logs out

  Scenario: The user if not logged in shouldn't be able to add a new article
    Given I am on the homepage
    Then I should not be able to go to the add article page

  Scenario: The user if logged in should be able to add a new category
    Given I am logged in as the user Python
    And I can see the Add Category link
    When I add the category People
    Then I should see People listed on the homepage
    And The user logs out

  Scenario: The user should be able to edit an article if they are the owner
    Given I am logged in as the user Python
    And I have selected the category Process
    And I have selected the article Kanban Teams
    When I select edit article from the article page
    Then I should be able to edit the article
    And The user logs out