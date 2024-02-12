#!/usr/bin/env python3

import click

from addResult import addResult
from createUsers import createUsers
from importResults import importResults
from populateGames import populateGames
from runSolver import runSolver
from telegramBot import telegramBot


@click.group()
@click.option("--base-url", help="The base URL for the API", required=True)
@click.option("--debug/--no-debug", default=False, help="Debug")
@click.pass_context
def cli(ctx, base_url, debug):
    ctx.ensure_object(dict)

    ctx.obj["BASE_URL"] = base_url
    ctx.obj["DEBUG"] = debug


cli.add_command(addResult)
cli.add_command(createUsers)
cli.add_command(importResults)
cli.add_command(populateGames)
cli.add_command(runSolver)
cli.add_command(telegramBot)

if __name__ == "__main__":
    cli(obj={})
