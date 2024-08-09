from pytube import YouTube
from telegram import Bot
from sqlite3 import connect
import os
import datetime as date
TOKEN = ""
bot = Bot(token=TOKEN)
data_base = connect("telegram_bot_db.db")
cursor = data_base.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS bot_data(name TEXT NOT NULL, data BLOB)
"""
)


def insert_data(name: str, data: str):
    with open(data, "rb") as data_file:
        get_data = data_file.read()
    cursor.execute("INSERT INTO bot_data(name, data) VALUES(?, ?)", (name, get_data))
    data_base.commit()


async def get_free_data(request_name: str, chat_id: int):
    data_tag = [
        "reward_code"
        "demo_free_surf",
        "compte_paypal",
        "compte_free_surf",
        "compte_djamo",
        "carte_credit",
        "abonnement_yourfreedom",
        "partage_freesurf",
    ]
    hint = 1
    if request_name in data_tag:
        cursor.execute("SELECT * FROM bot_data WHERE name = ?", (request_name,))
        for data in cursor.fetchall():
            name, data_content = data
            file_path = f"{request_name}_{hint}.mp4"
            hint += 1
            with open(file_path, "wb") as file:
                file.write(data_content)
            with open(file_path, "rb") as file:
                await bot.send_video(chat_id=chat_id, video=file,protect_content=True)
            os.remove(file_path)


async def get_data(request_name: str, chat_id:int):
    values = [
        "html",
        "python",
        "java",
        "php",
        "hacking",
        "css",
        "c#",
        "c++",
        "c",
        "javascript",
        "roadmap_c++",
        "roadmap_java",
        "roadmap_php",
        "roadmap_html",
        "roadmap_hack"
        "roadmap_c#",
        "roadmap_css",
        "roadmap_javascript",
        "roadmap_python",
    ]
    request = request_name.removeprefix("/")
    if request in values:
        date = None
        await bot.send_message(chat_id=chat_id, text=f"Cette ressoucre sera disponible le {date}",protect_content=True)
        hint = 1
        cursor.execute("SELECT * FROM bot_data WHERE name = ?", (request,))
        for data in cursor.fetchall():
            name, data_content = data
            file_path = f"{request}_{hint}.pdf"
            hint += 1
            with open(file_path, "wb") as file:
                file.write(data_content)
            with open(file_path, "rb") as file:
                await bot.send_document(chat_id=chat_id, document=file,protect_content=True)
            os.remove(file_path)


async def get_free_surf_config(chat_id: int):
    request_name = "yourfreedom_pack(video_config+apk)"
    #await bot.send_message(chat_id=chat_id, text=f"c'est la requête {request_name}")
    cursor.execute("SELECT * FROM bot_data WHERE name = ?", (request_name,))
    name, data_content = cursor.fetchone()
    file_path = f"{request_name}.zip"
    with open(file_path, "wb") as file:
        file.write(data_content)
    with open(file_path, "rb") as file:
        await bot.send_document(chat_id=chat_id, document=file,protect_content=True)
    os.remove(file_path)


def explained_free_surf(name: str):
    return f"""
Bienvenue dans la rubrique free surf (connexion libre) ou 'illimité' {name}.
De nos jours, avoir accès à internet est vraiment coûteux, ce qui fait que plusieurs personnes souffrent pour s'en procurer. Moi aussi, j'étais dans ce pétrin jusqu'à ce que je découvre cette application. Mes problèmes se sont résolus à moindre coût.
Bonne nouvelle : que ce soit partout dans le monde, vous avez la possibilité de naviguer librement avec cette méthode sans dépenser énormément d'argent 😃. Bref, vous l'aurez compris, avant de commencer, j'aimerais vous dire que je réside en Côte d'Ivoire. Pour cet exemple, j'utiliserai les moyens de transactions et de paiement ainsi que le réseau disponible dans mon pays. Mais ne vous inquiétez pas, cette application fonctionne dans tous les pays.
PS : 🎯 Une petite suggestion, si dans votre pays vous disposez d'un réseau "ORANGE", utilisez ce réseau car il offre une bonne vitesse de connexion avec cette application.

Pré-requis :
Pour utiliser cette application et en profiter énormément, vous aurez besoin d'un abonnement. Vous savez que pour se procurer de la connexion, c'est toujours payant. Avec cette méthode, c'est moins cher et illimité dans le temps selon vos besoins. Si vous n'êtes pas satisfait, vous pouvez demander un remboursement. Sans plus tarder, vous aurez besoin de :

📌 D'UN COMPTE PAYPAL : si vous ne savez pas comment vous procurer un compte PayPal étant en Afrique, je vous suggère de cliquer sur la commande /compte_paypal.

📌 D'UN COMPTE YOURFREEDOM : pour savoir comment créer un compte YourFreedom, entrez la commande /compte_free_surf.

📌 D'UN COMPTE DJAMO (si vous êtes en Côte d'Ivoire) : pour vous procurer un compte Djamo, entrez la commande /compte_djamo. Pour me soutenir et m'encourager à vous fournir une énorme aide dans le futur, je vous suggère d'utiliser ce code d'invitation 😌: KKYBO

📌 DE L'APPLICATION YOURFREEDOM ET LA CONFIGURATION : pour télécharger l'application et savoir comment la configurer, entrez la commande : /freesurf_config.

📌 D'UN ABONNEMENT YOURFREEDOM : pour savoir comment faire un abonnément vous pouvez entrez la commande : /abonnement_yourfreedom

📌 DEMO FREE SURF : pour voir une démo en guise de preuve, tapez la commande : /demo_free_surf.

📌 AUTRE(facultatif pour Côte d'Ivoire et Sénagal): si vous ête dans un pays où vous ne savez pas comment faire pour avoire une carte viruelle ou bancaire pour vos achat en ligne vous pouvez entrez la commande : /carte_credit

Congratulations ,Enjoy {name} 🎁.
"""


def youtube_download_single_video(url: str):
    if url.startswith("https://www.youtube.com"):
        get_url = YouTube(url)

        def on_download_progress(stream, chunk, bytes_remaining):
            bytes_downloaded = stream.filesize - bytes_remaining
            percent = bytes_downloaded * 100 / stream.filesize
            # Vous pouvez envoyer un message de progression ici si nécessaire
            # bot.send_message(chat_id=update.message.chat_id, text=f"Progression : {int(percent)}%")

        get_url.register_on_progress_callback(on_download_progress)
        get_url.streams.get_by_itag(133).download()
    else:
        return


def handle_msgs(text: str, user_name: str):
    input_msg = text.lower()
    if input_msg == "/help_user":
        return f"""
🧾 Bienvenue dans le guide {user_name}.

Mon but est de vous fournir un maximum de ressources pour vous aider dans votre apprentissage.

Découvrez notre bot Telegram révolutionnaire ! 🚀

Notre bot est conçu pour aider les utilisateurs en leur offrant une gamme de services essentiels :

- Cours de programmation (applications & web)
- Hacking éthique
- Connexion internet illimitée
- Conseils pour débutants en informatique
- Assistente Virtuelle Gratuit
- Et bien plus à venir !

PS : Et tout cela est à vous gratuitement 🎁. Tout ce que vous avez à faire, c'est de taper la commande /access_learn.
"""
    # elif input_msg.return "Requête non prise en charge 😞"
    # - Téléchargement de ressources YouTube (vidéos & playlists)


def doc(name: str):
    return f"""
Bienvenue dans la documentation des commandes de votre bot {name}. Voici une liste des commandes disponibles et leur utilisation :

1. /compte_djamo - Créer un compte Djamo
   Utilisez cette commande pour obtenir un code d'invitation et créer un compte Djamo.

2. /codes_roadmap - Feuilles de route de programmation
   Obtenez des feuilles de route pour différents langages de programmation.

3. /compte_free_surf - Créer un compte FreeSurf
   Utilisez cette commande pour créer un compte FreeSurf via un lien de parrainage.

4. /help - Aide
   Affiche une liste des commandes disponibles et leur utilisation.

5. /about - À propos
   Obtenez des informations sur le bot et son créateur.

6. /access_learn - Accéder à l'apprentissage
   Accédez à des ressources d'apprentissage pour différents sujets.

7. /assistente_virtuelle - Assistante virtuelle
   Interagissez avec l'assistante virtuelle pour être autonome dans votre apprentissage.

8. /cours_code - Choisir la langue de programmation
   Choisissez une langue de programmation pour obtenir des ressources et des tutoriels.
   
9. /hacking - Hacking éthique
    Obtenez des ressources et des informations sur le hacking éthique.

10. /abonnement_yourfreedom - Abonnement YourFreedom
    Gérez votre abonnement au service YourFreedom.

11. /free_surf - FreeSurf
    Accédez aux services FreeSurf.

12. /freesurf_config - APK FreeSurf + La configuration
    Téléchargez l'APK pour le service FreeSurf ainsi que la configuration.

13. /compte_paypal - PayPal
    Création et Gestion de vos transactions PayPal.

14. /carte_credit - Carte de crédit
    Obtention et Gestion de vos informations de carte de crédit.

15. /demo_free_surf - Démo FreeSurf
    Regardez une démonstration du service FreeSurf.

16. /hacking_roadmap - Feuille de route de hacking
    Obtenez une feuille de route pour apprendre le hacking.

17. /help_novice - Aide pour les novices
    Obtenez de l'aide et des conseils pour les débutants.

18. /start - Démarrer
    Démarrez une nouvelle session avec le bot.

19. /help_user - Aide utilisateur
    Obtenez de l'aide spécifique pour les utilisateurs.

20. /partage_freesurf - Partagé sa connexion
    Partagé votre connexion free surf (vpn) avec votre ordinateur ou autre téléphones
"""

#9. /youtube_downloader - Téléchargeur YouTube
#    Utilisez cette commande pour télécharger des vidéos YouTube.

"""

22. /contact_admin - contactez l'administration
    pour des problemes ou des questions
    
23. /reward_code - Obtention de votre code
    free surf
Pour toute question ou assistance supplémentaire, n'hésitez pas à utiliser la commande /help.
"""
