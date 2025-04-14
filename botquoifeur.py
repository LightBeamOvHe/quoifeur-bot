import discord
from discord.ext import commands
import random
import os
import re
import time
import json
from collections import defaultdict

TOKEN = os.environ["DISCORD_TOKEN"]

# Remplacez par votre ID Discord
ADMIN_ID = VotreIDUtilisateurIci

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration par défaut
DEFAULT_CONFIG = {
    "prob_exact": 0.3,  # Probabilité de répondre aux "quoi" dans la phrase
    "prob_end": 1.0,    # Probabilité de répondre aux "quoi" en fin de message
    "admin_ids": [ADMIN_ID],  # Liste des administrateurs
    "max_responses": 2,  # Réponses avant cooldown
    "cooldown": 60,     # Durée du cooldown en secondes
    "reset_window": 30  # Fenêtre temporelle pour les réponses
}

# Chargement/sauvegarde des configurations
def load_config():
    if os.path.exists('feurbot_config.json'):
        try:
            with open('feurbot_config.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    with open('feurbot_config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Initialisation
server_configs = defaultdict(lambda: DEFAULT_CONFIG.copy())
loaded_config = load_config()
for server_id, config in loaded_config.items():
    server_configs[int(server_id)] = config

# États
user_response_counts = defaultdict(lambda: defaultdict(list))
user_cooldowns = defaultdict(dict)

# Réponses
reponses_feur = [
    "feur",
    "https://files.catbox.moe/v5ru9m.mp4",
    "https://files.catbox.moe/gaw473.mp4"
]

reponses_feur_fautes = [
    "f e u r haha il s'est trompé :index_pointing_at_the_viewer::joy:",
    "feru",
    "feür"
]

reponses_feurent = [
    "feurent",
    "feurent :index_pointing_at_the_viewer::joy:"
]

SPECIAL_USERS = {
    123746587317898909: ["toi tg :pointing_at_the_viewer:", "att tg un peu pour voir", "gênant", "https://files.catbox.moe/lirfo9.mp4"]
}

# Fonctions de détection
def normalize_quoi(text):
    text = re.sub(r'<a?:\w+:\d+>', '', text)
    text = re.sub(r'[^a-zA-Z]*$', '', text)
    text = text.lower()
    text = re.sub(r'(.)\1+', r'\1', text)
    text = re.sub(r'mec$', '', text)
    return text.strip()

def check_quoient(text):
    return normalize_quoi(text).endswith('quoient')

def check_quoi_faute(text):
    normalized = normalize_quoi(text)
    fautes = ['quio', 'qoui', 'quioi', 'quioo', 'qouoi', 'quoui', 'quouio', 'quoio', 'qouio', 'qoi']
    return any(normalized.endswith(f) for f in fautes)

def check_quoi(text):
    normalized = normalize_quoi(text)
    variantes = ['quoi', 'koi', 'koa', 'qua', 'quo', 'ko', 'kwa', 'kua', 'koua']
    return any(normalized.endswith(v) for v in variantes)

def contains_exact_quoi(text):
    clean_text = re.sub(r'<a?:\w+:\d+>', '', text)
    return re.search(r'\bquoi\b', clean_text, re.IGNORECASE) is not None

# Commandes
@bot.command()
@commands.guild_only()
async def setprob(ctx, prob_exact: float = None, prob_end: float = None):
    """Définit les probabilités de réponse (!setprob [milieu] [fin])"""
    config = server_configs[ctx.guild.id]

    if ctx.author.id not in config["admin_ids"]:
        await ctx.send("mot de passe ?")
        return

    changes = []
    if prob_exact is not None and 0 <= prob_exact <= 1:
        config["prob_exact"] = prob_exact
        changes.append(f"Milieu de phrase: {prob_exact*100}%")
    if prob_end is not None and 0 <= prob_end <= 1:
        config["prob_end"] = prob_end
        changes.append(f"Fin de message: {prob_end*100}%")

    if changes:
        save_config({str(k): v for k, v in server_configs.items()})
        await ctx.send(f"✅ Probabilités mises à jour:\n" + "\n".join(changes))
    else:
        await ctx.send("❌ Aucun paramètre valide fourni")

@bot.command()
@commands.guild_only()
async def addadmin(ctx, user: discord.User):
    """Ajoute un administrateur (!addadmin @utilisateur)"""
    config = server_configs[ctx.guild.id]

    if ctx.author.id not in config["admin_ids"]:
        await ctx.send("mot de passe ?")
        return

    if user.id not in config["admin_ids"]:
        config["admin_ids"].append(user.id)
        save_config({str(k): v for k, v in server_configs.items()})
        await ctx.send(f"✅ {user.mention} ajouté comme administrateur")
    else:
        await ctx.send("❌ Cet utilisateur est déjà administrateur")

@bot.command()
@commands.guild_only()
async def config(ctx):
    """Affiche la configuration actuelle"""
    config = server_configs[ctx.guild.id]
    embed = discord.Embed(title="Configuration du serveur", color=0x00ff00)
    embed.add_field(
        name="Probabilités",
        value=f"Milieu de phrase: {config['prob_exact']*100}%\nFin de message: {config['prob_end']*100}%",
        inline=False
    )
    embed.add_field(
        name="Limites",
        value=f"Max réponses: {config['max_responses']}/{config['reset_window']}s\nCooldown: {config['cooldown']}s",
        inline=False
    )
    embed.add_field(
        name="Administrateurs",
        value=", ".join([f"<@{id}>" for id in config["admin_ids"]]) or "Aucun",
        inline=False
    )
    await ctx.send(embed=embed)

# Gestion des messages
@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    # Traitement des commandes
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    config = server_configs[message.guild.id]
    user_id = message.author.id
    current_time = time.time()
    content = message.content.strip()

    # Vérification du cooldown
    if user_id in user_cooldowns[message.guild.id]:
        if current_time < user_cooldowns[message.guild.id][user_id]:
            return

    # Gestion spéciale pour les utilisateurs listés
    if user_id in SPECIAL_USERS:
        await message.channel.send(f"{message.author.mention} {random.choice(SPECIAL_USERS[user_id])}")
        user_cooldowns[message.guild.id][user_id] = current_time + config["cooldown"]
        return

    # Détection des triggers
    response = None
    response_type = None

    if check_quoient(content) and random.random() < config["prob_end"]:
        response = random.choice(reponses_feurent)
    elif check_quoi_faute(content) and random.random() < config["prob_end"]:
        response = random.choice(reponses_feur_fautes)
    elif check_quoi(content) and random.random() < config["prob_end"]:
        response = random.choice(reponses_feur)
    elif contains_exact_quoi(content) and random.random() < config["prob_exact"]:
        response = re.sub(r'\bquoi\b', 'feur', content, flags=re.IGNORECASE)

    if response:
        # Gestion du taux de réponse
        counts = user_response_counts[message.guild.id][user_id]
        counts = [t for t in counts if current_time - t < config["reset_window"]]
        counts.append(current_time)
        user_response_counts[message.guild.id][user_id] = counts

        if len(counts) > config["max_responses"]:
            await message.channel.send(f"bon tg maintenant {message.author.mention}")
            user_cooldowns[message.guild.id][user_id] = current_time + config["cooldown"]
        else:
            await message.channel.send(response)

@bot.event
async def on_ready():
    print(f'{bot.user.name} connecté et prêt!')

bot.run(TOKEN)
