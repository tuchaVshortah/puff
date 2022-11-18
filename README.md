
# Puff

Yet another passive subdomain enumeration tool written in Python from scratch.



## Badges

[![MPL 2.0 License](https://img.shields.io/badge/License-MPL%202.0-green.svg)](https://choosealicense.com/licenses/mpl-2.0/)


## Features

- Get subdomains from multiple sources 
- Several formats of output
- Multithreading
- Cross platform


## Subdomain sources

 - [subdomains.whoisxmlapi.com](https://subdomains.whoisxmlapi.com/api/)
 - [crt.sh](https://crt.sh/)
 - [urlscan.io](https://urlscan.io)
 - [otx.alienvault.com](https://otx.alienvault.com/api)
 - [jonlu.ca (Anubis-DB)](https://jonlu.ca/anubis/)
## Requirements

 - [subdomains-lookup](https://pypi.org/project/subdomains-lookup/)
 - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
 - [requests](https://pypi.org/project/requests/)


## Run Locally

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


## Usage/Examples

Parse in multithreading mode and list all subdomains of the specified domain:

```bash
python puff.py -d google.com -b
<subdomain>.google.com
<subdomain>.google.com
<subdomain>.google.com
...
```

Parse, list and save all subdomains of the specified domain to the given file:

```bash
python puff.py -d google.com -f subdomains.google.txt
<subdomain>.google.com
<subdomain>.google.com
<subdomain>.google.com
...
```
Parse in multithreading and save all subdomains of the specified domain without showing output:

```bash
python puff.py -d google.com -f subdomains.google.txt -b -q
```

Parse and output all subdomains of the specified domain in JSON format:

```bash
python puff.py -d google.com -j
{
    "search": "google.com",
    "result": {
        "count": 10000,
        "records": [
            {
                "domain": "<subdomain>.google.com",
                "firstSeen": 0123456789,
                "lastSeen": 0123456789
            },
            {
                "domain": "<subdomain>.google.com",
                "firstSeen": 0123456789,
                "lastSeen": 0123456789
            },
            ...
        ]
    }
}
```

Parse and output all subdomains of the specified domain in XML format:

```bash
python puff.py -d google.com -x
<?xml version="1.0" ?>
<xml>
	<search>google.com</search>
	<result>
		<count>10000</count>
		<records>
			<record>
				<domain><subdomain>.google.com</domain>
				<firstSeen>0123456789</firstSeen>
				<lastSeen>0123456789</lastSeen>
			</record>
			<record>
				<domain><subdomain>.google.com</domain>
				<firstSeen>0123456789</firstSeen>
				<lastSeen>0123456789</lastSeen>
			</record>
            ...
        </records>
	</result>
</xml>

```
## Roadmap

- Add an option to check for alive domains

- ~Multithreading~ *Done!*

- Beautiful README

- Beautiful code

- ~Divide the code base into several files/modules~ *Done!*

- Beautiful --help page 

- Comprehensive documentation

- Add functionality to parse another resources *In progress*

- ~Create requirements.txt~ *Done!*

- Configurability

- Add functionality to log events happening while Puff is running

- ~Convenient usage in scripts~ *Done!*


## FAQ

#### What does Puff do?

Puff parses [subdomains.whoisxmlapi.com](https://subdomains.whoisxmlapi.com/api/),
[crt.sh](https://crt.sh/), [urlscan.io](https://urlscan.io), 
[otx.alienvault.com](https://otx.alienvault.com/api) and [jonlu.ca (Anubis-DB)](https://jonlu.ca/anubis/) 
to get information about subdomains of the target domain.

#### How many output formats are supported?

Currently, three output formats are supported: **JSON**, **XML** and **TXT**. **TXT** 
is a regular text format where subdomains are listed one per line wihtout any additional 
information to make usage in scripts easier.

#### How fast it is?

It will run in multiple threads if the -b or --boost flag is set, 
so the internet connection speed may be the bottleneck.


## Authors

- [@tuchaVshortah](https://github.com/tuchaVshortah)

