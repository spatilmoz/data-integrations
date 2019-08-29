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

### Best practices

Before merging a PR, we can use pylint which provides good static analysis in addition of PEP-8 recommendations provided by PyCharm. Not all recommendations must be followed but it improves the code readability. It includes stuff like variables rename and spacing and documentation.

Another recommendation would be to run coverage which provides a good summary about test coverage. Posting the output would let the team members know if your additions increased or decreased test coverage.

Also, when adding unit tests, it would be good to post output of a unit test run of all modules, this makes sure your PR does not break your or anybody else's unit tests before the actual commit and travis finds out that something broke on last commit.

Unit tests best practices:
  Unit Tests Should Be Trustworthy
  Unit Tests Should Be Maintainable and Readable
  Unit Tests Should Verify a Single-Use Case
  Unit Tests Should Be Isolated
  Unit Tests Should Be Automated
  Use a Good Mixture of Unit and Integration Tests
  Unit Tests Should Be Executed Within an Organized Test Practice
