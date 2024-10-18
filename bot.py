import cloudscraper
import os
from colorama import *
from datetime import datetime
import time
import pytz
from requests.exceptions import RequestException

wib = pytz.timezone('Asia/Jakarta')

class Pumpad:
    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'tg.pumpad.io',
            'Cookie': 'cf_clearance=',
            'Pragma': 'no-cache',
            'Referer': 'https://tg.pumpad.io/lottery/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Pumpad - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        
    def user_information(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/tg/user/information'
        self.headers.update({
            'Authorization': f'tma {query}'
        })

        response = self.scraper.get(url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:
            return result
        else:
            return None
        
    def get_lottery(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/lottery'
        self.headers.update({
            'Authorization': f'tma {query}',
        })

        response = self.scraper.get(url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:
            return result
        else:
            return None
    
    def post_lottery(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/lottery'
        self.headers.update({
            'Authorization': f'tma {query}',
        })

        response = self.scraper.post(url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:
            return result
        else:
            return None
    
    def get_missions(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/tg/missions'
        self.headers.update({
            'Authorization': f'tma {query}',
        })

        response = self.scraper.get(url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:
            return result
        else:
            return None
    
    def post_missions(self, query: str, mission_id: int):
        url = f'https://tg.pumpad.io/referral/api/v1/tg/missions/check/{mission_id}'
        data = {}
        self.headers.update({
            'Authorization': f'tma {query}',
        })

        response = self.scraper.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:
            return result
        else:
            return None
    
    def process_query(self, query: str):
        try:
            user = self.user_information(query)
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['user_name']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

            lottery = self.get_lottery(query)
            if lottery is not None:
                count = lottery['draw_count']
                if count != 0:
                    while count > 0:
                        draw = self.post_lottery(query)
                        if draw is not None:
                            if 'reward' in draw:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Draw{Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT} Is Success {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {draw['reward']['name']} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Draw{Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT} Isn't Success {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                        else:
                            self.log(f"{Fore.RED + Style.BRIGHT}[ Data Post Lottery Is None ]{Style.RESET_ALL}")
                        count -= 1
                else:
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}[ You Don't Have Enough Draw Count ]{Style.RESET_ALL}")
            else:
                self.log(f"{Fore.RED + Style.BRIGHT}[ Data Get Lottery Is None ]{Style.RESET_ALL}")

            missions = self.get_missions(query)
            if missions['mission_list'] is not None and 'mission_list' in missions:
                for mission in missions['mission_list']:
                    mission_id = mission['mission']['id']
                    mission_name = mission['mission']['name']
                    mission_reward = mission['mission']['reward']
                    done_time = mission['done_time']

                    if mission_id == 38:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {mission_name} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Skipped{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                        continue

                    if done_time == 0:
                        complete = self.post_missions(query, mission_id)
                        if complete is True:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {mission_name} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} +{mission_reward} Draw Count {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {mission_name} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {mission_name} {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}Is Already Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
            else:
                self.log(f"{Fore.GREEN + Style.BRIGHT}[ Mission Clear ]{Style.RESET_ALL}")

        except RequestException as e:
            self.log(
                f"{Fore.RED + Style.BRIGHT}[ Blocked By Cloudflare ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}[ Restart First ]{Style.RESET_ALL}"
            )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Pumpad - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    pumpad = Pumpad()
    pumpad.main()