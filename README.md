# 🤖 Quoifeur-bot pour Discord

Un bot Discord très simple qui répond dès qu'un message se termine par « quoi ».

Développé avec Python, utilisable avec Docker.

## ⚙️ Création de l'application sur Discord

1. **Accéder au portail développeur :**  
   [https://discord.com/developers/applications](https://discord.com/developers/applications)

2. **Créer une nouvelle application :**  
   Cliquez sur "New Application", donnez-lui un nom (par ex. `BotQuoiFeur`) et validez.

3. **Créer un bot :**  
   - Allez dans l’onglet **"Bot"**
   - Cliquez sur **"Add Bot"**, puis confirmez.

4. **Copier le token du bot :**  
   - Dans l'onglet **"Bot"**, cliquez sur **"Reset Token"** si nécessaire, puis copiez-le.
   - **⚠️ Gardez ce token secret.** Notez le quelque part, il sera utile et devra être noté dans le fichier .env uniquement.
   - Toujours sur cette page, en dessous activez les 3 options qui concernent les Presence Update, GUILD_MEMBERS et message content, comme ceci : ![image](https://github.com/user-attachments/assets/ea1a9c6b-4daa-47fa-95b4-a95d3f23558a)


5. **Donner les permissions au bot :**  
   - Allez dans l'onglet **"Installation" > "Default Install Settings"**
   - Sélectionnez ces paramètres : ![image](https://github.com/user-attachments/assets/0067c7be-1ccb-45d4-8ba4-d4651fd4577d)
   - Dans Install Link, un lien sera généré pour pouvoir inviter le bot sur un serveur (mais il ne pourra rien faire tant qu'il ne sera pas en train de fonctionner).


---

Si vous voulez simplement vous amuser quelques minutes et héberger le bot sur votre PC en local, c'est possible, mais vous devrez être capable de lancer des scripts python sur votre machine locale. Il suffit de télécharger le fichier botquoifeur.py sur le repo et remplacer TOKEN = os.environ["DISCORD_TOKEN"] par TOKEN = VotreTokenSansGuillemets, pareil dans la dernière commande bot.run, mais avec des guillemets cette fois-ci, donc : bot.run("VotreTokenAvecDesGuillemets").

Il n'est absolument pas recommandé de laisser son token en clair par soucis de sécurité, pensez à le réinitialiser directement sur le portail développeur de Discord si jamais vous pensez avoir pris des risques en ayant partagé ou fait fuiter le token.


Si vous souhaitez l'utiliser avec Docker, vous pouvez simplement cloner le repo, il faudra indiquer votre propre token dans un fichier .env

## 🔐 Variables d’environnement

Créez un fichier `.env` dans le dossier du projet et inscrivez : DISCORD_TOKEN=VotreTokenSansGuillemets


## Utilisation du bot

```
make run     # Démarre le bot
make build   # Rebuild + start
make stop    # Stoppe le bot
```

Vous pouvez démarrer le bot avec la commande : `make up`, la commande `make update` permet de rebuild l'image pour prendre en compte les éventuels changements que vous pourrez introduire dans le projet.
Pour éteindre le bot, vous pouvez utiliser la commande `make down`. Ces commandes sont des raccourcis et vous pouvez voir à quoi elles correspondent dans le fichier Makefile.



## Ajouter des messages

Le bot change de message aléatoire et sélectionne un message écrit (« feur »), ou un meme en vidéo hébergé au préalable (j'aime bien catbox.moe). Si vous souhaitez les changer ou en ajouter, vous pouvez le faire dans le fichier botquoifeur.py, à partir de la ligne 16 chaque ligne est un message que le bot pourra utiliser (veillez à bien respecter le format, la phrase ou le lien entre guillemets, avec une virgule avant le retour à la ligne sauf pour la dernière entrée).


## Licence
Aucune, j'ai juste vibecodé. Fait par moi.
