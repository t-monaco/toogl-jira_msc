# Toggl to JIRA MSC
The purpose of this repo is to speed up the process of uploading your working hours to JIRA.  Its functionality is to get your tracked hours from the [TOGGL](https://toggl.com/) app, process the data, and upload them to JIRA.

There are some steps you need to follow in order to successfully upload your data your JIRA.
* Your time tracks on TOGGL **must** start with the JIRA ticket number. A regex will look the ticket number on the time track's description and split the result. The found number will be your issue_id and the rest will be uploaded as description.

Additionally, this script was created in order to be executed (manually) EOD. It means, that by default will upload your working hours of the current day.
## Set up
1. Install requirements.txt packages
```bash
pip3 install -r requirements.txt
```
2. Copy `config.sample.py` and set your credentials, and your JIRA MSC URL
```bash
cp config.sample.py config.py
``` 

## Execution
Run the following cmd
```bash
python3 toggl.py
``` 
If for some reason you forgot to upload your hours from the day before, run the same command with the `--yesterday` flag.
```bash
python3 toggl.py --yesterday
```

Furthermore, there is a flag to upload all the remaining hours, that has no **"OnJira"** tag, with an specific time frame. The flag `--custom` with the desire time frame `yyyy-mm-dd`. First the `initial_date`, follow by the `end_date`, with space in between. The time tracks of the end date are omitted, this means that the time tracks that will be uploaded are from the `initial_date` to `end_date - 1.`
```
python3 toggl.py --custom 2021-01-01 2021-01-14
```

## Disclaimer
This script was created for personal uses, so it might not work for everyone's workspace. However, it can be modified for each different situation.