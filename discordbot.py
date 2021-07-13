import os
import requests, json

import discord


token = os.environ["DISCORD_BOT_TOKEN"] # https://discord.com/developers/applications から取得
channel_id = os.environ["DISCORD_TARGET_CHANNEL_ID"] # Discordを開発者モードにしてチャンネルを右クリックで取得できる
webhook_url = os.environ["SLACK_WEBHOOK_URL"] # Slack に Incoming Webhook を追加して取得


client = discord.Client()


def post_to_slack(msg):
    requests.post(webhook_url, data=json.dumps({"text": msg}))


@client.event
async def on_voice_state_update(member, before, after):

    if before.channel != after.channel:

        # 入室
        if after.channel is not None and after.channel.id == channel_id:
            msg = f"{before.channel.name} に、 {member.name} が入室しました。\n\n" \
                "現在の参加者:\n  " \
                "\n  ".join([m.name for m in after.channel.members])
            post_to_slack(msg)

        # 退室
        if before.channel is not None and before.channel.id == channel_id:
            msg = f"{before.channel.name} から、 {member.name} が退室しました。\n\n" \
                "現在の参加者:\n  " \
                "\n  ".join([m.name for m in before.channel.members])
            post_to_slack(msg)

client.run(token)
