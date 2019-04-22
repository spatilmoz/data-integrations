FROM google/cloud-sdk

RUN apt-get update && apt-get install python3                                                    \
    && apt-get install python3-pip -y                                                            \
    && apt-get install unzip -y                                                            \
    && apt-get install lftp -y                                                            \
    && pip3 install git+https://github.com/mozilla-it-data/data-integrations                     \
    && pip3 install git+https://github.com/mozilla-it-data/salesforce-fetcher@21029351b026374cddd1b2e7e8a3f261ab6b8f81
