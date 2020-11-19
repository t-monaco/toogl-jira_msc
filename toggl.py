import json
import re
import requests
from datetime import date, timedelta
import sys
from colorama import Fore
from config import *
# from pprint import pprint


# TODO:
#  - Prepare data to upload to google sheet
#  - Make more flexible _TaskType_ value

def main():
    today_date = str(date.today().strftime("%Y-%m-%dT%H:%M:%SZ"))
    tomorrow_date = str((date.today() + timedelta(days=1)
                         ).strftime("%Y-%m-%dT%H:%M:%SZ"))
    yesterday_date = str((date.today() + timedelta(days=-1)
                          ).strftime("%Y-%m-%dT%H:%M:%SZ"))

    if '--yesterday' in sys.argv:
        toggl_raw_data = get_toggl_time_entries_json(yesterday_date, today_date)
    else:
        toggl_raw_data = get_toggl_time_entries_json(today_date, tomorrow_date)

    united_dataset, not_united_dataset = process_data(toggl_raw_data)

    for key, united_item in enumerate(united_dataset):
        print(united_item)
        print(f'{Fore.YELLOW}Uploading item {key + 1} of {len(united_dataset)}...')
        jira_response = upload_data_to_jira(united_item)
        toggl_response = update_toggl_time_entry(united_item)


def get_toggl_time_entries_json(initial_date, final_date):
    url = f"{TOGGL['url']}/time_entries?start_date={initial_date}&end_date={final_date}"
    x = requests.get(url, auth=(
        TOGGL['API_token'], 'api_token'))
    res = json.loads(x.text)

    # This was made for updating spreadsheet -> future development
    # for entry in response:
    #     entry['ORG'] = 'W
    return res


def process_data(data):
    united = []
    not_united = []
    issue_id_regex = r"((UMP|MMP)-\d{4})\s"

    for item in data:
        issue_id = re.search(issue_id_regex, item.get('description', ''))
        if issue_id and 'onJira' not in item.get('tags', ''):
            item['issue_id'] = issue_id.group(1)
            # item['duration'] = str(round(int(item['duration']) / 3600, 1))
            item['description'] = re.sub(issue_id_regex, '', item['description'])
            united.append(item)
        else:
            not_united.append(item)

    return [united, not_united]


def upload_data_to_jira(item):
    payload = {
        'timeSpentSeconds': item.get('duration'),
        'dateStarted': item.get('start'),
        # Remove the Jira issue from the copy
        'comment': item.get('description'),
        'author': {
            'name': JIRA['usr']
        },
        'issue': {
            'key': item.get('issue_id')
        },
        'worklogAttributes': [{
            'key': '_TaskType_',
            'value': 'DEVELOPMENT: BACK END'
        },
            {
                'key': '_Round_',
                'value': 'InternalActivity'
            }
        ]
    }

    header = {'content-type': 'application/json',
              'Authorization': JIRA['API_token']}

    try:
        res = requests.post(
            url=f"{JIRA['url']}/rest/tempo-timesheets/3/worklogs/",
            data=json.dumps(payload),
            headers=header)
        if res.status_code == 200:
            print(f'{Fore.GREEN}UPLOADED SUCCESSFULLY')
            if 'tags' in item.keys():
                item['tags'].append('onJira')
            else:
                item['tags'] = ['onJira']
        return res
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def update_toggl_time_entry(time_entry):
    payload = {
        'time_entry': {
            'tags': time_entry['tags']
        }
    }

    res = requests.put(
        url=f"{TOGGL['url']}/time_entries/{time_entry['id']}",
        data=json.dumps(payload),
        auth=(TOGGL['API_token'], 'api_token'),
        headers={'content-type': 'application/json'}
    )

    return res


main()
