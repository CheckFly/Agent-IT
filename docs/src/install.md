
# Agent-IT Installation

## Creation utilisateur agent_it

'sudo useradd -m agent_it
mkdir /opt/agent_it
sudo chown -R agent_it:agent_it /opt/agent_it
sudo -u agent_it git clone <https://github.com/CheckFly/Agent-IT> /opt/agent_it'

## environnement python

'python3 -m venv /home/envs/agent_it
source /home/envs/agent_it/bin/activate
cd /opt/agent_it/Agent-IT
pip install -r requirements'

## Creation service

le fichier /etc/systemd/system/agent_it.service

[Unit]
Description=Agent_IT FastAPI Server
After=network.target mariadb.service

[Service]
User=agent_it
Group=agent_it

WorkingDirectory=/opt/agent_it

Environment="PYTHONPATH=/opt/agent_it/Agent-IT/src"

ExecStart=/home/envs/agent_it/bin/uvicorn \
    agent_it.server.api:app \
    --host 0.0.0.0 \
    --port 8000

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

### command

'sudo systemctl daemon-reload
sudo systemctl enable agent_it
sudo systemctl start agent_it
journalctl -u agent_it -f'
