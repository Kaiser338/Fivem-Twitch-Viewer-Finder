from time import sleep
from twitch_bot import TwitchBot

def main():
    bot = TwitchBot()
    
    while True:
        print("CHECKING STREAMS...")
        sleep(1.0)
        bot.check_streams()

if __name__ == "__main__":
    main()


