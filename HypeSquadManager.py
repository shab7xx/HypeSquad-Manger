import os
import sys
import requests
from colorama import init, Fore

init(autoreset=True)

class HypeSquadManager:
    def __init__(self):
        self.token = None
        self.houses = {"bravery": 1, "brilliance": 2, "balance": 3}
        self.session = requests.Session()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        banner = f"""{Fore.RED}
  _________.__          _______________________  ___        
 /   _____/|  |__ _____ \______   \______  \   \/  /___  ___
 \_____  \ |  |  \\__  \ |    |  _/   /    /\     / \  \/  /
 /        \|   Y  \/ __ \|    |   \  /    / /     \  >    < 
/_______  /|___|  (____  /______  / /____/ /___/\  \/__/\_ \\
        \/      \/     \/       \/               \_/      \/    
                    {Fore.MAGENTA}Developed by: ShaB7Xx{Fore.RESET}
"""
        print(banner)
    
    def set_token(self, token):
        self.token = token.strip()
        self.session.headers.update({'authorization': self.token, 'content-type': 'application/json'})
        print(f"\n{Fore.GREEN}[+] Token set successfully")
        self.check_hypesquad()

    def check_hypesquad(self):
        if not self.token:
            print(f"\n{Fore.RED}[!] Please set your token first")
            return
        
        try:
            res = self.session.get('https://discord.com/api/v9/users/@me')
            if res.status_code == 200:
                data = res.json()
                flags = data.get('public_flags', 0)
                
                if flags & (1 << 6):
                    print(f"{Fore.CYAN}[*] Current House: Bravery")
                elif flags & (1 << 7):
                    print(f"{Fore.CYAN}[*] Current House: Brilliance")
                elif flags & (1 << 8):
                    print(f"{Fore.CYAN}[*] Current House: Balance")
                else:
                    print(f"{Fore.YELLOW}[!] You are not in any HypeSquad house")
            else:
                print(f"{Fore.RED}[!] Failed to check status: {res.status_code}")
                if res.status_code == 401:
                    print(f"{Fore.RED}[!] Invalid Token")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")

    def join_house(self, house_id):
        if not self.token:
            print(f"\n{Fore.RED}[!] Please set your token first")
            return
        
        try:
            res = self.session.post('https://discord.com/api/v9/hypesquad/online', json={'house_id': house_id})
            if res.status_code == 204:
                house_name = [name for name, id in self.houses.items() if id == house_id][0]
                print(f"\n{Fore.GREEN}[+] Successfully joined house: {house_name.capitalize()}")
            else:
                print(f"\n{Fore.RED}[!] Failed to join: {res.text}")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error: {e}")

    def leave_hypesquad(self):
        if not self.token:
            print(f"\n{Fore.RED}[!] Please set your token first")
            return
        
        try:
            res = self.session.delete('https://discord.com/api/v9/hypesquad/online')
            if res.status_code == 204:
                print(f"\n{Fore.GREEN}[+] Successfully removed HypeSquad badge")
            else:
                print(f"\n{Fore.RED}[!] Failed to remove: {res.text}")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error: {e}")

    def display_main_menu(self):
        print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}] > Set Token")
        print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}] > Join HypeSquad")
        print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}] > Leave HypeSquad")
        print(f"{Fore.WHITE}[{Fore.RED}4{Fore.WHITE}] > Check Status")
        print(f"{Fore.WHITE}[{Fore.RED}0{Fore.WHITE}] > Exit")
        print(f"\n{Fore.RED}[>]{Fore.WHITE} Choose : ", end="")

    def join_hypesquad_menu(self):
        self.clear_screen()
        self.display_banner()
        print(f"{Fore.WHITE}[{Fore.RED}1{Fore.WHITE}] > Bravery")
        print(f"{Fore.WHITE}[{Fore.RED}2{Fore.WHITE}] > Brilliance")
        print(f"{Fore.WHITE}[{Fore.RED}3{Fore.WHITE}] > Balance")
        print(f"{Fore.WHITE}[{Fore.RED}0{Fore.WHITE}] > Back")
        print(f"\n{Fore.RED}[>]{Fore.WHITE} Choose House : ", end="")
        
        choice = input().strip()
        if choice == "1":
            self.join_house(1)
        elif choice == "2":
            self.join_house(2)
        elif choice == "3":
            self.join_house(3)
        elif choice == "0":
            return
        else:
            print(f"\n{Fore.RED}[!] Invalid choice")
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

    def run(self):
        try:
            while True:
                self.clear_screen()
                self.display_banner()
                self.display_main_menu()
                
                choice = input().strip()
                
                if choice == "1":
                    token = input(f"\n{Fore.YELLOW}[?] Enter Token: ").strip()
                    if token:
                        self.set_token(token)
                    input(f"\n{Fore.YELLOW}Press Enter to continue...")
                
                elif choice == "2":
                    self.join_hypesquad_menu()
                
                elif choice == "3":
                    self.leave_hypesquad()
                    input(f"\n{Fore.YELLOW}Press Enter to continue...")
                
                elif choice == "4":
                    self.check_hypesquad()
                    input(f"\n{Fore.YELLOW}Press Enter to continue...")
                
                elif choice == "0":
                    print(f"\n{Fore.RED}[!] Exiting...")
                    sys.exit(0)
                
                else:
                    print(f"\n{Fore.RED}[!] Invalid choice")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Program terminated by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Unexpected Error: {e}")
            input(f"\n{Fore.YELLOW}Press Enter to exit...")
            sys.exit(1)

if __name__ == "__main__":
    manager = HypeSquadManager()
    manager.run()
