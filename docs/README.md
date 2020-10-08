# sync
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-sync/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.01-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Windows-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/sync)

## Description
Sync losts of projects.
![](./sync.png)

## Goals
 - [x] Clone files segnalized in local.csv
 - [x] Add the sync in cloud option
 - [x] Add repo WebSite

## Required
 - python3
 - pip3 packages (in repo core ```pip install -r requirements\requirements.txt```)
 - setup file_to_upload_and_where.csv
 
## Directories structure
 - .github
   - ISSUE_TEMPLATE
     - bug_report.md
     - feature-request.md
 - bin
   - **sync.bat**
   - **sync.py**
 - docs
   - _config.yml
   - LICENSE
   - README.md
   - sync.png
 - flussi
   - cloned
     - ... <- auto created
   - file_to_upload_and_where.csv <- ***need setup***
 - log
   - trace.log
 - requirements
   - requirements.txt
   
### Execution examples (in bin folder)
 - python3 sync.py
 - .\sync.bat

# Changelog
 - [Version_01.01-2020-10-08](#Version_0101-2020-10-08)

## Version_01.01-2020-10-08
 - Clone files segnalized in local.csv
 - Fixed a bug
 - Add the sync in cloud option
 - Add repo WebSite

---
Made by Castellani Davide 
If you have any problem please contact me:
- help@castellanidavide.it
- [Issue](https://github.com/CastellaniDavide/sync/issues)
