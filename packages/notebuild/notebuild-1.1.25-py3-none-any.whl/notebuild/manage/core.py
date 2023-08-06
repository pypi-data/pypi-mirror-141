from notebuild.shell import run_shell


class SuperManage:
    def __init__(self):
        self.manage_conf_path = "/notechats/supervisord.conf"
        self.conf_dir = "/notechats/notebuild"

    def init(self):
        run_shell(f"echo_supervisord_conf > {self.manage_conf_path}")
        append_data = f"""
[include]
files = {self.conf_dir}/*.ini
        """
        data = open(self.manage_conf_path, 'r').read()
        data += append_data
        with open(self.manage_conf_path, 'w') as f:
            f.write(data)
        run_shell(f"mkdir {self.conf_dir}")

    def start(self):
        run_shell(f"supervisord -c {self.manage_conf_path}")

    def add_job(self, server_name, directory, command, user='bingtao', stdout_logfile=None):
        default_logfile = f'/notechats/logs/notebuild/{server_name}.log'
        config = f"""[program:{server_name}]
directory = {directory}
command = {command} 
autostart = true
autorestart = true
user = {user}
stdout_logfile = {stdout_logfile or default_logfile}
        """
        with open(f'{self.conf_dir}/{server_name}.ini', 'w') as f:
            f.write(config)


"""
[program:notecoin_server]
directory = .
command = python notecoin_server.py 
autostart = true
autorestart = true
user = bingtao
stdout_logfile = /notechats/logs/notecoin/strategy.log
"""

s = SuperManage()
s.init()
s.add_job(server_name='coin', directory='.', command="python notecoin_server.py", user='bingtao',
          stdout_logfile="/notechats/logs/notecoin/strategy.log")
