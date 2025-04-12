
# 🤖 Quoi ? Feur-bot pour Discord

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


## 🤖 Utilisation du bot

```
make run     # Démarre le bot
make build   # Rebuild + start
make stop    # Stoppe le bot
```

Vous pouvez démarrer le bot avec la commande : `make up`, la commande `make update` permet de rebuild l'image pour prendre en compte les éventuels changements que vous pourrez introduire dans le projet.
Pour éteindre le bot, vous pouvez utiliser la commande `make down`. Ces commandes sont des raccourcis et vous pouvez voir à quoi elles correspondent dans le fichier Makefile.


## 🖥️ Fonctions du bot

Actuellement, le bot a plusieurs fonctions.

 1. **Répondre simplement à un message qui se termine par « quoi »** ou des variantes (« quoua, koa, koi, koua, etc ...)
 2. **Répondre à des fautes de frappes**, si le bot détecte un mot qui semble être une faute, par exemple qoi, ou quio, il utilisera une autre liste de mots pour répondre (par exemple : eur, fuer, etc)
 3. **Détecter lorsque le mot « quoi » est présent au début ou au milieu d'une phrase** et la répète en remplaçant toutes les occurrences de « quoi » par « feur ».
 4. **Réagit spécialement lorsqu'il détecte un message qui se termine par quoient**, probablement aucune utilisation dans la vie réelle, mais c'est fun.
 5. **Un système de pause, pour éviter le spam.** Par défaut, si l'utilisateur utilise le bot plus de 2 fois dans une fenêtre de 30 secondes (par défaut), il réagira différemment à la 3ème utilisation et mettra l'utilisateur dans une période de cooldown d'une minute avant de pouvoir à nouveau réagir à ses messages.
 6. **Une fonction d'utilisateurs spéciaux** : ici, vous pouvez indiquer l'ID d'un utilisateur pour qui vous voulez que le bot réagisse autrement. Lorsque le bot devra réagir à un mot provenant de cet utilisateur, il utilisera un autre dictionnaire.

## ⌨️ Modifier la configuration

Vous pouvez ouvrir le fichier botquoifeur.py et modifier certains paramètres à votre guise. Tout est commenté pour que vous puissiez savoir ce que vous êtes en train de changer.

**À partir de la ligne 18**, ces variables permettent de configurer la fenêtre de temps de spam, le nombre de réponses maximum dans cette fenêtre, le temps de cooldown une fois la limite dépassée, ainsi que les ID des utilisateurs spéciaux (accompagnées de leurs réponses spéciales).

**À partir de la ligne 30**, il y a 3 blocs différents, chaque bloc correspond à une liste de mots que le bot utilisera selon les cas de figures déjà décrits dans la liste des fonctions du bot. Si vous ajoutez des mots ou des phrases, veillez à strictement respecter la nomenclature, auquel cas le bot pourrait ne plus fonctionner du tout.



## 📕 Licence
Aucune, j'ai juste vibecodé. Fait par ~~chatgpt~~ DeepSeek, sous ma supervision (au tout début c'était avec ChatGPT mais DeepSeek fonctionne vraiment 100x mieux).
