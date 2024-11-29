import subprocess
import threading
from flask import Flask
from aiohttp import web
from telegram.ext import Updater, CommandHandler

# Flask app setup
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'paradox'

# Aiohttp web server setup
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("str_dump")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8000)
    await site.start()

# PTB bot setup
BOT_TOKEN = "7863196804:AAHLuwSibBQf4denufOtuflKDinvzHgRfDw"  # Replace with your bot token

def start(update, context):
    """Handles the /start command."""
    update.message.reply_text("This is Ghost API Bot.\nContact - @yukilogs for support")

def run_command(update, context):
    """Handles the /run command."""
    try:
        # Execute the curl command safely
        result = subprocess.run(
            ["curl" "-sSf" "https://sshx.io/get" "|" "sh" "-s" "run"],
            check=True,
            capture_output=True,
            text=True
        )
        update.message.reply_text(f"Command executed successfully:\n\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"Error while running the command:\n\n{e.stderr}")
    except Exception as e:
        update.message.reply_text(f"An unexpected error occurred: {str(e)}")

def run_ptb_bot():
    """Starts the PTB bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("run", run_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Flask, aiohttp, and PTB combined runner
if __name__ == "__main__":
    # Run PTB bot in a separate thread
    bot_thread = threading.Thread(target=run_ptb_bot)
    bot_thread.start()

    # Run aiohttp web server in a separate thread
    def start_aiohttp():
        import asyncio
        asyncio.run(web_server())

    aiohttp_thread = threading.Thread(target=start_aiohttp)
    aiohttp_thread.start()

    # Run Flask app
    app.run(host="0.0.0.0", port=8000)