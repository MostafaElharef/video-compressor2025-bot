from pyrogram import Client, filters
import os
import subprocess

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def compress_video(input_file, output_file, resolution):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"scale=-2:{resolution}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        output_file
    ]
    subprocess.run(command)

@app.on_message(filters.video | filters.document)
def handle_video(client, message):
    file = message.video or message.document
    msg = message.reply("جاري التحميل...")

    file_path = app.download_media(message)
    base = os.path.splitext(file_path)[0]

    resolutions = {
        "360p": f"{base}_360p.mp4",
        "480p": f"{base}_480p.mp4",
        "720p": f"{base}_720p.mp4"
    }

    for res, out_file in resolutions.items():
        height = int(res.replace("p", ""))
        msg.edit_text(f"جاري الضغط إلى {res} ...")
        compress_video(file_path, out_file, height)
        message.reply_video(out_file, caption=f"الجودة: {res}")

    os.remove(file_path)
    for f in resolutions.values():
        os.remove(f)

    msg.delete()

app.run()
