import yaml
from pathlib import Path

class Config:
    def __init__(self, configPath: str):
        self.configPath = configPath
        self.accounts = []
        self.debug = False
        self.loadConfig()

    def loadConfig(self):
        try:
            with open(self.configPath, 'r') as file:
                config = yaml.safe_load(file)
                
            self.accounts = config.get('accounts', [])
            self.debug = config.get('debug', False)
            
            if not self.accounts:
                raise ValueError("No accounts found in config file")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {self.configPath}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading config: {e}") 