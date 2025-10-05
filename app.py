import os
import asyncio
from aiohttp import web
from main import bot  # Tu bot está en main.py

# 🔹 Puerto que Render asigna automáticamente
PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Asegurate que coincida con tu Secret en Render

# 🔹 Mini webserver para mantener el bot activo 24/7
async def handle(request):
    return web.Response(text="Bot activo 24/7! 🚀")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌐 Web server escuchando en el puerto {PORT}")

# 🔹 Ejecutar webserver + bot juntos
async def main():
    await run_web()
    await asyncio.sleep(1)  # Espera para que Render detecte el puerto
    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⚠️ Bot detenido")
