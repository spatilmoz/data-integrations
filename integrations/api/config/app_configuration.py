import os

config = {
    'proxies': {},
    'MozGeo': {
        'google_api_key': os.environ.get('MOZGEO_GOOGLE_API_KEY', ''),
    },
    'gpg': {
        'gpg_public_key_url': os.environ.get('PUBLIC_KEY_URL',
                                             'https://members.exacttarget.com/Content/Subscribers/SubsLists/publickey.txt'),
    },
    'sftp': {
        'sftp_host': os.environ.get('SFTP_HOST', ''),
        'sftp_username': os.environ.get('SFTP_USERNAME', ''),
        'sftp_password': os.environ.get('SFTP_PASSWORD', '')
    },

    'revenue': {
        'bing': {
            'creds': {  # actual local path to /opt/bing/creds
                'username': os.environ.get('REVENUE_BING_USERNAME', ''),
                'password': os.environ.get('REVENUE_BING_PASSWORD', ''),
                'developer_token': os.environ.get('REVENUE_BING_DEVELOPER_TOKEN', ''),
                'content_type': 'application/json'
            },
            'config': {
                'distribution':
                    {  # actual local path to /opt/bing/config
                        'report_name': 'Distribution performance report',
                        'report_type': 'Distribution',
                        'granularity': 'Day',
                        'columns': ['DistributionPartnerCode', 'FormCode', 'Clicks', 'BiddedSRPVs', 'RawSRPVs',
                                    'EstimatedRevenue', 'Market', 'Language',
                                    'DeviceType', 'Currency', 'Impressions', 'AdImpressions', 'AdImpressionYield',
                                    'RPM', 'CPC', 'ClickYield', 'AdCTR', 'Coverage',
                                    'AdDensity', 'CTR', 'BiddedCTR', 'UserCountry', 'WebSiteCountry', 'WebSiteLanguage']
                    },
                'partner_tag':
                    {  # actual local path to /opt/bing/config
                        'report_name': '',  #
                        'report_type': '',
                        'granularity': '',
                        'columns': ['DistributionPartnerCode', 'FormCode', 'Clicks', 'BiddedSRPVs', 'RawSRPVs',
                                    'EstimatedRevenue', 'Market', 'Language',
                                    'DeviceType', 'Currency', 'Impressions', 'AdImpressions',
                                    'AdImpressionYield',
                                    'RPM', 'CPC', 'ClickYield', 'AdCTR', 'Coverage',
                                    'AdDensity', 'CTR', 'BiddedCTR', 'UserCountry', 'WebSiteCountry',
                                    'WebSiteLanguage']
                    }
            }
        }
    }
}
