#!/usr/bin/env python3

import click
import csv
import requests

import http.client as http_client
import logging

from pprint import pprint

basicAuth = requests.auth.HTTPBasicAuth("andy", "testing")


def createUser(base_url, username, fullname):
    user = {"username": username, "fullname": fullname}

    response = requests.post(f"{base_url}/users", json=user, auth=basicAuth)
    print(f"user: {username}: {response.status_code}")


@click.command()
@click.option("--base-url", help="The base URL for the API", required=True)
@click.option("--debug/--no-debug", default=False, help="Debug")
def createUsers(base_url, debug):
    # http_client.HTTPConnection.debuglevel = 1

    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    createUser(base_url, "andy", "Andy Hawkins")
    createUser(base_url, "james", "James Marsh")
    createUser(base_url, "new", "New Solver")
    createUser(base_url, "old", "Old Solver")


if __name__ == "__main__":
    createUsers()
