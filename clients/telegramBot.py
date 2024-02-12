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

        if message:
            await context.bot.send_message(
                chat_id=update.my_chat_member.chat.id,
                text=message,
            )


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

    application.run_polling(allowed_updates=Update.ALL_TYPES)
