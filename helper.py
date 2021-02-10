import requests
import json
import urllib.parse
import time


class Config:
    def __init__(self):
        print("Initializing")
        self.access_token = ""
        with open("config.json", 'r') as configfile:
            self.settings = json.load(configfile)
        self.scheduler = Scheduler()

    def get_token(self):
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.settings["refresh_token"],
            "access_type": "offline",
            "client_id": self.settings["client_id"],
            "redirect_uri": "https://127.0.0.1"
        }
        self.scheduler.report_call()
        r = requests.post(self.settings["auth_endpoint"], headers=header, data=urllib.parse.urlencode(body))
        if r.status_code == 200:
            response = json.loads(json.dumps(r.json()))
            with open("config.json", 'w') as configfile:
                self.settings["refresh_token"] = response["refresh_token"]
                json.dump(self.settings, configfile)
                self.access_token = "Bearer " + response["access_token"]
            print("Bearer token created: {}".format(self.access_token))
            print("    **Info: Retrieved access token, continuing")
            return 0
        else:
            print(r.status_code)
            response = json.loads(json.dumps(r.json()))
            print(response)
            return 1


class Scheduler:
    def __init__(self):
        self.start_time = None
        self.call_counter = 0
        self.start_timer()

    def start_timer(self):
        if self.start_time is not None:
            raise Exception("Start operation failed, use stop_timer() to pause scheduler.")
        else:
            self.start_time = time.perf_counter()

    def get_elapsed(self):
        return time.perf_counter() - self.start_time

    def report_call(self):
        time_delta = time.perf_counter() - self.start_time
        if time_delta < 0.55:
            time.sleep(0.55 - time_delta)
        self.start_time = time.perf_counter()
