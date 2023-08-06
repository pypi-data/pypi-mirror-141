import os

from notebuild.core.core import command_line_parser
from notebuild.shell import run_shell

# sudo kill -9 `sudo lsof -t -i:8444`
# nohup python notecoin_server.py  >>/notechats/logs/notecoin/strategy-$(date +%Y-%m-%d).log 2>&1 &


class CoinServer:
    def __init__(self):
        self.server_name = 'notecoin_server'
        self.current_path = os.path.abspath(os.path.dirname(__file__))

    def init(self):
        print(self.current_path)
        run_shell(f"cd {self.current_path} && supervisord -c supervisord.conf")

    def stop(self):
        run_shell(f"cd {self.current_path} && supervisorctl stop {self.server_name}")

    def start(self):
        run_shell(f"cd {self.current_path} && supervisorctl start {self.server_name}")

    def restart(self):
        run_shell(f"cd {self.current_path} && supervisorctl restart {self.server_name}")


def notecoin():
    args = command_line_parser()
    package = CoinServer()
    if args.command == 'init':
        package.init()
    elif args.command == 'stop':
        package.stop()
    elif args.command == 'start':
        package.start()
    elif args.command == 'restart':
        package.restart()
    elif args.command == 'help':
        info = """
init
stop
start
restart
        """
        print(info)
