import http.client
import os
import subprocess
import time
import urllib.request
from src.utilities import display, send_message_to_slack as sml
import socket


def port_check(args):
    hostname = args.hostname
    surname = args.surname
    port = args.port

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(3)

    location = (hostname, port)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()

    if args.message:
        message = args.message.format(hostname=hostname, surname=surname, port=port)
    else:
        message = f"Port {port} of {hostname}/{surname} is accessible: Yes"

    if result_of_check == 0:
        display(message=message)
        return True
    else:
        message = message.replace("Yes", "No")
        display(message=message)
        sml(message=message)
        return False


def check_ping(hostname):
    """Check ping response of a host or IP."""
    res = subprocess.call(['ping', '-c', '1', '-W', '1000', hostname], stdout=open(os.devnull, 'wb'))
    if res == 0:
        """Ping ok"""
        return 1
    else:
        return 0


def ping_test(args):
    threshold = 80

    hostname = args.hostname
    surname = args.surname
    how_many_check = args.count
    interval = args.interval

    counter = 0

    for _ in range(how_many_check):
        ping_response = check_ping(hostname=hostname)
        counter += ping_response
        time.sleep(interval)

    percentage = int((counter / how_many_check) * 100)

    if args.message:
        message = args.message.format(hostname=hostname, surname=surname)
    else:
        message = f"Ping check to {hostname}/{surname} is ok: Yes"

    if percentage < threshold:
        message = message.replace("Yes", "No")
        display(message=message)
        sml(message=message)
    else:
        display(message=message)


def string_check(args):
    url = args.url
    surname = args.surname
    string = args.string

    if args.message:
        message = args.message.format(url=url, surname=surname, string=string)
    else:
        message = f"String - {string} found in {url} -- {surname}: Yes"

    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        chk = string.lower() in the_page.decode("utf-8").lower()
        print(the_page.decode("utf-8").lower())
        if string.lower() in the_page.decode("utf-8").lower():
            display(message=message)
            return True
        else:
            message = message.replace("Yes", "No")
            display(message=message)
            sml(message=message)
            return False

