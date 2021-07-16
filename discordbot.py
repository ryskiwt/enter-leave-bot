import json
import os

import requests
from discord.ext import tasks
import discord


# https://discord.com/developers/applications から取得
token = os.environ["DISCORD_BOT_TOKEN"]

# Discordを開発者モードにしてチャンネルを右クリックで取得できる
channel_id = int(os.environ["DISCORD_TARGET_CHANNEL_ID"])

# GASのdoPostで受けて、好きなところへ連携するのがオススメ
webhook_url = os.environ["WEBHOOK_URL"]

client = discord.Client()

channel_name = None
previous_members = []
members = []

# 10秒ごと
@tasks.loop(seconds=10)
async def send_periodic_message():
    global channel_name, members, previous_members

    if set(members) == set(previous_members):
        return

    # 累積した入退室者の確認
    msg = {
        "action": "periodic",
        "channel_name": channel_name,
        "members": members,
        "entering_members": list(set(members) - set(previous_members)),
        "leaving_members": list(set(previous_members) - set(members)),
    }
    requests.post(
        webhook_url,
        data=json.dumps(msg),
        headers={"Content-Type": "application/json"},
    )
    previous_members = members


# 起動時
@client.event
async def on_ready():
    global channel_name
    channel = client.get_channel(channel_id)
    channel_name = channel.name
    send_periodic_message.start()


# 状態の更新時
@client.event
async def on_voice_state_update(member, before, after):
    global channel_name, members

    if before.channel != after.channel:

        # 入室
        if after.channel is not None and after.channel.id == channel_id:
            channel_name = after.channel.name
            members = [m.name for m in after.channel.members]
            msg = {
                "action": "enter",
                "channel_name": channel_name,
                "trigger_member": member.name,
                "members": members,
            }
            requests.post(
                webhook_url,
                data=json.dumps(msg),
                headers={"Content-Type": "application/json"},
            )

        # 退室
        if before.channel is not None and before.channel.id == channel_id:
            channel_name = before.channel.name
            members = [m.name for m in before.channel.members]
            msg = {
                "action": "leave",
                "channel_name": channel_name,
                "trigger_member": member.name,
                "members": members,
            }
            requests.post(
                webhook_url,
                data=json.dumps(msg),
                headers={"Content-Type": "application/json"},
            )


client.run(token)
