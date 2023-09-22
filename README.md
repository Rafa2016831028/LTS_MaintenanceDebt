# LTS_MaintenanceDebt

The core intent of the project is to identify the maintenance trend of LTS support, to pinpoint how they are safeguarding the existing users of the targeted release.

The pipeline of analysis is described in the following picture:


![git_flow](https://github.com/joydeba/InconsistentLinking/blob/main/Image/methodology.png)

# Clone it by - 
    - git clone https://github.com/Rafa2016831028/LTS_MaintenanceDebt.git
     - if password is not working, use PAT

# Virtual environment 
    - python3 -m venv . venvINCON
    - source bin/activate [for locations]

# Required packages
    - pip/pip3 install PyGithub
    - pip3 install pytz
    - pip3 install GitPython 
    - brew install gh

# Research Question
1. Are the effort of safeguarding the releases prone to introducing quality debt to the target release?
2. How does quality debt evolve in release lifecycle?
3. When and why do developers induce new technical debt in LTS support?

# Links
![Github 2017 survey](https://opensourcesurvey.org/2017/)

# Install
 ![gh api](https://cli.github.com/manual/gh_api)
 
 # Data retrieve
 - gh repo list eclipse -L 300 > eclipse.csv
