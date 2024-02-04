import requests as req
from time import sleep
from database import Database
from discord_bot import DiscordBot
import config
import json

class TwitchBot:
    def __init__(self):
        self.db = Database()
        self.discord_bot = DiscordBot()
        self.whitelist = self.db.get_whitelist()
        self.players = {}
        self.streamers = self.db.get_streamers()
        self.streamers = ['Grendy']
        self.server_ip = "http://45.157.235.88:30130/players.json"

    def is_on_stream(self, name, streamer_watched):
        resp = req.request(method='GET', url=f"https://tmi.twitch.tv/group/user/{streamer_watched}/chatters")
        json_object = json.loads(resp.text)
        for k, v in json_object.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if type(v2) is list:
                        for online in v2:
                            if online == name:
                                return True
        return False

    def is_on_server(self, identifier):
        resp = req.request(method='GET', url= self.server_ip)
        json_object = json.loads(resp.text)
        for k in json_object:
            for k2, v2 in k.items():
                if type(v2) is list:
                    for k3 in v2:
                        if k3 == identifier:
                            return True
        return False

    def check_streams(self):
        for watched_streamer in self.streamers:
            print("Checking " + watched_streamer)
            sleep(3.0)
            resp = req.request(method='GET', url=f"https://tmi.twitch.tv/group/user/{watched_streamer}/chatters")
            json_object = json.loads(resp.text)
            for k, v in json_object.items():
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        if type(v2) is list:
                            for online in v2:
                                for whitelisted in self.whitelist:
                                    if online == whitelisted and self.is_on_server(self.players_data[online]):
                                        sleep(1.0)
                                        print(f"{whitelisted} joined the {watched_streamer} stream and he is playing on the server")
                                        self.discord_bot.send_message(f"{whitelisted} joined the {watched_streamer} stream and he is playing on the server")
                                        self.whitelist.remove(whitelisted)
                                        self.players[online] = watched_streamer
        for k, v in self.players.items():
            if v is not None:
                if not self.is_on_stream(k, v):
                    self.discord_bot.send_message(f"{k} left the {v} stream")
                    self.players[k] = None
                    self.whitelist.insert(len(k), k)
                elif not self.is_on_server(self.players_data[k]):
                    self.discord_bot.send_message(f"{k} left the server but he's still on {v} stream")
                    self.players[k] = None
                    self.whitelist.insert(len(k), k)


