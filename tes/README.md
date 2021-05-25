#  <img src="https://git.rockfin.com/servicing-sre/terratattle/blob/master/web/static/terraform.png" width="50" height="50"> Terratattle  

Python application that utilizes the GitHub API to crawl GitHub organizations for out-of-date/deprecated Terraform modules.

:sparkles: https://shorty/terratattle :sparkles:

## Table of Contents

- [Features](#features)
- [CLI](#cli)
  - [Install](#install)
  - [Configuration](#configuration)
- [CircleCI](#circleci)
  - [2.0](#20)
  - [2.1](#21)
- [WebApp](#webapp)
  - [API](#api)

## Features

* Finds out-of-date modules:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/outdated.png)]()

* Finds up-to-date modules:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/updated.png)]()

* Finds modules not using a release:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/no-ref.png)]()

* Finds modules using placeholder versions:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/no-release.png)]()

* Finds in-line/custom modules:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/in-line.png)]()

* Finds deprecated modules from the terraform-emerging organization:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/terraform-emerging.png)]()

* Finds deprecated modules from the tf-modules organization:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/tf-modules.png)]()

* Finds modules that have been archived:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/terraform-archive.png)]()

* Finds modules not in the official terraform organization:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/unofficial.png)]()

* Generates reports:

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/report.png)]()

## CLI

### Requirements

* Python 3
  * [requirements.txt](requirements.txt)

### Install

```
python3 -m venv terratattle      # make a virtualenv named `terratattle`
. terratattle/bin/activate       # activate the virtualenv
pip3 install -r requirements.txt # install the dependencies
```

### Configuration

1. Set ENV variables:

> **TOKEN** is your GitHub [Personal access token](https://git.rockfin.com/settings/tokens).  
> **ORG** is the GitHub User/Organization you want to crawl.   

```
export TOKEN=example && export ORG=example
```

2. Make application executable:

```
chmod +x terratattle.py
```

3. Run application:

```
python terratattle.py
```

### HTML reports

> Change **$ORG** with a valid GitHub organization (example: **servicing-sre**).  
> This will generate an HTML report in your HOME directory.  

```
export ORG=$ORG && python terratattle.py | ansi2html > ~/$ORG.html
```

### JSON output

> You can run Terratattle with the **--output** flag set to *json* to get a more app-friendly report.
> This will generate a JSON report in your HOME DIR.

```
export ORG=$ORG && python terratattle.py --output=json > ~/$ORG.json
```

### Repo mode

> You can run Terratattle with the **--repo** flag set to run at the repository level instead of the organization level.  
> **NOTE:** You will also need to provide an additional **REPONAME** ENV value!  

```
export REPONAME=$REPONAME && python terratattle.py --repo
```

### Search mode

> You can run Terratattle with the **--search** flag to search all of Git Enterprise for a module.  
> **NOTE:** You will also need to provide an additional **MODULE** ENV value!  

```
export MODULE=$MODULE && python terratattle.py --search
```

### Audit mode 

> You can run Terratattle with the **--audit** flag to search all of Git Enterprise for a module and audits that the version is greater than a minimum.  
> **NOTE:** You will also need to provide the additional **MODULE** & **MODULE_VERS** ENV values!  

```
export MODULE=MODULE && export MODULE_VERS=X.X.X && python terratattle.py --audit
```

## CircleCI

You can run Terratattle with the **--circleci** flag in your CircleCI pipelines to scan for out of date Terraform modules in your CI/CD pipeline.  This will update *Terratattle* to run at the repository level instead of the organization level.  It will scan for **terraform.tfvars** files in the GitHub repo containing the **config.yml** running the CircleCI pipeline.  This will catch out of date Terraform modules if your infrastructure as code is stored with your application code.  For instance in a *infrastructure/* directory with your code.  

```
./terratattle.py --circleci
```

*Example [CircleCI Job](https://circleci.foc.zone/gh/servicing-sre/terratattle/1)*  

### 2.0

*Example config.yml*:  

```
version: 2
jobs:
  build:
    docker:
      - image: circleci/python:3.6.1

    steps:
      - run:
          name: terratattle
          command: |
            git clone https://git.rockfin.com/servicing-sre/terratattle .
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
            python terratattle.py --circleci
```

#### Nightly Workflows

You can run Terratattle on a nightly schedule:  

> **NOTE:** cron time is *UTC-5*, this example runs midnight *EST*

```
version: 2
jobs:
  build:
    docker:
      - image: circleci/python:3.6.1

    steps:
      - run:
          name: terratattle
          command: |
            git clone https://git.rockfin.com/servicing-sre/terratattle .
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
            python terratattle.py --circleci
            
workflows:
  version: 2
  pipeline:
    jobs:
      - build
  nightly:
    triggers:
      - schedule:
          cron: "0 4 * * *"
          filters:
            branches:
              only:
                - master
    jobs:
      - build
```

### 2.1

> **NOTE:** to use CircleCI 2.1 features you will need to follow: https://docs.hal.foc.zone/configuring-circle-ci/using-orbs/

**Official Orb:** https://circleci.com/developer/orbs/orb/terratattle/terratattle-orb  

*Example config2.1.yml*:  

```
version: 2.1
orbs:
  terratattle-orb: terratattle/terratattle-orb@2.0.0

workflows:
  use-my-orb:
    jobs:
      - terratattle-orb/terratattle:
            github-url: git.rockfin.com
```      

## WebApp 

https://shorty/terratattle

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/web.png)]()
[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/results.png)]()

### API

Example: https://terratattle.rms.servicing.foc.zone/api?org=servicing-sre

[![](https://git.rockfin.com/servicing-sre/terratattle/blob/master/img/api.png)]()

[![]()]()
