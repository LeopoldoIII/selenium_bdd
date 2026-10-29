@api
Feature: Users API Integration

  @smoke
  Scenario: Retrieve list of users
    When I send a GET request to "/api/users?page=2"
    Then the response status code should be 200
    And the response body should contain key "data"
    And the response body key "page" should equal 2

  @regression
  Scenario: Create a new user
    When I send a POST request to "/api/users" with payload:
      """
      {
        "name": "morpheus",
        "job": "leader"
      }
      """
    Then the response status code should be 201
    And the response body should contain key "id"
    And the response body key "name" should equal "morpheus"

