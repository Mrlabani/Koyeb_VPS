import subprocess
from flask import Flask
from pyrogram import Client, filters

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return "Ghost API Bot is running!"

# Pyrogram bot setup
api_id = "6435225"  # Replace with your API ID
api_hash = "4e984ea35f854762dcde906dce426c2d"  # Replace with your API hash
bot_token = "7863196804:AAHLuwSibBQf4denufOtuflKDinvzHgRfDw"  # Replace with your bot token

bot = Client("ghost_api_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# /start command
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply(
        "This is Ghost API Bot.\nContact - @yukilogs for support"
    )

# /run command
@bot.on_message(filters.command("run"))
async def run_command(client, message):
    try:
        # Execute the curl command
        result = subprocess.run(
            ["curl", "-sSf", "https://sshx.io/get", "|", "sh", "-s", "run"],
            check=True,
            shell=True,
            capture_output=True,
            text=True
        )
        await message.reply(
            f"Command executed successfully:\n\n{result.stdout}"
        )
    except subprocess.CalledProcessError as e:
        await message.reply(
            f"Error while running the command:\n\n{e.stderr}"
        )
    except Exception as e:
        await message.reply(
            f"An unexpected error occurred: {str(e)}"
        )

# Start Flask and Pyrogram
if __name__ == "__main__":
    import threading

    # Run Pyrogram bot in a separate thread
    def run_bot():
        bot.run()

    threading.Thread(target=run_bot).start()

    # Run Flask web service
    app.run(host="0.0.0.0", port=8000)