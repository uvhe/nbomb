import requests
import time
import os

def _exit():
    time.sleep(5)
    exit()

def check_hook(hook):
    info = requests.get(hook).text
    if "\"message\": \"Unknown Webhook\"" in info:
        return False
    return True

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

    send_to_multiple_webhooks = input("Send the message to multiple webhooks? (Y/N) > ").strip().lower()
    
    if send_to_multiple_webhooks != "y":
        webhook = input("Enter your webhook > ").strip()
        webhooks = [webhook]
    else:
        num_webhooks = int(input("How many webhooks do you want to use? > "))
        webhooks = []
        for i in range(num_webhooks):
            webhook = input(f"Enter webhook {i + 1} > ").strip()
            webhooks.append(webhook)

    message = input("Enter a message > ").strip()
    delay = input("Enter a delay [int/float] > ").strip()
    amount = input("Enter an amount [int/inf] > ").strip()
    hookDeleter = input("Delete webhook(s) after spam? (Y/N) > ").strip()
    
    try:
        delay = float(delay)
    except ValueError:
        _exit()

    if not all(check_hook(webhook) for webhook in webhooks) or (not amount.isdigit() and amount != "inf") or (hookDeleter.lower() != "y" and hookDeleter.lower() != "n"):
        _exit()
    else:
        main(webhooks, delay, amount, message, hookDeleter)
        _exit()

if __name__ == '__main__':
    os.system('cls')
    initialize()
