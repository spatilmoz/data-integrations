Feature: Read Bing Revenue into BQ

  Scenario: We read data from a bing provided rest endpoint
    Given job id url https://searchapi.pubcenter.microsoft.com/api/v3/report
    And report id url https://searchapi.pubcenter.microsoft.com/api/v1/reportjobs/
    And the report name is Distribution performance report
    And the date range is from 2019-08-01 to 2019-08-12
    And the report type is Distribution
    And the report granularity is Day
    And the report columns are DistributionPartnerCode,FormCode,Clicks,BiddedSRPVs
    When we hit the endpoint
    Then we get a response