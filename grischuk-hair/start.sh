#!/bin/bash
cd grischuk-hair
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bot.py
curl -X POST "https://api.telegram.org/bot<7220866591:AAHXN0i2tYfhmCPUQKC-oGZv1ceBAkWmnds>/deleteWebhook" -d "drop_pending_updates=true"
