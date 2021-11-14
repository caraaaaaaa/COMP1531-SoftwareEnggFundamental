import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
from flask import Flask, request
import requests

# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "simple.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

#def test_empty(url):
#    buffer = erquests.get(f"{url}/names")
#    dic = buffer.json()
#    assert dic == {"names":[]}

def test_add(url):
    json_data = {"name": "Cara"}
    requests.post(f"{url}/name/add", json=json_data)
    buffer = requests.get(f"{url}/names")
    dic = buffer.json()

    assert (json_data.get("name") in dic.get("names"))

def test_delete(url):
    json_data = {"name": "Cara"}
    requests.delete(f"{url}/name/remove", json=json_data)
    buffer = requests.get(f"{url}/names")
    dic = buffer.json()

    assert (json_data.get("name") not in dic.get("names"))