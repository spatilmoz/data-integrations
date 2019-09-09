FROM google/cloud-sdk

COPY . /workspace/

WORKDIR /workspace

RUN echo deb http://deb.debian.org/debian stable main >> /etc/apt/sources.list && \
    apt-get update && apt-get -y install python3 python3-pip unzip lftp && \
    pip3 install --upgrade --no-cache-dir .  && \
    pip3 install git+https://github.com/mozilla-it/salesforce-fetcher


