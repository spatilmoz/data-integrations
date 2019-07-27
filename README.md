# Data Integrations

[![Build Status](https://travis-ci.org/bowlofstew/data-integrations.svg?branch=master)](https://travis-ci.org/bowlofstew/data-integrations)

## Description

This code base provides tooling for integrating with data connectors. The 
currently supported data connectors are:
* [XMatters](./docs/XMATTERS.md)
* [Workday](./docs/WORKDAY.md)
* [BrickFTP](./docs/BRICKFTP.md)

## Building

[Prerequisites](./docs/PREREQUISITES.md)

### Setup

* `pipenv install -dev`
* `pipenv shell`

### Python

#### Setup Build

To build the Python binary distribution, execute the following command line statement 
in a terminal after meeting the project prerequisites:

`python setup.py build`

### Docker

To build the docker image, execute the following command line statement 
in a terminal after meeting the project prerequisites:

  `docker build -t mozilla/data-integrations .`

## Author(s)
