#!/usr/bin/env python3

import requests
import click

import http.client as http_client
import logging

import sys

from pprint import pprint


def findUser(base_url, user):
    users = requests.get(f"{base_url}users").json()["users"]
    foundUsers = list(filter(lambda checkUser: checkUser["username"] == user, users))
    return foundUsers[0] if foundUsers else None


def storeResult(base_url, game, user, numGuesses, success):
    url = f"{base_url}/games/{game}/results"

    gameResult = {
        "user": user,
        "game": game,
        "guesses": numGuesses,
        "success": 1 if success else 0,
    }

    result = requests.post(url, json=gameResult)


def checkSuccess(ctx, param, value):
    if value and ctx.params["guesses"] == -1:
        click.echo("When success is specified, guesses is required")
        ctx.exit(1)

    return value


@click.command()
@click.option("--base-url", help="The base URL for the API", required=True)
@click.option("--user", help="The user the result applies to", required=True)
@click.option("--game", help="The game number", required=True)
@click.option("--guesses", default=-1, is_eager=True, help="The number of guesses")
@click.option(
    "--success",
    type=bool,
    callback=checkSuccess,
    help="Whether the game was successful",
)
@click.option("--debug/--no-debug", default=False, help="Debug")
def addResult(base_url, user, game, guesses, success, debug):
    # http_client.HTTPConnection.debuglevel = 1

    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    userDetails = findUser(base_url, user)
    if userDetails:
        storeResult(base_url, game, userDetails["id"], guesses, success)
    else:
        print(f"Invalid user {user}")
        sys.exit(1)


if __name__ == "__main__":
    addResult()
