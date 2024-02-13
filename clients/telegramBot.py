#!/usr/bin/env python3

import logging
import requests
import click

import Token

import re

from telegram import Update
from telegram.constants import ChatMemberStatus, ChatType
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatMemberHandler,
    MessageHandler,
    filters,
)

base_url = ""
basicAuth = requests.auth.HTTPBasicAuth("andy", "testing")

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
            await context.bot.send_message(
                chat_id=update.my_chat_member.chat.id,
                text=message,
            )


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

        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=message,
        )


async def chatMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    blocks = [
        "\u2B1C\u2B1B",  # Black / white square
        "\U0001F7E8",  # Yellow square
        "\U0001F7E9",  # Green square
    ]

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

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Wordle result for '{user['fullname']}' game {words[1]}: {numGuesses[0]}",
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"@{update.message.from_user.username}, that looked like a Wordle result, but I couldn't parse it properly",
                )
    else:
        print(f"Can't find user with id {update.message.from_user.id}")


@click.command()
@click.pass_context
def telegramBot(ctx):
    global base_url

    base_url = ctx.obj["BASE_URL"]

    application = ApplicationBuilder().token(Token.Token).build()

    bot = application.bot

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

    application.run_polling(allowed_updates=Update.ALL_TYPES)
