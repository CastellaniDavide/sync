# sync
[![GitHub license](https://img.shields.io/badge/licence-GNU-green?style=flat)](https://github.com/CastellaniDavide/cpp-sync/blob/master/LICENSE) ![Author](https://img.shields.io/badge/author-Castellani%20Davide-green?style=flat) ![Version](https://img.shields.io/badge/version-v01.03-blue?style=flat) ![Language Python](https://img.shields.io/badge/language-Python-yellowgreen?style=flat) ![sys.platform supported](https://img.shields.io/badge/OS%20platform%20supported-Windows-blue?style=flat) [![On GitHub](https://img.shields.io/badge/on%20GitHub-True-green?style=flat&logo=github)](https://github.com/CastellaniDavide/sync) ![Sync test](https://github.com/CastellaniDavide/sync/workflows/Sync%20test/badge.svg)

## Description
Sync losts of projects.
![](./sync.svg)

## Goals
 - [x] Clone files segnalized in local.csv
 - [x] Add the sync in cloud option
 - [x] Add repo WebSite
 - [x] Added GitHub Action
 - [x] Change sync.py
 - [x] Added .gitignore to don't save log file(s)
 - [x] Made the two options (agent or agentless)

## Required
 - python3
 - pip3 packages (in repo core ```pip install -r requirements\requirements.txt```)
 - setup file_to_upload_and_where.csv & settings.json
 
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
   - settings.json <- ***need setup***
 - log
   - trace.log
 - requirements
   - requirements.txt
 - .gitignore
   
### Execution examples (in bin folder)
 - python3 sync.py
 - .\sync.bat

# Changelog
 - [Version_01.03_2021-01-14](#Version_0103_2021-01-14)
 - [Version_01.02-2020-12-20](#Version_0102-2020-12-20)
 - [Version_01.01-2020-10-08](#Version_0101-2020-10-08)

## Version_01.03_2021-01-14
 - Optimized log

## Version_01.02-2020-12-20
 - Added GitHub Action for Agent and Agentless
 - Change sync.py
 - Optimize sync.bat: added the possibility to pass the args to python file
 - Update README.md
 - Added .gitignore to don't save log file(s)
 - Added demo files to mantain the folders when upload to 

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
