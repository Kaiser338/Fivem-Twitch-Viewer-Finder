import requests as req
import json
import mysql.connector
from discord_webhook import DiscordWebhook
from time import time, sleep

"""
whitelist = ['buter_____','aniulkaa','sysiaaa__','serovvy','krysteq33','kwiecciek','mcgagupl12','malina_1998','no_lo_ve','zo_onk','bydlak__','hanyss07','deboslaw','keejk_','j4nkes7','wwesola','xukayo','kill3r______','oronaboro','darkev1337','jawor9991','kreizzii','mycuhehexd','sh0rder1337','banasiczek1','blancik___'
            ,'rp_icej', 'majerankoffy', 'thenikooss', 'trintenn', 'mmmmakssss', 'emmeal_', 'kkloss', 'trejvis', 'adriann664', 'BlooDyY7', '777ness', 'sensiik', 'bosschomik', '12bzyku12', 'foxuuuuuuu', 'cebula_ak', 'kominegl', 'vekus5', 'xraaven_', 'arax_x', 'cal1neczka', 'cyycuuu', 'modeyoo', 'xsqu1r', 'dexiiiiiii', 'blindkret', 'xspaceeee', 'jelonxbot', 'kacperwilla', 'eevilbunny', 'pumbaxtv', 'ol4z', 'szymon_112_', 'voxiloss', 'kjubiq71', 'saiber81', 'morsky69', '20bartek00', 'semper_23', 'shinedvd', 'ram_bo0', '8pulpet8', 'rokicooo', 'skunmaster4200', 'szymtocz', '777huberik', 'sad_norton', 'benito_121', 'kubik03x', 'liteer_', 'potul2k', 'drapiezny_rzuf', 'xkarpollll', 'bifur444', 'iqvvertyi', 'enz0_3', 'mesjaszek', 'japkooooooo', 'krysteq33', 'kvrmel_', 'co0oki396', 'cacek_pl', 'gothdamnn', 'kondzeex', 'kungun123', 'veroon']
"""

whitelist = []
players = {}
players_data = {}
streamers = []
Webhookurl = "https://discord.com/api/webhooks/902592100883906600/cxAk7nwi77M4bvly8wEjdiCD7jdeTy2yPwGsmWG2QbEdBB7K3a6VqfXlRFQDqfl09Si3"
BotName = "Konfident"
BotAvatarUrl = "https://stopkonfidentom.pl/wp-content/uploads/2021/05/19a.jpg"

db = mysql.connector.connect(
    host = "127.0.0.1",
    user="root",
    passwd="gLp24VNX2x",
    database="twitch_players",
    port=3307
)

mycursor = db.cursor()
sqlFormula = "SELECT twitch_name,steam_hex FROM suspects"
mycursor.execute(sqlFormula)
myresult = mycursor.fetchall()

for row in myresult:
    whitelist.insert(len(whitelist),row[0])
    players_data[row[0]] = row[1]

sqlFormula2 = "SELECT name FROM streamers"
mycursor.execute(sqlFormula2)
myresult2 = mycursor.fetchall()

print("Streamers in base:")
for row in myresult2:
    streamers.insert(len(streamers),bytearray.decode(row[0]))
    print(bytearray.decode(row[0]))

def IsOnStream(name,streamerwatched):
    resp = req.request(method='GET', url="https://tmi.twitch.tv/group/user/"+streamerwatched+"/chatters")
    json_object = json.loads(resp.text)
    for k,v in json_object.items():
        if isinstance(v, dict):
            for k2,v2 in v.items():
                if type(v2) is list:
                    for online in v2:
                        if online == name:
                            return True
    return False

def IsOnServer(identifier):
    resp = req.request(method='GET', url="http://45.157.235.88:30130/players.json")
    json_object = json.loads(resp.text)
    for k in json_object:
        for k2,v2 in k.items():
            if type(v2) is list:
                for k3 in v2:
                    if k3 == identifier:
                        return True
    return False


webhook = DiscordWebhook(
url = Webhookurl,
content = "Bot Started",
username = BotName,
avatar_url = BotAvatarUrl)
response = webhook.execute()



while True:
    print("INITIALIZING")
    sleep(1.0)
    for watchedstreamer in streamers:
        print("Checking "+watchedstreamer)
        sleep(3.0)
        resp = req.request(method='GET', url="https://tmi.twitch.tv/group/user/"+watchedstreamer+"/chatters")
        json_object = json.loads(resp.text)
        for k,v in json_object.items():
            if isinstance(v, dict):
                for k2,v2 in v.items():
                    if type(v2) is list:
                        for online in v2:
                            for whitelisted in whitelist:
                                if online == whitelisted and IsOnServer(players_data[online]):
                                    sleep(1.0)
                                    webhook = DiscordWebhook(
                                    url=Webhookurl,
                                    content= whitelisted + " joined the "+watchedstreamer+" stream and  he is playing on the server",
                                    username = BotName,
                                    avatar_url = BotAvatarUrl)
                                    response = webhook.execute()
                                    whitelist.remove(whitelisted)
                                    players[online] = watchedstreamer
    for k,v in players.items():
        if v != None:
            if(not IsOnStream(k,v)):
                webhook = DiscordWebhook(
                url=Webhookurl,
                content=k + " left the "+v+" stream",
                username = BotName,
                avatar_url = BotAvatarUrl)
                response = webhook.execute()
                players[k] = None
                whitelist.insert(len(k),k)
            elif(not IsOnServer(players_data[k])):
                webhook = DiscordWebhook(
                url=Webhookurl,
                content=k + " left the server but he's still on "+v+" stream",
                username = BotName,
                avatar_url = BotAvatarUrl)
                response = webhook.execute()
                players[k] = None
                whitelist.insert(len(k),k)
