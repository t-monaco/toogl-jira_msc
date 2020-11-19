import base64


def encode_jira_token():
    global JIRA
    temp_token = base64.b64encode(f"{JIRA['usr']}:{JIRA['pwd']}".encode()).decode()
    JIRA['API_token'] = f'Basic {temp_token}'


# SET YOUR CREDENTIALS HERE ########

JIRA = {
    "usr": "your_user",
    "pwd": "your_pass",
    "url": "intenal_jira_url"
}
TOGGL = {
    "API_token": "your_token",
    "url": "https://api.track.toggl.com/api/v8"
}

####################################

encode_jira_token()
