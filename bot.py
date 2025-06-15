import os
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot está rodando!"

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Envie um vídeo e eu retornarei o File ID.")

@bot.on_message(filters.video | filters.document)
async def get_file_id(client, message: Message):
    media = message.video or message.document
    if not media:
        await message.reply("Envie um vídeo ou documento válido.")
        return

    file_id = media.file_id
    file_unique_id = media.file_unique_id
    file_name = media.file_name if media.file_name else "Desconhecido"

    await message.reply(
        f"<b>Nome:</b> <code>{file_name}</code>\n"
        f"<b>File ID:</b> <code>{file_id}</code>\n"
        f"<b>Unique ID:</b> <code>{file_unique_id}</code>",
        parse_mode="html"
    )

# Inicia o Flask (obrigatório no Render)
if __name__ == "__main__":
    import threading

    def run_flask():
        app.run(host="0.0.0.0", port=8080)

    threading.Thread(target=run_flask).start()
    bot.run()
