#!/usr/bin/env python3

import requests
import click

import http.client as http_client
import logging

from pprint import pprint

import SolveForWord

basicAuth = requests.auth.HTTPBasicAuth("andy", "testing")


def resultExists(results, game, user):
    found = list(filter(lambda result: result["user"] == user["id"], results))
    return len(found) != 0


def storeResult(base_url, game, user, guesses):
    url = f"{base_url}/games/{game}/results"

    result = {
        "user": user,
        "game": game,
        "guesses": len(guesses),
        "success": 1 if len(guesses) <= 6 else 0,
    }

    result = requests.post(url, json=result, auth=basicAuth).json()["gameresult"]

    guessNumber = 1

    guessURL = f"{base_url}/games/{game}/results/{result['id']}/guesses"

    for guess in guesses:
        guessData = {
            "guess_num": guessNumber,
            "guess": guess.Guess(),
            "result1": str(guess.Matches()[0].value),
            "result2": str(guess.Matches()[1].value),
            "result3": str(guess.Matches()[2].value),
            "result4": str(guess.Matches()[3].value),
            "result5": str(guess.Matches()[4].value),
        }

        guessResult = requests.post(guessURL, json=guessData, auth=basicAuth)

        guessNumber += 1


@click.command()
@click.option(
    "--words-list", help="The file name containing the list of words", required=True
)
@click.pass_context
def runSolver(ctx, words_list):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    # http_client.HTTPConnection.debuglevel = 1

    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    games = requests.get(f"{base_url}games", auth=basicAuth).json()["games"]

    users = [
        {
            "id": 3,
            "name": "New Solver",
            "matchType": SolveForWord.Word.tScoreType.eLetterValue,
        },
        {
            "id": 4,
            "name": "Old Solver",
            "matchType": SolveForWord.Word.tScoreType.eVowelsPreferred,
        },
    ]
    for game in games:
        results = requests.get(
            f"{base_url}/games/{game['id']}/results", auth=basicAuth
        ).json()["gameresults"]

        for user in users:
            if not resultExists(results, game["id"], user):
                print(f"Solving {game['date']} ({game['id']}) for {user['name']}")

                solver = SolveForWord.SolveForWord(
                    words_list, game["solution"], user["matchType"]
                )

                guesses = solver.Solve("")
                storeResult(base_url, game["id"], user["id"], guesses)


if __name__ == "__main__":
    runSolver()
