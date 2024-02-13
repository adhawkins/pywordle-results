#!/usr/bin/env python3

import logging
import requests
import click

import Token

from telegram import Update
from telegram.constants import ChatMemberStatus, ChatType
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatMemberHandler,
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

    application.run_polling(allowed_updates=Update.ALL_TYPES)
