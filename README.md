
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
 - [urlscan.io](https://urlscan.io/)
 - [otx.alienvault.com](https://otx.alienvault.com/api/)
 - [jonlu.ca (Anubis-DB)](https://jonlu.ca/anubis/)
 - [hackertarget.com](https://hackertarget.com/)
 - [dnsrepo.noc.org](https://dnsrepo.noc.org/)
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
## Demo/Speed test

Number of found subdomains for [google.com](https://google.com/):

```bash
python puff.py -d google.com -b | wc -l
16124
```

Multithreaded execution time:

```bash
time python puff.py -d google.com -b
<subdomain>.google.com
<subdomain>.google.com
<subdomain>.google.com
...

real    0m14.134s
user    0m4.919s
sys     0m0.085s
```

Number of found subdomains for [yahoo.com](https://yahoo.com/):

```bash
python puff.py -d yahoo.com -b | wc -l
20986
```

Multithreaded execution time:

```bash
time python puff.py -d yahoo.com -b
<subdomain>.yahoo.com
<subdomain>.yahoo.com
<subdomain>.yahoo.com
...

real    0m13.522s
user    0m7.334s
sys     0m0.079s
```
## FAQ

#### What does Puff do?

Puff parses [subdomains.whoisxmlapi.com](https://subdomains.whoisxmlapi.com/api/),
[crt.sh](https://crt.sh/), [urlscan.io](https://urlscan.io), 
[otx.alienvault.com](https://otx.alienvault.com/api), 
[jonlu.ca (Anubis-DB)](https://jonlu.ca/anubis/), [hackertarget.com](https://hackertarget.com/) 
and [dnsrepo.noc.org](https://dnsrepo.noc.org/) to get information about subdomains of the target domain.

#### How many output formats are supported?

Currently, three output formats are supported: **JSON**, **XML** and **TXT**. **TXT** 
is a regular text format where subdomains are listed one per line wihtout any additional 
information to make usage in scripts easier.

#### How fast it is?

It will run in multiple threads if the -b or --boost flag is set, 
so the internet connection speed may be the bottleneck.


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

- ~Add functionality to log events happening while Puff is running~ *Done!*

- ~Convenient usage in scripts~ *Done!*

- Add functionality to check wheter the retrieved subdomains' urls are valid or not


## Authors

- [@tuchaVshortah](https://github.com/tuchaVshortah)

