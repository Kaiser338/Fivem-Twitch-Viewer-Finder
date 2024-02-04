from discord_webhook import DiscordWebhook
import config

class DiscordBot:
    def __init__(self):
        self.webhook = DiscordWebhook(
            url=config.WEBHOOK_CONFIG['URL'],
            username=config.WEBHOOK_CONFIG['NAME'],
            avatar_url=config.WEBHOOK_CONFIG['AVATAR_URL']
        )

    def send_message(self, content):
        self.webhook.content = content
        self.webhook.execute()