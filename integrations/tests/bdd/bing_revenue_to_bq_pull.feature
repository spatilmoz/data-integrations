Feature: Read Bing Revenue into BQ

  Scenario: We read data from a bing provided rest endpoint
    Given the report name is Distribution performance report
    And the date range is from 2019-08-01 to 2019-08-01
    And the report type is Distribution
    And the report granularity is Day
    And the report columns are DistributionPartnerCode,FormCode,Clicks,BiddedSRPVs,RawSRPVs,EstimatedRevenue,Market,Language,DeviceType,Currency,Impressions,AdImpressions,AdImpressionYield,RPM,CPC,ClickYield,AdCTR,Coverage,AdDensity,CTR,BiddedCTR,UserCountry,WebSiteCountry,WebSiteLanguage
    When we hit the endpoint
    Then we get a response