from aiohttp import web
import asyncio
from main import bot
import os

PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("TOKEN")

async def handle(request):
    return web.Response(text="Bot activo!")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web server listening on port {PORT}")

async def main():
    await run_web()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
