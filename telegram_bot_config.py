from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    Bot,
)
import telegram.ext as te
import tracemalloc
import answer_bot as answer
import sqlite3 as sqlite
import uuid as uid
# import datetime as date
tracemalloc.start()

print("Bot started ...")

TOKEN =""
bot = Bot(token=TOKEN)
# Créez la connexion à la base de données
data_user = sqlite.connect('user_data.db')

# Créez un curseur
cursor = data_user.cursor()

# Créez la table si elle n'existe pas déjà
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE,
                    full_name TEXT,
                    balance REAL DEFAULT 0,
                    referrer_id INTEGER,
                    public_key TEXT UNIQUE,
                    CONSTRAINT fk_referrer FOREIGN KEY (referrer_id) REFERENCES users(id)
                )"""
)
data_user.commit()
def generate_public_key():
    return str(uid.uuid4())


def register_user(telegram_id: int, full_name: str, referrer_id: int = None):
    try:
        public_key = generate_public_key()
        cursor.execute('''INSERT OR IGNORE INTO users (telegram_id, full_name, referrer_id, public_key)
                        VALUES (?, ?, ?, ?)''', (telegram_id, full_name, referrer_id, public_key))
        data_user.commit()
    except sqlite.IntegrityError:
        # Si l'ID utilisateur existe déjà, mettez à jour le nom complet
        cursor.execute(
            """UPDATE user_data SET full_name = ? WHERE telegram_id = ?""",
            (full_name, telegram_id),
        )
        data_user.commit()
    except Exception as e:
        print(f"Erreur register user : {e}")

def update_balance(telegram_id:int, amount:float,options:str):
    if options.lower() == "up":
        cursor.execute('''UPDATE users SET balance = balance + ? WHERE telegram_id = ?''', (amount, telegram_id))
    elif options.lower() == "down":
        cursor.execute('''UPDATE users SET balance = balance - ? WHERE telegram_id = ?''', (amount, telegram_id))
    data_user.commit()

async def handle_start(update: Update, context: te.CallbackContext):
    try:
        args = context.args
        referrer_public_key = None
        if args:
            referrer_public_key = args[0]
            cursor.execute('''SELECT id, telegram_id FROM users WHERE public_key = ?''', (referrer_public_key,))
            result = cursor.fetchone()
            referrer_id = result[0] if result else None
            referrer_telegram_id = result[1] if result else None
        else:
            referrer_id = None
            referrer_telegram_id = None

        telegram_id = update.message.from_user.id
        full_name = f"{update.message.from_user.first_name} {update.message.from_user.last_name or ''}".strip()

        register_user(telegram_id, full_name, referrer_id)

        if referrer_id and referrer_telegram_id != telegram_id:
            update_balance(referrer_id, 10,"up")
        await update.message.reply_text(f"""🎉 Bienvenue {full_name}, mon nom est Tools Bot et je suis ici pour vous aider. Si vous désirez savoir comment m'utiliser, entrez la commande /help .""")
        await context.bot.send_message(
            chat_id=5728776632,
            text=f"""Nouveau utilisateur {full_name}""",)
    except Exception as e:
        print(f"Erreur dans handle_start: {e}")


async def handle_paypal(update: Update, context: te.CallbackContext):
    try:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Crée un Compte Paypal",
                    url="https://paypal.com/ae",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await answer.get_free_data("compte_paypal", chat_id=update.effective_chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.message.from_user.first_name} pour crée votre compte paypal cliquez sur le bouton ci-dessous\nNB: Veuillez utilisé la vidéo comme un guide",
            reply_markup=reply_markup,
        )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réssayer encore.
""",
        )


async def handle_cb(update: Update, context: te.CallbackContext):
    try:
        await answer.get_free_data("carte_credit", chat_id=update.effective_chat.id)
        #print("carte credit")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )

async def freesurf_config(update: Update, context: te.CallbackContext):
    try:
        await update.message.reply_text(""""
🚧(Pétite Suggestion pour vous)

Avant de continuer veuillez vous assurez que
vous avez remplire ses conditions :

-avoir crée un compte paypal ,sinon cliquez ici : /compte_paypal
-avoir crée un compte free surf ,sinon cliquez ici : /compte_free_surf
-avoir liée sa carte de crédit a son compte paypal ,sinon cliquez ici : /compte_paypal
-avoir crée et réchargé sa carte de crédit ,sinon cliquez ici : /compte_djamo
-avoir achété un abonnément , sinon cliquez ici : /abonnement_freesurf
""")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
Il faut suivre la vidéo attentivement.\n
PS :🎯 lorsque vous arrivez sur la partie qui présente un tableau, veuillez choisir une préférence (PREF) supérieure ou égale à 8.
""",
        )

        await answer.get_free_surf_config(chat_id=update.effective_chat.id)
        #print("free surf config")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def compte_freesurf(update: Update, context: te.CallbackContext):
    try:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Crée un Compte",
                    url="https://www.your-freedom.net/?referer=31573181",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await answer.get_free_data("compte_free_surf", chat_id=update.effective_chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.message.from_user.first_name} pour crée votre compte cliquez sur le bouton ci-dessous",
            reply_markup=reply_markup,
        )

        # print("compte_free_surf")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def codes_roadmap(update: Update, context: te.CallbackContext):
    try:
        keyboards = [
            [KeyboardButton("/roadmap_c++"), KeyboardButton("/roadmap_java")],
            [KeyboardButton("/roadmap_php"), KeyboardButton("/roadmap_html")],
            [KeyboardButton("/roadmap_c#"), KeyboardButton("/roadmap_css")],
            [KeyboardButton("/roadmap_javascript"),KeyboardButton("/roadmap_python")],
            #[],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboards, one_time_keyboard=False, resize_keyboard=True
        )
        #print("codes roadmap")
        await update.message.reply_text(
            f"{update.message.from_user.first_name} cette fonctionnalité est en cours de maintenance. Dès qu'elle sera disponible, je te ferai savoir.",
            reply_markup=reply_markup,
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def compte_djamo(update: Update, context: te.CallbackContext):
    try:
        await answer.get_free_data("compte_djamo", chat_id=update.effective_chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.message.from_user.first_name} pour me soutenir, utilisez ce code d'invitation 😌: KKYB0",
        )
        #print("compte_djamo")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def help_cmd(update: Update, context: te.CallbackContext):
    try:
        keyboards = [
            [KeyboardButton("/help_user"), KeyboardButton("/about")],
            [KeyboardButton("/documentation")],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboards, resize_keyboard=True, one_time_keyboard=False
        )
        await update.message.reply_text(
            "📌Avez-vous besoin d'aide ? , pour voir la liste des commandes ainsi que leurs rôle entrez la commande /documentation", reply_markup=reply_markup
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def doc(update: Update, context: te.CallbackContext):
    await update.message.reply_text(answer.doc(update.message.from_user.first_name))


async def about(update: Update, context: te.CallbackContext):
    try:
        user_name = update.message.from_user.first_name
        await update.message.reply_text(
            f"""
Présentation de Tools Bot

{user_name},

Tools Bot est conçu pour aider un grand nombre de personnes en offrant divers services.

Vous pouvez apprendre la programmation d’applications et de sites web, explorer le hacking éthique, profiter d’une connexion internet illimitée, bénéficier d’une assistance virtuelle pour affiner vos compétences, et bien plus encore.

De plus, nous fournissons des conseils pratiques pour les débutants en informatique .

Notre objectif est de rendre l’informatique accessible à tous et de vous accompagner dans votre apprentissage. Le créateur de Tools Bot n’a pas de but lucratif, mais vise à répondre aux problématiques rencontrées par de nombreuses personnes dans ce monde interconnecté. Nous visons à toucher et aider un grand nombre de personnes.

Pour que l’objectif de Tools Bot devienne une réalité, nous vous prions, cher {user_name}, d’inviter le maximum de personnes souhaitant bénéficier des avantages que vous avez actuellement.

Afin de nous motivé à vous aider encore plus dans le future .

Cordialement,
L’équipe Tools Bot
"""
        )
        #et permettons le téléchargement de vidéos et de playlists YouTube
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )

# Mais ce n’est pas tout : à chaque fois que vous invitez une personne avec votre lien de parrainage, vous cumulez des TB. Ces TB vous seront utiles pour obtenir un code fourni par Tools Bot, qui vous permettra d’activer votre compte Free Surf et de profiter d’une connexion illimitée pendant 14 jours si vous atteignez 100 TB. Pour chaque personne invitée utilisant votre lien, vous recevrez 10 TB.
# Pour consulter votre compte et visualiser votre lien de parrainage, entrez la commande : /my_account .
async def handle_msg(update: Update, context: te.CallbackContext):
    try:
        await update.message.reply_text(
            answer.handle_msgs(update.message.text, update.message.from_user.first_name)
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def access_learn(update: Update, context: te.CallbackContext):
    try:
        keyboards = [
            [KeyboardButton("/cours_code"), KeyboardButton("/hacking")],
            [KeyboardButton("/free_surf"), KeyboardButton("/help_novice")],
            #[KeyboardButton("/youtube_downloader")],
            [KeyboardButton("/assistente_virtuelle")],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboards, one_time_keyboard=False, resize_keyboard=True
        )
        await update.message.reply_text(
            f"En attente de votre requête {update.message.from_user.first_name}",
            reply_markup=reply_markup,
        )
        #print("access_learn")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def assistente_virtuelle(update: Update, context: te.CallbackContext):
    try:
        keyboard = [
            InlineKeyboardButton("Assistente Virtuelle", url="https://chatgpt.com/")
        ]
        reply_markup = InlineKeyboardMarkup([keyboard])
        await update.message.reply_text(
            f"{update.message.from_user.first_name}, votre assistance virtuelle est prête. Cliquez sur le bouton ci-dessous pour démarrer vos requêtes.",
            reply_markup=reply_markup,
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def choose_lang(update: Update, context: te.CallbackContext):
    try:
        keyboards = [
            [KeyboardButton("/python"), KeyboardButton("/java")],
            [KeyboardButton("/html"), KeyboardButton("/css")],
            [KeyboardButton("/php"), KeyboardButton("/c++")],
            [KeyboardButton("/c"), KeyboardButton("/c#")],
            [KeyboardButton("/javascript")],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboards, resize_keyboard=True, one_time_keyboard=False
        )
        await update.message.reply_text(
            f"""
🎯 {update.message.from_user.first_name}
PS: Si vous êtes débutant dans l'univers de la programmation,
je vous suggère d'entrer la commande /help_novice pour savoir
comment débuter et quel langage de programmation choisir
afin de ne pas être découragé. Dans le cas contraire, vous
pouvez choisir votre langage.
""",
            reply_markup=reply_markup,
        )
        #print("choose_lang")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def handle_get_data(update: Update, context: te.CallbackContext):
    try:
        await answer.get_data(update.message.text, update.effective_chat.id)
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def download_ytb_cmd(update: Update, context: te.CallbackContext):
    try:
        await update.message.reply_text(
            f"{update.message.from_user.first_name} cette fonctionnalité est en cours de maintenance. Dès qu'elle sera disponible, je te ferai savoir."
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def hacking_ethique(update: Update, context: te.CallbackContext):
    try:
        await answer.get_data(update.message.text, update.effective_chat.id)
        # print("hacking_ethique")
    except:
        """await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""#{update.message.from_user.first_name}
# une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
# Réssource sera disponible le {date.datetime(2024, 8, 8, 24, 00, 00)}
""",
        )"""

async def handle_abonnement(update: Update, context: te.CallbackContext):
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""
🚧(Pétite Suggestion pour vous)

Avant de continuer veuillez vous assurez que
vous avez remplire ses conditions :

-avoir crée un compte paypal ,sinon cliquez ici : /compte_paypal
-avoir crée un compte free surf ,sinon cliquez ici : /compte_free_surf
-avoir liée sa carte de crédit a son compte paypal ,sinon cliquez ici : /compte_paypal
-avoir crée et réchargé sa carte de crédit ,sinon cliquez ici : /compte_djamo

Pour achéter un abonnnement je vous
suggère de faire ceux-ci :

1-Choisir uniquement selon vos bésoins
   les differents abonnéments qui ont pour
   titre ( Mobile plus)

2-Si vous n'avez pas trop de moyens choisissez
   uniquement les differents abonnément
   qui ont pour titre (Mobile)

3-Vous pouvez convertir les differents
   prix dans votre dévise

4-Pour l'abonnément veuillez tout d'abord
   vous connectez a votre compte paypal

1-Remarquer : - bien pour un mois de connexion illimité
vous dépensez 651.10 FCFA + 500FCFA de frais
avec l'abonnement mobile (regardez dans les images fournir
pour bien visualisé et savoir où vous pouvez convertir les
differents prix d'abonnément dans votre dévise)

2-Remarquer : - bien pour un mois de connexion illimité
vous dépensez 1302.20 FCFA + 500FCFA de frais
avec l'abonnement mobile plus (regardez dans les images fournir
pour bien visualisé et savoir où vous pouvez convertir les
differents prix d'abonnément dans votre dévise)

NB :veuillez mêttre des frais supplementaire
d'au moins 500 FCFA pour les pays de la
CEDEAO, qui inclus des frais de réjet pour
ceux qui utilise DJAMO , ainsi que pour le
payement de l'abonnément cet motant (500 fcfa) ne
sera pas totalement débité mais c'est pour que vous
ne puissiez pas ressentir de la frustration comme
moi lorsque j'avais essayé pour la premier fois
d'effectué un abonnément .
""")
        keyboard = [
            [
                InlineKeyboardButton(
                    "Abonnement free surf",
                    url="https://www.your-freedom.net/?referer=31573181",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await answer.get_free_data("abonnement_yourfreedom", update.effective_chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.message.from_user.first_name} pour achetez un abonnement free surf(yourfreedom) veuillez cliquez sur le bouton ci-dessous",
            reply_markup=reply_markup,
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def free_surf(update: Update, context: te.CallbackContext):
    try:
        keyboards = [
            [KeyboardButton("/freesurf_config"), KeyboardButton("/compte_paypal")],
            [KeyboardButton("/demo_free_surf"), KeyboardButton("/compte_djamo")],
            [KeyboardButton("/compte_free_surf"), KeyboardButton("/carte_credit")],
            [KeyboardButton("/abonnement_freesurf")],
            [KeyboardButton("/partage_freesurf")],
        ]
        name = update.message.from_user.first_name
        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboards, resize_keyboard=True, one_time_keyboard=False
        )
        await update.message.reply_text(
            answer.explained_free_surf(name), reply_markup=reply_markup
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def demo_freesurf(update: Update, context: te.CallbackContext):
    try:
        await answer.get_free_data("demo_free_surf", chat_id=update.effective_chat.id)
        #print("demo_freesurf")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


"""async def help_novice_codage(update: Update, context: te.CallbackContext):
    try:
        await update.message.reply_text(
            f"{update.message.from_user.first_name} cette fonctionnalité est en cours de maintenance. Dès qu'elle sera disponible, je te ferai savoir."
        )
        print("help_novice")
    except Exception as e:
        print(f"Error in help_novice: {e}")"""


async def helper_novice(update: Update, context: te.CallbackContext):
    try:
        keyboards = [
            [KeyboardButton("/hacking_roadmap"), KeyboardButton("/codes_roadmap")],
            # [KeyboardButton("/help_novice")],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboards, one_time_keyboard=False, resize_keyboard=True
        )
        await update.message.reply_text(
            f"En attente de votre requête {update.message.from_user.first_name}",
            reply_markup=reply_markup,
        )
        #print("help novice")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )


async def partage_freesurf(update: Update, context: te.CallbackContext):
    try:

        await update.message.reply_text(f""""
🚧(Pétite Suggestion pour vous)

Avant de continuer veuillez vous assurez que
vous avez remplire ses conditions :

-avoir crée un compte paypal ,sinon cliquez ici : /compte_paypal
-avoir crée un compte free surf ,sinon cliquez ici : /compte_free_surf
-avoir liée sa carte de crédit a son compte paypal ,sinon cliquez ici : /compte_paypal
-avoir crée et réchargé sa carte de crédit ,sinon cliquez ici : /compte_djamo
-avoir achété un abonnément , sinon cliquez ici : /abonnement_freesurf

😀 Bonvisionnage {update.message.from_user.first_name}"
        """)
        await answer.get_free_data("partage_freesurf", chat_id=update.effective_chat.id)
        #print("partage_freesurf")
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""{update.message.from_user.first_name}
une erreur est survenue lors du traitement de votre requête veuillez réessayer encore.
""",
        )

app = te.Application.builder().token(TOKEN).build()
app.add_handler(te.CommandHandler("start", handle_start))
app.add_handler(te.CommandHandler("freesurf_config", freesurf_config))
app.add_handler(te.CommandHandler("compte_paypal", handle_paypal))
app.add_handler(te.CommandHandler("carte_credit", handle_cb))
app.add_handler(te.CommandHandler("compte_djamo", compte_djamo))  #
app.add_handler(te.CommandHandler("help_novice", helper_novice))  #
app.add_handler(te.CommandHandler("codes_roadmap", codes_roadmap))  #
app.add_handler(te.CommandHandler("compte_free_surf", compte_freesurf))  #
app.add_handler(te.CommandHandler("help", help_cmd))
app.add_handler(te.CommandHandler("documentation", doc))
app.add_handler(te.CommandHandler("about", about))
app.add_handler(te.MessageHandler(te.filters.Regex(r"(help_user|start)"), handle_msg))
app.add_handler(te.CommandHandler("access_learn", access_learn))
app.add_handler(te.CommandHandler("assistente_virtuelle", assistente_virtuelle))
app.add_handler(te.CommandHandler("cours_code", choose_lang))
app.add_handler(
    te.MessageHandler(
        te.filters.Regex(
            r"(c#|c\+\+|css|javascript|c|php|html|python|hacking|java|roadmap_c\+\+|roadmap_java|roadmap_php|roadmap_html|roadmap_c#|roadmap_css|roadmap_javascript|roadmap_python|roadmap_hack)"
        ),
        handle_get_data,
    )
)
# hacking_roadmap keyword ,
# app.add_handler(te.CommandHandler("youtube_downloader", download_ytb_cmd))
app.add_handler(te.CommandHandler("hacking", hacking_ethique))
app.add_handler(te.CommandHandler("abonnement_freesurf", handle_abonnement))
app.add_handler(te.CommandHandler("free_surf", free_surf))
app.add_handler(te.CommandHandler("demo_free_surf", demo_freesurf))
# app.add_handler(te.CommandHandler("hacking_roadmap", roadmap_hack))
app.add_handler(te.CommandHandler("partage_freesurf", partage_freesurf))
app.run_polling(poll_interval=5)
# app.add_handler(te.CommandHandler("help_novice", help_novice_codage))


# build cmd for share connexion vpn
# condif free surf + carte crédit

"""'async def roadmap_hack(update: Update, context: te.CallbackContext):
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.message.from_user.first_name} cette fonctionnalité est en cours de maintenance. Dès qu'elle sera disponible, je te ferai savoir."
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.message.from_user.first_name}, une erreur est survenue lors du traitement de votre requête. Veuillez réessayer encore.\nRéssource sera disponible le {date.datetime(2024, 8, 8, 24, 00, 00)}",
        )"""
