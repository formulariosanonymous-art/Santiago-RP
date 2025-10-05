import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

aperturas = {}


class VotarView(View):

    def __init__(self, interaction_id, codigo, votos_minimo):
        super().__init__(timeout=None)
        self.interaction_id = interaction_id
        self.codigo = codigo
        self.votos_minimo = votos_minimo

        votar_btn = Button(label="🔥 Votar para abrir",
                           style=discord.ButtonStyle.red,
                           emoji="🔥")
        votar_btn.callback = self.votar
        self.add_item(votar_btn)

    async def votar(self, interaction: discord.Interaction):
        datos = aperturas[self.interaction_id]
        datos["votos_actuales"] += 1

        votos = datos["votos_actuales"]
        votos_minimo = datos["votos_minimo"]
        codigo = datos["codigo"]

        await interaction.response.send_message(
            f"🔥 ¡Tu voto fue registrado! Van {votos}/{votos_minimo} votos.",
            ephemeral=True)

        mensaje_original = datos["mensaje"]
        embed = mensaje_original.embeds[0]
        embed.set_field_at(
            1,
            name="📊 Progreso de Votación:",
            value=f"```fix\n{votos} / {votos_minimo} votos alcanzados\n```",
            inline=False)
        await mensaje_original.edit(embed=embed, view=self)

        if votos >= votos_minimo and not datos["abierto"]:
            datos["abierto"] = True
            canal = interaction.channel
            embed_final = discord.Embed(
                title="🎊 ¡SERVIDOR OFICIALMENTE ABIERTO! 🎊",
                description=
                ("━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                 "✨ **¡La comunidad ha decidido!** ✨\n\n"
                 f"🎮 Gracias a **{votos} votantes** el servidor está listo\n\n"
                 "🔓 **Las puertas están abiertas**\n"
                 "🌟 Tu aventura de roleplay comienza ahora\n"
                 "💫 Únete a una comunidad vibrante y emocionante\n\n"
                 "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                 f"🔑 **CÓDIGO DE ACCESO:** `{codigo}`\n\n"
                 "⚡ ¡Copia el código y únete ahora mismo!\n"
                 "━━━━━━━━━━━━━━━━━━━━━━━━━"),
                color=discord.Color.from_rgb(0, 255, 127))
            await canal.send(embed=embed_final)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"📡 {len(synced)} comandos sincronizados.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")


@bot.tree.command(name="apertura",
                  description="Publica el mensaje de apertura del servidor.")
@app_commands.describe(
    codigo="Código de acceso al servidor (por ejemplo: RP2025)",
    votos_minimo="Cantidad mínima de votos para abrir (por ejemplo: 10)",
    rol="Rol a mencionar en el anuncio (opcional)")
async def apertura(interaction: discord.Interaction,
                   codigo: str,
                   votos_minimo: int,
                   rol: discord.Role = None):
    embed = discord.Embed(
        title="🔥 ¡APERTURA DE SERVIDOR! 🔥",
        description=("━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                     "🎮 **¡Un nuevo mundo de roleplay está por abrirse!**\n\n"
                     "💎 Experiencia única de roleplay inmersivo\n"
                     "⚡ Comunidad activa y apasionada\n"
                     "🌟 Eventos exclusivos y contenido premium\n\n"
                     "**¡Vota ahora y sé parte de esta aventura!**\n"
                     "━━━━━━━━━━━━━━━━━━━━━━━━━"),
        color=discord.Color.from_rgb(255, 69, 0))
    embed.add_field(name="🗝️ Código de Acceso:",
                    value=f"```{codigo}```",
                    inline=False)
    embed.add_field(name="📊 Progreso de Votación:",
                    value=f"```fix\n0 / {votos_minimo} votos alcanzados\n```",
                    inline=False)
    embed.set_footer(
        text=
        "🔥 Cada voto nos acerca más a la apertura | ¡Tu participación cuenta!")

    view = VotarView(str(interaction.id), codigo, votos_minimo)
    content = rol.mention if rol else None
    mensaje = await interaction.response.send_message(content=content,
                                                      embed=embed,
                                                      view=view)

    aperturas[str(interaction.id)] = {
        "codigo": codigo,
        "votos_minimo": votos_minimo,
        "votos_actuales": 0,
        "abierto": False,
        "mensaje": await interaction.original_response()
    }
