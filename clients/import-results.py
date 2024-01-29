#!/usr/bin/env python3

import click
import csv
import requests
import sys

import http.client as http_client
import logging

from pprint import pprint


def resultPresent(base_url, game, user):
    results = requests.get(f"{base_url}/games/{game}/results").json()["gameresults"]

    found = list(filter(lambda result: result["user"] == user, results))
    return len(found) != 0


def postResult(base_url, game, user, guesses, failure):
    if not resultPresent(base_url, game, user):
        gameResult = {
            "user": user,
        }

        if len(failure) == 0:
            gameResult["guesses"] = guesses
            gameResult["success"] = 1
        else:
            gameResult["guesses"] = failure if failure.isnumeric() else 0
            gameResult["success"] = 0

        url = f"{base_url}/games/{game}/results"

        response = requests.post(url, json=gameResult)
        print(f"{game}, user: {gameResult['user']}: {response.status_code}")
        if response.status_code != 200:
            pprint(gameResult)
            print(f"\t: {response.text}")
            sys.exit()


@click.command()
@click.option("--base-url", help="The base URL for the API", required=True)
@click.option("--csv-file", help="The name of the CSV file to import", required=True)
@click.option("--debug/--no-debug", default=False, help="Debug")
def importResults(base_url, csv_file, debug):
    # http_client.HTTPConnection.debuglevel = 1

    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    with open(csv_file) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=",")
        First = True
        for row in csvReader:
            if First:
                header = row
                First = False
            else:
                if len(row[0]):
                    if len(row[1]) or len(row[2]):
                        postResult(base_url, row[0], 1, row[1], row[2])
                    if len(row[7]) or len(row[8]):
                        postResult(base_url, row[0], 2, row[7], row[8])
                    # if len(row[3]) or len(row[4]):
                    #     postResult(base_url, row[0], 3, row[3], row[4])
                    # if len(row[5]) or len(row[6]):
                    #     postResult(base_url, row[0], 4, row[5], row[6])


if __name__ == "__main__":
    importResults()
