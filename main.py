import requests
import os
from pystyle import Write, Colorate, Colors, Center
from threading import Thread

try:
    import requests
    import os
    from pystyle import Write, Colorate, Colors, Center
except ModuleNotFoundError as ModuleError:
    ModuleNotFound = Write.Input('You dont have the required modules, would you like to install them? (Y/N): ')
    if ModuleNotFound == 'Y' or 'y':
        os.system('pip install requests')
        os.system('pip install pystyle')
        input('Open the file again, modules are downloaded.. ')

def show_banner():
    banner = r'''
 _    _              _  _               _   
| |  (_)_ _ _  ___ _| || |__ _ ___  ___| |__ 
| |__| | ' \ || \ \ / __ / _` / _ \/ _ \ / / Made by @xbt.lol 
|____|_|_||_\_,_/_\_\_||_\__,_\___/\___/_\_\ V.1.1     

--------------------------------------------
[1] Delete Webhook  |  [4] Get Webhook Details
[2] Rename Webhook  |  [5] Edit Config
[3] Spam Webhook
-------------------------------------------- 
'''
    print(Colorate.Horizontal(Colors.blue_to_red, Center.XCenter(banner)))

def delete_webhook(hook):
    print(Colorate.Horizontal(Colors.blue_to_red, "Deleting Webhook"))
    requests.delete(hook)
    print(Colorate.Horizontal(Colors.blue_to_red, "Deleted!"))

def rename_webhook(hook):
    name = Write.Input('Name >> ', Colors.blue_to_red, interval=0.025)
    requests.patch(hook, json={"name": name})
    print(Colorate.Horizontal(Colors.blue_to_red, "Changed!"))

def spam_webhook(hook):
    print(Colorate.Horizontal(Colors.blue_to_red, "Starting!"))
    amount = int(Write.Input('Amount >> ', Colors.blue_to_red, interval=0.025))
    message = Write.Input('Message >> ', Colors.blue_to_red, interval=0.025)
    threads_count = int(Write.Input('Threads (Recommended: 5) >> ', Colors.blue_to_red, interval=0.025))

    def send_messages():
        for _ in range(amount // threads_count):
            send = requests.post(hook, json={"content": message})
            if send.status_code == 200 or send.status_code == 204:
                print(Colorate.Horizontal(Colors.blue_to_purple, f"[+] Sent: Message"))
            elif send.status_code == 404:
                print(Colorate.Horizontal(Colors.red_to_yellow, "[-] URGENT: Webhook Deleted!"))
            elif send.status_code == 429:
                print(Colorate.Horizontal(Colors.blue_to_red, "[/] Error: Webhook Ratelimited!"))

    threads = []
    for _ in range(threads_count):
        thread = Thread(target=send_messages)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_webhook_details(hook):
    print(Colorate.Horizontal(Colors.blue_to_red, "Getting details!"))
    data = requests.get(hook).json()
    d1 = data.get('channel_id', 'N/A')
    d2 = data.get('token', 'N/A')
    d3 = data.get('avatar', 'N/A')
    print(f"Channel id: {d1}")
    print(f"Token: {d2}")
    print(f"Avatar: {d3}")

def edit_config(hook):
    hook = Write.Input('New webhook >> ', Colors.blue_to_red, interval=0.025)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
    hook = Write.Input('Webhook >> ', Colors.blue_to_red, interval=0.025)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_banner()
        choice = Write.Input('Choice >> ', Colors.blue_to_red, interval=0.025)

        if choice == '1':
            delete_webhook(hook)
        elif choice == '2':
            rename_webhook(hook)
        elif choice == '3':
            spam_webhook(hook)
        elif choice == '4':
            get_webhook_details(hook)
        elif choice == '5':
            edit_config(hook)
        else:
            print(Colorate.Horizontal(Colors.red_to_yellow, "Invalid choice, try again!"))

        cont = Write.Input('Go back to home screen? (y/n) >> ', Colors.blue_to_red, interval=0.025)

        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
