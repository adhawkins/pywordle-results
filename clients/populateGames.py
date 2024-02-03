#!/usr/bin/env python3

import requests
import click
import datetime
import json

from pprint import pprint


def gameInDatabase(date, games):
    result = list(
        filter(lambda game: datetime.date.fromisoformat(game["date"]) == date, games)
    )
    return len(result) != 0


def debugPrint(message, debug):
    if debug:
        click.echo(message)


@click.command()
@click.pass_context
def populateGames(ctx):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    basicAuth = requests.auth.HTTPBasicAuth("andy", "testing")

    games = requests.get(f"{base_url}/games", auth=basicAuth).json()["games"]

    gameDate = datetime.date(2021, 6, 19)
    endDate = datetime.date.today()

    while True:
        gameURL = f"https://www.nytimes.com/svc/wordle/v2/{gameDate}.json"

        if gameInDatabase(gameDate, games):
            debugPrint(f"{gameDate} already present", debug)
        else:
            gameResponse = requests.get(gameURL, auth=basicAuth)
            if gameResponse.status_code == 200:
                gameJSON = gameResponse.json()

                gameData = {
                    "id": (
                        gameJSON["days_since_launch"]
                        if "days_since_launch" in gameJSON
                        else 0
                    ),
                    "date": gameJSON["print_date"],
                    "solution": gameJSON["solution"],
                }

                response = requests.post(
                    f"{base_url}/games", json=gameData, auth=basicAuth
                )
                print(f"{gameDate}: {response.status_code}")

        gameDate += datetime.timedelta(days=1)
        if gameDate > endDate:
            break


if __name__ == "__main__":
    populateGames()
