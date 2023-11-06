import requests, colorama, time, os


def _exit():
    time.sleep(5)
    exit()


def check_hook(hook):
    info = requests.get(hook).text
    if "\"message\": \"Unknown Webhook\"" in info:
        return False
    return True


def main(webhook, delay, amount, message, hookDeleter):
    counter = 0
    while True if amount == "inf" else counter < int(amount):
        try:
            data = requests.post(webhook, json={"content": str(message), "avatar_url": "https://media.discordapp.net/attachments/778720320035094550/808181516483166228/ec35695c38b97ea470a3d8761930f5d7.png"})
            if data.status_code == 204:
                print(f"{colorama.Back.RED} {colorama.Fore.WHITE}[+] Sent{colorama.Back.RESET}")
            else:
                print(f"{colorama.Back.RED} {colorama.Fore.WHITE}[-] Fail{colorama.Back.RESET}")
        except:
            print()
        time.sleep(float(delay))
        counter += 1
    if hookDeleter.lower() == "y":
        requests.delete(webhook)
        print(f'{colorama.Fore.RED}webhook deleted')
    print(f'{colorama.Fore.GREEN}done...')


def initialize():
    print(f"""{colorama.Fore.RED}
          $$\                               $$\       
          $$ |                              $$ |      
$$$$$$$\  $$$$$$$\   $$$$$$\  $$$$$$\$$$$\  $$$$$$$\  
$$  __$$\ $$  __$$\ $$  __$$\ $$  _$$  _$$\ $$  __$$\ 
$$ |  $$ |$$ |  $$ |$$ /  $$ |$$ / $$ / $$ |$$ |  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |
$$ |  $$ |$$$$$$$  |\$$$$$$  |$$ | $$ | $$ |$$$$$$$  |
\__|  \__|\_______/  \______/ \__| \__| \__|\_______/ 
                               https://e-z.bio/vx
          """)
    webhook = input("Enter your webhook > ")
    message = input("Enter a message > ")
    delay = input("Enter a delay [int/float] > ")
    amount = input("Enter an amount [int/inf] > ")
    hookDeleter = input("Delete webhook after spam? [Y/N] > ")
    try:
        delay = float(delay)
    except ValueError:
        _exit()
    if not check_hook(webhook) or (not amount.isdigit() and amount != "inf") or (hookDeleter.lower() != "y" and hookDeleter.lower() != "n"):
        _exit()
    else:
        main(webhook, delay, amount, message, hookDeleter)
        _exit()


if __name__ == '__main__':
    os.system('cls')
    colorama.init()
    initialize()
    