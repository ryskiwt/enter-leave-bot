# enter-leave-bot

Discord の特定のボイスチャンネルの入退室を監視して、外部の URL に通知するボットです。


## 環境変数

- `DISCORD_BOT_TOKEN`: https://discord.com/developers/applications から取得できる、Discordボットのトークン
- `DISCORD_TARGET_CHANNEL_ID`: 監視対象のチャンネルのID（Discordを開発者モードにしてチャンネルを右クリックで取得できる）
- `WEBHOOK_URL`: 通知を送る先のWebhookのURL


## Webhook 仕様
### 入室があった際の通知

```json
{
    "action": "enter",
    "channel_name": "<チャンネル名>",
    "trigger_member": "<入室したメンバーの名前>",
    "members": ["<現在チャンネルにいるメンバーの名前>", ...],
}
```

### 入室があった際の通知

```json
{
    "action": "leave",
    "channel_name": "<チャンネル名>",
    "trigger_member": "<退室したメンバーの名前>",
    "members": ["<現在チャンネルにいるメンバーの名前>", ...],
}
```

### 1分ごとのサマリ通知

```json
{
    "action": "periodic",
    "channel_name": "<チャンネル名>",
    "members": ["<現在チャンネルにいるメンバーの名前>", ...],
    "entering_members": ["<前回のサマリ通知後に入室したメンバーの名前>", ...],
    "leaving_members": ["<前回のサマリ通知後に退室したメンバーの名前>", ...],
}
```


## オススメの使い方

Google App Script (GAS) の doPost() を使って 一度 Webhook を受けてから、
GAS 内で自由にメッセージを整形して Slack などの他の Incoming Webhook に連携すると、
いろんなツールに柔軟に連携できるのでオススメです。