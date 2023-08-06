import click
from qplay_cli.dataset.commands import dataset
from qplay_cli.backtest.commands import backtest
from qplay_cli.user.commands import user
import configparser
import os
from os.path import expanduser
from qplay_cli.qplay_config import QplayConfig
from qplay_cli.instance import Instance

@click.group()
def quantplay():
    pass

quantplay.add_command(dataset)
quantplay.add_command(backtest)
quantplay.add_command(user)

@quantplay.command()
def launch_machine():
    credentials = QplayConfig.get_credentials()
    access_token = credentials['DEFAULT']['access_token']
    
    print("Enter lease time in hours")
    lease_time = input()
    
    response = Instance().launch_machine(access_token, lease_time)
    print(response['message'])
    
if __name__ == '__main__':
    quantplay()