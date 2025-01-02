#!/bin/bash
set -e

export PYTHONPATH=/home/computeruse

./start_all.sh
./novnc_startup.sh

python http_server.py > /tmp/server_logs.txt 2>&1 &

# Run our new server that handles both Streamlit and FastAPI
cd /home/computeruse && python -m computer_use_demo.server > /tmp/server.log 2>&1 &

echo "✨ Computer Use Demo is ready!"
echo "➡️  Open http://localhost:8080 in your browser to begin"

# Keep the container running
tail -f /dev/null
