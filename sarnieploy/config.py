import json
import sys


class Config:

    def __init__(self, server, config_file=".deploy_config.json"):

        try:
            with open(config_file, "r") as f:
                config = json.load(f)
        except FileNotFoundError as e:
            print("Could not find sarnieploy config file in current location.")
            print("Please refer to documentation on how to create one.")
            print(e)
            sys.exit(1)

        try:
            server_config = config[server]
            self.wars_folder = server_config["wars_folder"]
            self.jetty_stop = server_config["jetty_stop"]
            self.jetty_start = server_config["jetty_start"]
            self.current = server_config["current"]
        except KeyError as e:
            print("Invalid syntax in config file.")
            print("Please refer to documentation on how to create one.")
            print(e)
            sys.exit(1)

    def __repr__(self):
        to_repr = "Config: ["
        to_repr += "wars_folder: {}, ".format(self.wars_folder)
        to_repr += "jetty_stop: {}, ".format(self.jetty_stop)
        to_repr += "jetty_start: {}, ".format(self.jetty_start)
        to_repr += "current: {}]".format(self.current)

        return to_repr
