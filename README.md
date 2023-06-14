# Vaccine

Although there may not be an exact way to automatize SQL injections, the purpose of this project is trying to attack the most common ways of vulnerable inputs in order to recover information and data from the database.

## Description

We all know how important secure programming is.
SQL Injection is the injection of SQL commands to alter the behaviour of a program and execute commands on the database.
In this project we create a tool that is able to detect SQL injections providing a URL.

The tool has a battery of tests to run against a given URL and is able to detect SQL injections.
It can detect the type of database engine to make the tests more successful.
The tests are based on several types: union, error, boolean.

In case a website is confirmed to be vulnerable, the following is obtained:

- The vulnerable parameters.
- The payload used.
- Database names.
- Table names.
- Column names.
- Complete database dump.

The tool has some storage file for the data, if it does not exist it will be created on the first run.

## Prerequisites

- bs4~=0.0.1
  - beautifulsoup4~=4.12.2
    - soupsieve~2.4.1
- lxml~=4.9.2
- requests~=2.31.0
  - certifi~=2023.5.7
  - charset-normalizer~=3.1.0
  - idna~=3.4
  - urllib3~=2.0.2

## Usage

Vaccine performs SQL injection by providing a URL as a parameter.
The program manages the following options:

```bash
vaccine [-oP] URL
```

- Option -o: Archive file, if not specified it will be stored in a default one.
- Option -X : Type of request, if not specified GET will be used.

## Credits

42 Málaga Cybersecurity Bootcamp

- josesanc02
- jmorillo42
