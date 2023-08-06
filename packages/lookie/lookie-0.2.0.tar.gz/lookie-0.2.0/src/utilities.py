import datetime
import logging
import json
import os
import http.client
from urllib.parse import urlparse


def date_time_now():
    to_return = datetime.datetime.utcnow().isoformat()
    return to_return


def display(message):
    logging.log(level=1, msg=message)
    to_print = f'{message}'
    print(to_print)
    return True


def get_path():
    default_path = str(os.getcwd())
    return default_path


def config_reader():
    try:
        with open(file=get_path() + "/" + "lookie.config.json", mode='r') as cf:
            lookie_config = json.load(cf)
            return lookie_config
    except Exception:
        return {}


def send_message_to_slack(message):
    slack_config = config_reader().get("slack")
    if not slack_config:
        return False

    slack_url = urlparse(slack_config.get("hook"))
    slack_channel = urlparse(slack_config.get("channel"))

    conn = http.client.HTTPSConnection(slack_url.netloc)

    the_data = {
        "channel": slack_channel,
        "text": message
    }

    headers = {'Content-Type': "application/json"}

    conn.request("POST", slack_url.path, json.dumps(the_data), headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
