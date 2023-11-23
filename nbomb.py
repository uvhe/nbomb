import requests
import time
import os
import re

def _exit():
    time.sleep(5)
    exit()

def is_valid_url(url):
    regex = r"^(http|https)://[a-zA-Z0-9.-]+.[a-zA-Z]{2,6}(/.*)?$"
    return re.match(regex, url)

def check_hook(hook):
    try:
        if is_valid_url(hook):
            info = requests.get(hook).text
            if "\"message\": \"Unknown Webhook\"" in info:
                return False
        else:
            return False
    except requests.exceptions.MissingSchema:
        pass
    except requests.exceptions.InvalidSchema:
        pass
    return True

def get_webhooks_from_file(file_path):
    valid_webhooks = []
    invalid_webhooks = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                webhook = line.strip()
                if check_hook(webhook):
                    valid_webhooks.append(webhook)
                else:
                    invalid_webhooks.append(webhook)
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")

    return valid_webhooks, invalid_webhooks

def get_webhooks():
    webhooks = []
    num_webhooks = int(input("How many webhooks do you want to use? > "))
    for i in range(num_webhooks):
        while True:
            webhook = input(f"Enter webhook {i + 1} > ").strip()
            if check_hook(webhook):
                webhooks.append(webhook)
                break
            else:
                print("Invalid webhook. Please enter a valid webhook URL.")
    return webhooks

def main(webhooks, delay, amount, message, hookDeleter):
    counter = 0
    while True if amount == "inf" else counter < int(amount):
        try:
            for webhook in webhooks:
                data = requests.post(webhook, json={"content": str(message), "avatar_url": "https://media.discordapp.net/attachments/778720320035094550/808181516483166228/ec35695c38b97ea470a3d8761930f5d7.png"})
                print(f"[+] Sent to {webhook}")

                # Check for rate limit headers
                if 'X-RateLimit-Remaining' in data.headers and 'X-RateLimit-Reset' in data.headers:
                    remaining = int(data.headers['X-RateLimit-Remaining'])
                    reset_timestamp = int(data.headers['X-RateLimit-Reset'])

                    if remaining <= 0:
                        sleep_time = reset_timestamp - int(time.time())
                        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
                        time.sleep(sleep_time)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # Sleep for 1 second in case of errors
        time.sleep(float(delay))
        counter += 1

    if hookDeleter.lower() == "y":
        for webhook in webhooks:
            requests.delete(webhook)
        print('Webhook(s) deleted')
    print('Done')

def initialize():
    print(f"""          
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

    while True:
        send_to_multiple_webhooks = input("Send the message to multiple webhooks? (Y/N) > ").strip().lower()
        if send_to_multiple_webhooks in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    webhooks = []
    if send_to_multiple_webhooks == "y":
        file_path = input("Enter the path to the .txt file containing webhooks > ").strip()
        valid_webhooks, invalid_webhooks = get_webhooks_from_file(file_path)

        print(f"Found {len(valid_webhooks)} valid webhooks.")
        print(f"Found {len(invalid_webhooks)} invalid webhooks.")

        webhooks = valid_webhooks
    else:
        webhooks = get_webhooks()

    message = input("Enter a message > ").strip()

    while True:
        delay = input("Enter a delay [int/float] > ").strip()
        if delay.replace('.', '', 1).isdigit():
            delay = float(delay)
            break
        else:
            print("Invalid input. Please enter a valid delay.")

    while True:
        amount = input("Enter an amount [int/inf] > ").strip()
        if amount.isdigit() or amount.lower() == "inf":
            break
        else:
            print("Invalid input. Please enter a valid amount.")

    while True:
        hookDeleter = input("Delete webhook(s) after spam? (Y/N) > ").strip().lower()
        if hookDeleter in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    main(webhooks, delay, amount, message, hookDeleter)
    _exit()

if __name__ == '__main__':
    os.system('cls')
    initialize()
