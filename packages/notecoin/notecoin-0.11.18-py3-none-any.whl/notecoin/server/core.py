from notebuild.shell import run_shell

log_dir = "/notechats/logs/notecoin"

run_script = 'python notecoin_server.py'


def start():
    run_shell(f"mkdir -p {log_dir}")
    run_shell(f"nohup {run_script}  >>/notechats/logs/notecoin/strategy-$(date +%Y-%m-%d).log 2>&1 &")


def stop():
    stop_pids = "`ps -ef | grep '" + run_script + "' | awk '{ print $2 }'`"
    print(stop_pids)
    print(run_shell(stop_pids))


start()
stop()
