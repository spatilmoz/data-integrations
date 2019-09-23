Feature: Push Bing Revenue into BQ

  Scenario: We push Bing data to BQ
    Given this report integrations/tests/resources/report.csv
    Then we write the report data to BQ