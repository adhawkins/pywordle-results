#!/usr/bin/env python3

import logging
import requests
import click

import Token

import re
import tempfile
import os

import plotly.express as px

from telegram import Update, BotCommand
from telegram.constants import ChatMemberStatus, ChatType, ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    ChatMemberHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

base_url = ""
basicAuth = requests.auth.HTTPBasicAuth("andy", "testing")

blocks = [
    "\u2B1C\u2B1B",  # Black / white square
    "\U0001F7E8",  # Yellow square
    "\U0001F7E9",  # Green square
]

solvers = [3, 4]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)


def addGroup(group, title):
    url = f"{base_url}telegram_groups"

    print(f"Would add group '{title}' - {group} - url: '{url}'")

    telegramGroup = {
        "group": group,
        "title": title,
    }

    return requests.post(url, json=telegramGroup, auth=basicAuth)


def findGroup(group):
    url = f"{base_url}telegram_groups?groupid={group}"

    response = requests.get(url, auth=basicAuth)
    if response:
        foundGroups = response.json()["telegram_groups"]
        if len(foundGroups) == 1:
            return foundGroups[0]

    return None


def removeGroup(group):
    foundGroup = findGroup(group)

    if foundGroup:
        url = f"{base_url}telegram_groups/{foundGroup['id']}"

        response = requests.delete(url, auth=basicAuth)
        return response

    return None


def findUserWithTelegramID(telegramID):
    url = f"{base_url}users?telegramid={telegramID}"

    response = requests.get(url, auth=basicAuth)
    if response:
        foundUsers = response.json()["users"]
        if len(foundUsers) == 1:
            return foundUsers[0]

    return None


def findUserWithFullName(fullName):
    url = f"{base_url}users?fullname={fullName}"

    response = requests.get(url, auth=basicAuth)
    if response:
        foundUsers = response.json()["users"]
        if len(foundUsers) == 1:
            return foundUsers[0]

    return None


def setUserTelegramID(user, telegramID):
    print(f"Setting telegram ID for {user} to {telegramID}")

    userUpdate = {
        "username": user["username"],
        "telegram_id": telegramID,
        "fullname": user["fullname"],
    }

    response = requests.patch(
        f"{base_url}users/{user['id']}", auth=basicAuth, json=userUpdate
    )

    if response:
        return response.json()["user"]

    return None


def createUser(userName, telegramID, fullName):
    print(f"Creating user: {userName}, '{fullName}' - {telegramID}")

    user = {
        "username": userName,
        "telegram_id": telegramID,
        "fullname": fullName,
    }

    response = requests.post(f"{base_url}users", auth=basicAuth, json=user)

    if response:
        return response.json()["user"]

    return None


def getUser(userName, telegramID, fullName):
    # Check if a user exists with that telegram ID, if it does, use it
    user = findUserWithTelegramID(telegramID)
    if user:
        return user

    # If not, find a user whose full name matches
    user = findUserWithFullName(fullName)
    if user:
        # If that user doesn't have a telegram ID, update it and use it
        if user["telegram_id"] == 0:
            user = setUserTelegramID(user, telegramID)
            return user
        else:
            return None

    # Otherwise, create the user

    return createUser(userName, telegramID, fullName)


def addUserToGroup(group, user):
    group = findGroup(group)

    if group:
        url = f"{base_url}telegram_groups/{group['id']}/members"

        response = requests.post(url, auth=basicAuth, json={"user": user})


def removeUserFromGroup(group, user):
    group = findGroup(group)

    if group:
        url = f"{base_url}telegram_groups/{group['id']}/members?userid={user}"
        result = requests.get(url, auth=basicAuth)
        if result:
            members = result.json()["telegram_group_members"]

            if members:
                url = f"{base_url}telegram_groups/{group['id']}/members/{members[0]['id']}"

                result = requests.delete(url, auth=basicAuth)


def addGameResult(gameResult):
    url = f"{base_url}games/{gameResult['game']}/results"

    result = requests.post(url, json=gameResult, auth=basicAuth)

    if result:
        return result.json()["gameresult"]

    return None


def addGuess(game, resultID, guessNumber, result):
    guessURL = f"{base_url}games/{game}/results/{resultID}/guesses"

    guessData = {
        "guess_num": guessNumber,
        "num_words": 0,
        "guess": "",
        "result1": str(result[0]),
        "result2": str(result[1]),
        "result3": str(result[2]),
        "result4": str(result[3]),
        "result5": str(result[4]),
    }

    guessResult = requests.post(guessURL, json=guessData, auth=basicAuth)


def latestGameID():
    url = f"{base_url}games/latest"

    response = requests.get(url, auth=basicAuth)
    if response:
        game = response.json()["game"]
        return game["id"]

    return None


def fetchResultsForGame(game):
    results = requests.get(f"{base_url}games/{game}/results", auth=basicAuth)
    if results:
        return sorted(results.json()["gameresults"], key=lambda d: d["user"])

    return None


def fetchGroupMembers(telegramGroupID):
    group = findGroup(telegramGroupID)
    if group:
        results = requests.get(
            f"{base_url}telegram_groups/{group['id']}/members", auth=basicAuth
        )
        if results:
            members = []
            for member in results.json()["telegram_group_members"]:
                members.append(member["user"])

            return members

    return None


def fetchGuesses(gameID, resultID):
    results = requests.get(
        f"{base_url}games/{gameID}/results/{resultID}/guesses", auth=basicAuth
    )
    if results:
        return results.json()["guesses"]

    return None


def fetchAllResults():
    results = requests.get(f"{base_url}results", auth=basicAuth)
    if results:
        return results.json()["results"]

    return None


def fetchUser(userID):
    user = requests.get(f"{base_url}users/{userID}", auth=basicAuth)
    if user:
        return user.json()["user"]

    return None


async def botMembership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.chat.type == ChatType.GROUP:
        message = "What happened?"
        if (
            update.my_chat_member.new_chat_member.status
            == ChatMemberStatus.ADMINISTRATOR
            or update.my_chat_member.new_chat_member.status == ChatMemberStatus.MEMBER
        ):
            result = addGroup(
                update.my_chat_member.chat.id, update.my_chat_member.chat.title
            )
            message = f"Member status in group {update.my_chat_member.chat.title} ({update.my_chat_member.new_chat_member.status}) - {result.status_code}"

        elif update.my_chat_member.new_chat_member.status == ChatMemberStatus.LEFT:
            result = removeGroup(update.my_chat_member.chat.id)
            print(
                f"Left group {update.my_chat_member.chat.title} ({update.my_chat_member.chat.type}), result: {result.status_code}"
            )
            message = ""

        if message:
            try:
                await context.bot.send_message(
                    chat_id=update.my_chat_member.chat.id,
                    text=message,
                )
            except Exception as e:
                print(f"Exception: '{e}'")


async def groupMembership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("groupMembership")

    userName = update.chat_member.new_chat_member.user.username
    if not userName:
        userName = f"{update.chat_member.new_chat_member.user.first_name} {update.chat_member.new_chat_member.user.last_name}".lower().replace(
            " ", ""
        )

    user = getUser(
        userName,
        update.chat_member.new_chat_member.user.id,
        f"{update.chat_member.new_chat_member.user.first_name} {update.chat_member.new_chat_member.user.last_name}",
    )
    print(f"Found user: {user['username']}")

    if user:
        message = "What happened?"
        if (
            update.chat_member.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            or update.chat_member.new_chat_member.status == ChatMemberStatus.MEMBER
        ):
            message = f"Thank you for adding me to the '{update.my_chat_member.chat.title}' group."
            if update.my_chat_member.new_chat_member.status == ChatMemberStatus.MEMBER:
                message += " In order to track people joining or leaving the group, I need to be an Administrator of it. Please make me an Administrator of this group."
            else:
                message += " As an Administrator of the group I can now track people joining and leaving correctly."

            addUserToGroup(update.chat_member.chat.id, user["id"])
        elif update.chat_member.new_chat_member.status == ChatMemberStatus.LEFT:
            message = f"User {update.chat_member.new_chat_member.user.first_name} {update.chat_member.new_chat_member.user.last_name} left group {update.chat_member.chat.title} ({update.chat_member.chat.type})"

            removeUserFromGroup(update.chat_member.chat.id, user["id"])

        try:
            await context.bot.send_message(
                chat_id=update.chat_member.chat.id,
                text=message,
            )
        except Exception as e:
            print(f"Exception: '{e}'")


async def chatMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = findUserWithTelegramID(update.message.from_user.id)
    if user:
        addUserToGroup(update.message.chat.id, user["id"])

        lines = update.message.text.splitlines()

        firstLine = lines[0]

        match = re.search("^Wordle \d+ [\dX]\/\d\*?$", firstLine)
        if match:
            words = firstLine.split()
            numGuesses = words[2].split("/")

            del lines[0]

            guesses = []

            linesValid = True

            for line in lines:
                if line:
                    thisGuess = []
                    for char in line:
                        blockNum = 0

                        for block in blocks:
                            if char in block:
                                resultCode = blockNum
                                thisGuess.append(resultCode)

                            blockNum += 1

                    if len(thisGuess) == 5:
                        guesses.append(thisGuess)
                    else:
                        print(f"Invalid line length: {len(thisGuess)}")

                        linesValid = False
                        break

            if linesValid and (
                (numGuesses[0] == "X" and len(guesses) >= 6)
                or (numGuesses[0] != "X" and int(numGuesses[0]) == len(guesses))
            ):
                gameResult = {
                    "user": user["id"],
                    "game": words[1],
                    "guesses": numGuesses[0] if numGuesses[0] != "X" else 0,
                    "success": 1 if numGuesses[0] != "X" else 0,
                }

                result = addGameResult(gameResult)

                guessNumber = 1

                if result:
                    for guess in guesses:
                        addGuess(words[1], result["id"], guessNumber, guess)

                        guessNumber += 1

                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Wordle result for '{user['fullname']}' game {words[1]}: {numGuesses[0]}",
                    )
                except Exception as e:
                    print(f"Exception: '{e}'")

            else:
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"@{update.message.from_user.username}, that looked like a Wordle result, but I couldn't parse it properly",
                    )
                except Exception as e:
                    print(f"Exception: '{e}'")
    else:
        print(f"Can't find user with id {update.message.from_user.id}")


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 1:
        try:
            game = int(context.args[0])
        except ValueError:
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Invalid game number '{context.args[0]}'",
                )
            except Exception as e:
                print(f"Exception: '{e}'")

            return
    else:
        game = latestGameID()

    results = fetchResultsForGame(game)

    groupMembers = fetchGroupMembers(update.effective_chat.id)
    if groupMembers:
        groupMembers += solvers
    else:
        groupMembers = solvers

    response = ""
    if results:
        for result in results:
            if result["user"] in groupMembers:
                if response:
                    response += "\n"

                response += f"{result['userdetails.fullname']}\nWordle {game} "
                if result["success"]:
                    response += f"{result['guesses']}/6"
                else:
                    response += "X/6"

                response += "\n"

                guesses = fetchGuesses(result["game"], result["id"])
                if guesses:
                    guessNum = 1

                    response += "\n"
                    for guess in guesses:
                        if guessNum == 7:
                            response += "`===========================`\n"

                        response += f"`{guessNum:0>2}` \- {blocks[int(guess['result1'])][0]}{blocks[int(guess['result2'])][0]}{blocks[int(guess['result3'])][0]}{blocks[int(guess['result4'])][0]}{blocks[int(guess['result5'])][0]}"

                        if guess["num_words"] and guess["guess"]:
                            response += (
                                f" \- `{guess['num_words']:>5}` \- ||{guess['guess']}||"
                            )

                        response += "\n"
                        guessNum += 1

    if response:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=response,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except Exception as e:
            print(f"Exception: '{e}'")
    else:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"No results found for game {game}",
            )
        except Exception as e:
            print(f"Exception: '{e}'")


async def streaks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = fetchAllResults()

    if results:
        results.sort(key=lambda x: x["game"])

        groupMembers = fetchGroupMembers(update.effective_chat.id)
        if groupMembers:
            groupMembers += solvers
        else:
            groupMembers = solvers

        groupMembers.sort()

        numGames = latestGameID() + 1
        streaks = {}

        for member in groupMembers:
            user = fetchUser(member)
            if user:
                streaks[str(user["id"])] = {
                    "fullName": user["fullname"],
                    "currentStreak": 0,
                    "maxStreak": 0,
                    "streakData": [0] * numGames,
                }

        chartData = []

        for game in range(0, latestGameID() + 1):
            for user, streak in streaks.items():
                filteredResult = list(
                    filter(
                        lambda result: str(result["user"]) == user
                        and result["game"] == game,
                        results,
                    )
                )

                result = None
                if filteredResult:
                    result = filteredResult[0]

                if result and result["success"]:
                    streak["currentStreak"] += 1
                    if streak["currentStreak"] > streak["maxStreak"]:
                        streak["maxStreak"] = streak["currentStreak"]
                else:
                    streak["currentStreak"] = 0

                streak["streakData"][game] = streak["currentStreak"]

        for result in results:
            if str(result["user"]) in streaks:
                data = streaks[str(result["user"])]

                chartData.append(
                    {
                        "game": result["game"],
                        "user": f"{data['fullName']} - longest: {data['maxStreak']}, current: {data['currentStreak']}",
                        "streak": data["streakData"][result["game"]],
                    }
                )

        categoryOrders = {"user": []}

        caption = ""
        for member in groupMembers:
            data = streaks[str(member)]

            categoryOrders["user"].append(
                f"{data['fullName']} - longest: {data['maxStreak']}, current: {data['currentStreak']}"
            )

            caption += f"{data['fullName']} - longest: {data['maxStreak']}, current: {data['currentStreak']}\n"

        fig = px.line(
            chartData,
            width=1920,
            height=1080,
            x="game",
            y="streak",
            color="user",
            category_orders=categoryOrders,
            labels={
                "game": "Game",
                "streak": "Streak",
                "user": "User",
            },
            title="Streak History",
        )

        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0,
            ),
            title_x=0.5,
            font=dict(size=40),
        )

        tempFile, tempFileName = tempfile.mkstemp(suffix=".png")
        os.close(tempFile)

        fig.write_image(tempFileName)

        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                photo=tempFileName,
                caption=caption,
                filename="streakshistory.png",
            )
        except Exception as e:
            print(f"Exception: '{e}'")

        os.remove(tempFileName)


async def postInitHandler(application: Application):
    commands = [
        BotCommand("results", "Display results"),
        BotCommand("streaks", "Display streak information"),
    ]

    await application.bot.set_my_commands(commands)


@click.command()
@click.pass_context
def telegramBot(ctx):
    global base_url

    base_url = ctx.obj["BASE_URL"]

    application = (
        ApplicationBuilder().token(Token.Token).post_init(postInitHandler).build()
    )

    botMembershipHandler = ChatMemberHandler(
        botMembership, ChatMemberHandler.MY_CHAT_MEMBER
    )
    application.add_handler(botMembershipHandler)

    groupMembershipHandler = ChatMemberHandler(
        groupMembership, ChatMemberHandler.CHAT_MEMBER
    )
    application.add_handler(groupMembershipHandler)

    chatMessageHandler = MessageHandler(filters.TEXT & (~filters.COMMAND), chatMessage)
    application.add_handler(chatMessageHandler)

    resultsHandler = CommandHandler("results", results)
    application.add_handler(resultsHandler)

    streaksHandler = CommandHandler("streaks", streaks)
    application.add_handler(streaksHandler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
