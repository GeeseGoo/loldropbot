from src.DataProviderThread import DataProviderThread
from src.FarmThread import FarmThread
from src.GuiThread import GuiThread
from src.Config import Config
from src.Logger import Logger
from src.SharedData import SharedData
from src.Stats import Stats
from src.Restarter import Restarter
from threading import Lock
import logging
import sys
import argparse
from rich import print
from pathlib import Path
from time import sleep, strftime, localtime

CURRENT_VERSION = 1.4

def init() -> tuple[logging.Logger, Config]:
    parser = argparse.ArgumentParser(description='Farm Esports Capsules by watching all matches on lolesports.com.')
    parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                        help='Path to a custom config file')
    args = parser.parse_args()

    print("*********************************************************")
    print(f"*   Thank you for using Capsule Farmer Evolved v{str(CURRENT_VERSION)}!    *")
    print("* [steel_blue1]Please consider supporting League of Poro on YouTube.[/] *")
    print("*    If you need help with the app, join our Discord    *")
    print("*             https://discord.gg/ebm5MJNvHU             *")
    print(f"*                 Started: [green]{strftime('%b %d, %H:%M', localtime())}[/]                *")
    print("*********************************************************")
    print()

    Path("./logs/").mkdir(parents=True, exist_ok=True)
    Path("./sessions/").mkdir(parents=True, exist_ok=True)
    config = Config(args.configPath)
    log = Logger.createLogger(config.debug, CURRENT_VERSION)

    return log, config

def main(log: logging.Logger, config: Config):
    farmThreads = {}
    refreshLock = Lock()
    locks = {"refreshLock": refreshLock}

    sharedData = SharedData()
    stats = Stats()

    for account in config.accounts:
        stats.initNewAccount(account)

    restarter = Restarter(stats)

    log.info(f"Starting a GUI thread.")
    guiThread = GuiThread(log, config, stats, locks)
    guiThread.daemon = True
    guiThread.start()

    dataProviderThread = DataProviderThread(log, config, sharedData)
    dataProviderThread.daemon = True
    dataProviderThread.start()

    while True:
        for account in config.accounts:
            if account not in farmThreads and restarter.canRestart(account) and stats.getThreadStatus(account):
                log.info(f"Starting a thread for {account}.")
                thread = FarmThread(log, config, account, stats, locks, sharedData)
                thread.daemon = True
                thread.start()
                farmThreads[account] = thread
                log.info(f"Thread for {account} was created.")

            if account in farmThreads and not stats.getThreadStatus(account):
                del farmThreads[account]

        toDelete = []
        
        for account in farmThreads:
            if not farmThreads[account].is_alive():
                toDelete.append(account)
                log.warning(f"Thread {account} has finished.")
                restarter.setRestartDelay(account)
                stats.updateStatus(account, f"[red]ERROR - restart at {restarter.getNextStart(account).strftime('%H:%M:%S')}, failed logins: {stats.getFailedLogins(account)}")
                log.warning(f"Thread {account} has finished and will restart at {restarter.getNextStart(account).strftime('%H:%M:%S')}. Number of consecutively failed logins: {stats.getFailedLogins(account)}")
                
        for account in toDelete:
            del farmThreads[account]

        sleep(5)

if __name__ == '__main__':
    log = None
    try:
        log, config = init()
        main(log, config)
    except (KeyboardInterrupt, SystemExit):
        print('Exiting. Thank you for farming with us!')
        sys.exit()
    except Exception as e:
        if isinstance(log, logging.Logger):
            log.error(f"An error has occurred: {e}")
        else:
            print(f'[red]An error has occurred: {e}') 