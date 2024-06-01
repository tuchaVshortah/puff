# puff

Yet another passive subdomain enumeration tool written in Python from scratch.


# Table of Contents

1. [Badges](#badges)
2. [Features](#features)
3. [Subdomain sources](#subdomain-sources)
4. [Requirements](#requirements)
5. [Run Locally](#run-locally)
6. [Usage examples](#usage-examples)
7. [Demos](#demos)
8. [FAQ](#faq)
9. [Roadmap](#roadmap)
10. [Authors](#authors)


## Badges

[![MPL 2.0 License](https://img.shields.io/badge/License-MPL%202.0-green.svg)](https://choosealicense.com/licenses/mpl-2.0/)


## Features

- Subdomains from multiple sources 
- JSON and regular output
- Multithreading
- Cross platform
- Rate-limiting evasion functionality
- Docker image


## Subdomain sources

 - [subdomains.whoisxmlapi.com](https://subdomains.whoisxmlapi.com/api/)
 - [crt.sh](https://crt.sh/)
 - [urlscan.io](https://urlscan.io/)
 - [otx.alienvault.com](https://otx.alienvault.com/api/)
 - [jonlu.ca (Anubis-DB)](https://jonlu.ca/anubis/)
 - [hackertarget.com](https://hackertarget.com/)
 - [dnsrepo.noc.org](https://dnsrepo.noc.org/)


## Requirements

 - [Python 3.11](https://www.python.org/)
 - [subdomains-lookup](https://pypi.org/project/subdomains-lookup/)
 - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
 - [requests](https://pypi.org/project/requests/)


## Run Locally
### Install with Git
Clone the project

```bash
git clone https://github.com/tuchaVshortah/puff.git
```

Go to the project directory

```bash
cd puff
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start puff

```bash
python puff.py -d <domain> --boost
```

### Install with Docker

```bash
docker pull tuchavshortah/puff:latest
```

## Usage examples

⚠️ ***Usage examples are provided for the Git installation. The Docker method is not recommended for daily driving. Use it if you are a developer.***

ℹ️ ***The same arguments can be used in the Docker installation.***  
Replace \"python puff.py\" with \"docker run --rm tuchavshortah/puff\" to run the Docker container.

❗***The -n flag limits the maximum amount of subdomains to probe. You may get less results than the specified number due to the fact that subdomains may be dead***

Parse remotes in multithreading mode and perform active scanning on 3 subdomains of the specified domain:

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> python puff.py -d google.com -b -a -n 3
Parsing sites...                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Completing concurrent.futures... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Preparing alive subdomains...    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
                                            Alive subdomains
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Number ┃ Subdomain                               ┃ Status code ┃           Title           ┃ Backend ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 1      │ pub-1556105567536871.afd.ghs.google.com │     404     │ Error 404 (Not Found)!!1  │     ghs │
│ 2      │ 36-98.docs.google.com                   │     200     │ Sign in - Google Accounts │     ESF │
└────────┴─────────────────────────────────────────┴─────────────┴───────────────────────────┴─────────┘
```

Parse in multithreading mode and save 3 subdomains in the subdomains.\<domain\>.\<format\> files:

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> python puff.py -d google.com -b -n 3 -a -df
Parsing sites...                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Completing concurrent.futures... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Preparing alive subdomains...    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
                                                                      Alive subdomains
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Number ┃ Subdomain                                                                                              ┃ Status code ┃     Title      ┃ Backend ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 1      │ o-o.preferreaccounts-ph.sn-35153iuxa-unxe.v9.lscache2.c.anaccounts-phroiaccounts-ph.clients.google.com │     404     │ Error 404 (Not │     N/A │
│        │                                                                                                        │             │   Found)!!1    │         │
└────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────┴────────────────┴─────────┘
```

❗***Functionality provided by the -n flag allows you to have a cleaner terminal while saving the full output to the specified file***  
_In the example below only 5 subdomains are outputted to the CLI, but all of the found subdomains were saved into the specified file._  
  
Parse, list and save all subdomains of the specified domain to the given file but limit the CLI output with 5 subdomains only:

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> python puff.py -d google.com -f subdomains.google.txt -n 5
Parsing sites...                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Preparing subdomains...          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
                                         Subdomains
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Number ┃ Subdomain                                                                       ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1      │ testing6.r4.sn-npoeenle.c.docs.google.com                                       │
│ 2      │ 13q8faa.feedproxy.ghs.google.com                                                │
│ 3      │ alt24468.xmpp.l.google.com                                                      │
│ 4      │ alt-0243.upload.google.com                                                      │
│ 5      │ payh2gjxuyyt2o3gsax5gcxri6d4nr7ts7xhepbxuxv3bxweuosa.mx-verification.google.com │
└────────┴─────────────────────────────────────────────────────────────────────────────────┘
```

Parse and output 5 subdomains of the specified domain in JSON:

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> python puff.py -d google.com -j -n 5
Parsing sites...                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[
  "jmcnamara.r1.sn-npoeenl7.c.docs.google.com",
  "pub-5461530528097278.afd.ghs.google.com",
  "e3bxooh7aamclbxgyf2c5vcxe64xt5dajflll5bp4denufti5rna.mx-verification.google.com",
  "google-proxy-74-125-211-40.google.com",
  "google-proxy-66-249-93-40.google.com"
]
```

## Demos

Number of found subdomains for [google.com](https://google.com/):

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> python puff.py -d google.com -b -v -n 0
Parsing sites...                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
10000 subdomains from whoisxmlapi.com
0 subdomains from crt.sh
5 subdomains from] urlscan.io
199 subdomains from otx.alienvault.com
5197 subdomains from jonlu.ca
136 subdomains from dnsrepo.noc.org
         Total unique subdomains: 15422
Preparing subdomains...          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

Multithreaded execution time:

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> Measure-Command { python puff.py -d google.com -b } | Select-Object TotalSeconds

TotalSeconds
------------
   9.4502747
```

Number of found subdomains for [yahoo.com](https://yahoo.com/):

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> python puff.py -d yahoo.com -b -v -n 0 
Parsing sites...                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
10000 subdomains from whoisxmlapi.com
0 subdomains from crt.sh
0 subdomains from] urlscan.io
254 subdomains from otx.alienvault.com
8232 subdomains from jonlu.ca
145 subdomains from dnsrepo.noc.org
         Total unique subdomains: 18320
Preparing subdomains...          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

Multithreaded execution time:

```powershell
(.venv) PS C:\Users\nuken\Projects\puff> Measure-Command { python puff.py -d yahoo.com -b } | Select-Object TotalSeconds 

TotalSeconds
------------
   9.8459897
```


## FAQ

#### What does puff do?

puff parses [subdomains.whoisxmlapi.com](https://subdomains.whoisxmlapi.com/api/),
[crt.sh](https://crt.sh/), [urlscan.io](https://urlscan.io), 
[otx.alienvault.com](https://otx.alienvault.com/api), 
[jonlu.ca (Anubis-DB)](https://jonlu.ca/anubis/), [hackertarget.com](https://hackertarget.com/) 
and [dnsrepo.noc.org](https://dnsrepo.noc.org/) to get information about subdomains of the target domain.

#### How many output formats are supported?

Currently, two output formats are supported: **JSON** and **TXT**.

#### How fast it is?

Very fast IMHO. However, your connection speed might be its bottleneck.

## Goals

- ✅ Add an option to check for alive domains

- Add a class named ConfigWrapper to make management of arguments easier and add support for config files

- Add a universal ConsoleWrapper class which will  manage output styles and options (such as --quiet)

- ✅ Multithreading 

- ✅ Good README

- Clean code

- ✅ Modular codebase

- ✅ Comprehensive --help page 

- Comprehensive documentation

- ✅ Parse data

- ✅ requirements.txt

- Configurability

- Logging

- ✅ Check alive subdomains

- ✅ Rate limiting evasion

- Caching

- Vulnerability searching 🧐

- Threat detection 🧐

- GUI 🧐

- Full information about the target

- Integrate paid APIs

- CI/CD 🧐?

- ✅ Github releases

- Sponsoring 🧐?


## Authors

- [@tuchaVshortah](https://github.com/tuchaVshortah)
