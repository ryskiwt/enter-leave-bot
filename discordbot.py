import json
import os

import requests
import discord


# https://discord.com/developers/applications から取得
token = os.environ["DISCORD_BOT_TOKEN"]

# Discordを開発者モードにしてチャンネルを右クリックで取得できる
channel_id = int(os.environ["DISCORD_TARGET_CHANNEL_ID"])

# Slack に Incoming Webhook を追加して取得
webhook_url = os.environ["SLACK_WEBHOOK_URL"]


client = discord.Client()


def post_to_slack(msg):
    requests.post(webhook_url, data=json.dumps({"text": msg}))


@client.event
async def on_voice_state_update(member, before, after):

    if before.channel != after.channel:

        # 入室
        if after.channel is not None and after.channel.id == channel_id:
            msg = (
                f"Discordの「{after.channel.name}」チャンネルに、 {member.name} が入室しました。\n\n"
                "現在の参加者:\n  "
                + "\n  ".join([m.name for m in after.channel.members])
            )
            post_to_slack(msg)

        # 退室
        if before.channel is not None and before.channel.id == channel_id:
            msg = (
                f"Discordの「{before.channel.name}」チャンネルから、 {member.name} が退室しました。\n\n"
                "現在の参加者:\n  "
                + "\n  ".join([m.name for m in before.channel.members])
            )
            post_to_slack(msg)


client.run(token)
