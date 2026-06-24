Full process to run AURA STORAGE on your laptop
Prerequisites — one-time setup
1. Check if Python is installed Open Terminal and run:

python3 --version
You need Python 3.9 or higher. If you get "command not found", download it from python.org and install it.

Every time you want to run it
2. Open Terminal and navigate to the project folder

cd ~/Downloads/aura-storage-python
3. Install dependencies (only needed once, or after a fresh download)

pip3 install -r requirements.txt
This installs FastAPI, uvicorn, and everything else the app needs. Takes about 1–2 minutes the first time.

4. Start the server

python3 main.py
You'll see:

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
5. Open your browser Go to: http://localhost:8000

That's it — the full UI with all 4 modules loads from there.

To stop the server
Press Ctrl + C in the Terminal window where it's running.

If something breaks
"No module named 'fastapi'" → run pip3 install -r requirements.txt again

"Address already in use" → something else is on port 8000. Run:

python3 main.py
Or kill the old process:

lsof -ti:8000 | xargs kill -9
