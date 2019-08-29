FROM google/cloud-sdk

COPY . /workspace/

WORKDIR /workspace

RUN apt-get update && apt-get install python3                             \
    && apt-get install python3-pip -y                                     \
    && apt-get install unzip -y                                           \
    && apt-get install lftp -y                                            \
    && pip3 install --upgrade --no-cache-dir .  \
    && pip3 install git+https://github.com/mozilla-it/salesforce-fetcher

#
