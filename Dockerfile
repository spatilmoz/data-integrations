FROM google/cloud-sdk

RUN apt-get update && apt-get install python3                             \
    && apt-get install python3-pip -y                                     \
    && apt-get install unzip -y                                           \
    && apt-get install lftp -y                                            \
    && pip3 install git+https://github.com/mozilla-it/data-integrations   \
    && pip3 install git+https://github.com/mozilla-it/salesforce-fetcher@ade62b1750d354b9cbbc1a6b917f57ab816c3569
