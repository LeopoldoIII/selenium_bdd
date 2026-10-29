@ui
Feature: SauceDemo Authentication

  Background:
    Given I open the SauceDemo login page

  @smoke
  Scenario: Successful login with valid credentials
    When I enter valid credentials for "standard" user
    And I click the login button
    Then I should be redirected to the inventory products page
    And I take a screenshot of the current page

  @regression
  Scenario: Failed login with locked out user
    When I enter credentials for locked out user
    And I click the login button
    Then I should see the error message "Epic sadface: Sorry, this user has been locked out."
