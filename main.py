import time
import asyncio
from supabase import create_client
from telegram import Bot

# CONFIG
TOKEN = "8111036039:AAETnIcI4P45jEpD9FDwg6fx1_Jj3j1Ak3E"
CHANNEL_ID = "@zazsupports"

SUPABASE_URL = "https://fooboseeshzwpzcbscmr.supabase.co"
SUPABASE_KEY = "sb_publishable_RdAZnIiRo3HauHpRHKOrkg_cztpn551"

# INIT
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
bot = Bot(token=TOKEN)

print("🚀 Bot ishga tushdi")


# ---------------- CHECK FUNCTION ----------------
async def check_messages():

    print("🔎 Tekshirilyapti...")

    try:
        response = supabase.table("messages") \
            .select("*") \
            .eq("sent", False) \
            .execute()

        data = response.data

        if not data:
            return

        for msg in data:

            name = msg.get("name") or msg.get("Name") or "Noma'lum"
            email = msg.get("email") or msg.get("Email") or "-"
            message = msg.get("message") or msg.get("Message") or "-"

            text = f"""📩 Yangi xabar

👤 {name}
📧 {email}
💬 {message}"""

            try:
                # 🔥 IMPORTANT: AWAIT
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )

                print("✅ Yuborildi:", name)

                supabase.table("messages") \
                    .update({"sent": True}) \
                    .eq("id", msg["id"]) \
                    .execute()

            except Exception as err:
                print("❌ Telegram error:", err)

    except Exception as e:
        print("❌ Supabase error:", e)


# ---------------- LOOP ----------------
async def main():
    while True:
        await check_messages()
        await asyncio.sleep(5)


asyncio.run(main())
