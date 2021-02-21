import os, toml, shutil


class Config:
    def get_path(self, name):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    def extract_config(self, file_name, template_name):
        config_file = self.get_path(file_name)
        if not os.path.isfile(config_file):
            print("config file doesn't exist, copying template!")
            shutil.copyfile(self.get_path(template_name), config_file)
        return config_file


class TomlConfig(Config):
    def __init__(self, file_name, template_name):
        config_file = self.extract_config(file_name, template_name)
        self.load_config(config_file)

    def load_config(self, config_file):
        config = toml.load(config_file)
        client = config["client"]
        self.user_agent = client["user_agent"]

        nvidia = client["nvidia"]
        self.nvidia_link = nvidia["link"]
        self.nvidia_enabled = nvidia["enabled"]
        self.nvidia_delay = nvidia["delay"]
        self.nvidia_api_url = nvidia["api_url"]
        self.nvidia_referer = nvidia["referer"]

        ldlc = client["ldlc"]
        self.ldlc_enabled = ldlc["enabled"]
        self.ldlc_delay = ldlc["delay"]
        self.ldlc_url = ldlc["url"]
        self.ldlc_referer = ldlc["referer"]

        telegram = config["alerters"]["telegram"]
        self.telegram_api_id = telegram["api_id"]
        self.telegram_api_hash = telegram["api_hash"]
        self.telegram_bot_token = telegram["bot_token"]
        self.telegram_usernames = telegram["usernames"]
