import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from graphBotCode import graphBot

import graphBotCode

LAT = 41.3887901
LONG = 2.1589899

GB = graphBot()


# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola benvingut! Sóc un GRAPHBOT!")
    bot.send_message(chat_id=update.message.chat_id, text="Obtenint les dades actualitzades del mapa a les ciutats...")
    bot.send_message(chat_id=update.message.chat_id, text="És recomanable que enviis la teva localització per ajustar els mapes amb precisió (mitjançant el clip)")
    GB.inicialitzarDades()
    bot.send_message(chat_id=update.message.chat_id, text="Dades obtingudes amb èxit! Selecciona una de les opcions disponibles per començar.")
    bot.send_message(chat_id=update.message.chat_id, text="I recorda sempre començar amb la creació d'un graph amb /graph <distancia> <poblacio>")
    bot.send_message(chat_id=update.message.chat_id, text="En cas de dubte, a /help trobaràs tot el que necessitis.")


def help(bot, update):
    info = '''
En _GRAPHBOT_  tens disponibles les següents comandes:

- /start: _Iniciar la conversa amb el BOT._
- /author: Nom i email de l'autor.
- /exemple: Mostra un possible exemple de les possiblitats del bot
- /graph ⟨distance⟩ ⟨population⟩: Utilitzi un nou graf.
- /nodes: Nombre de nodes del graf.
- /edges: Nombre d'arestes en el graf.
- /components: Nombre de components connexs en el graf.
- /plotpop ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]: Mostra una mapa amb totes les ciutats del graf a distància menor o igual que ⟨dist⟩ de ⟨lat⟩,⟨lon⟩.
- /plotgraph ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]: Mostra una mapa amb totes les ciutats del graf a distància menor o igual que ⟨dist⟩ de ⟨lat⟩,⟨lon⟩ i les arestes que es connecten.
- /route ⟨src⟩ ⟨dst⟩: Mostra una mapa amb les arestes del camí més curt per anar entre dues ciutats ⟨src⟩ i ⟨dst⟩.
'''
    bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)


def author(bot, update):
    info = '''
*AUTOR:* Roger Almató Baucells
*EMAIL:* roger.almato@est.fib.upc.edu
'''
    bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)


def nodes(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Número de nodes: " + str(GB.numNodesGraph()))


def edges(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Número d'arestes: " + str(GB.numEdgesGraph()))


def components(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Número de components connexes: " + str(GB.numComponentsGraph()))


def graph(bot, update, args):
    try:
        bot.send_message(chat_id=update.message.chat_id, text='Construint el Graph...')
        distance = float(args[0])
        population = float(args[1])
        GB.crearNodes(population)
        GB.crearGraph(distance)
        bot.send_message(chat_id=update.message.chat_id, text='Graph construit amb èxit')

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /grpah ⟨distance⟩ ⟨population⟩')


def plotpop(bot, update, args):
    try:
        distance = float(args[0])
        GB.plotPOP(distance, LAT, LONG)
        bot.send_photo(chat_id=update.message.chat_id, photo=open('plotpop.png', 'rb'))

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /plotpop ⟨distance⟩')


def plotgraph(bot, update, args):
    try:
        distance = float(args[0])
        GB.plotGraph(distance, LAT, LONG)
        bot.send_photo(chat_id=update.message.chat_id, photo=open('plotGraph.png', 'rb'))

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /plotgraph ⟨distance⟩ ')


def route(bot, update, args):
    try:
        src1 = src2 = dst1 = dst2 = ""
        src1 = str(args[0])
        if src1[-1] == ',':
            src2 = str(args[1])
            dst1 = str(args[2])
            if dst1[-1] == ',':
                dst2 = str(args[3])
        else:
            dst1 = str(args[1])
            if dst1[-1] == ',':
                dst2 = str(args[2])
        src = src1 + " " + src2
        dst = dst1 + " " + dst2
        GB.plotRoute(src, dst)
        bot.send_photo(chat_id=update.message.chat_id, photo=open('route.png', 'rb'))
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='Usage: /route "Ciutat origen" "Ciutat desti" ')
        bot.send_message(chat_id=update.message.chat_id, text='Tingues en compte que podries esta introduint una ciutat amb menys habitans que els establerts al crear al graph')


def exemple(bot, update):
    info = '''
Un exemple d'execució seria:

- /start    Inicial el Bot amb totes les dades
- /graph 300 100000     Crear un graph amb ciutats de més de 100000 habitants i camins de menys de 300 kms
- /plotPop 1000     Mostra les ciutats del graf a 1000 kms de l'usuari
- /plotGraph 1000   Mostra les ciutats i camins a 1000 kms de l'usuari
- /route "Barcelona" "Amsterdam"    Mostra el camí més ràpid, si existeix, des de Barcelona a Amsterdam
- /nodes    Mostra el número de nodes del Graph
- /edges    Mostra el número d'arestes del Graph
- /components    Mostra el número de components connexes del Graph
'''
    bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)


def where(bot, update, user_data):
    LAT, LONG = update.message.location.latitude, update.message.location.longitude
    print(LAT, LONG)
    bot.send_message(chat_id=update.message.chat_id, text='Ets a les coordenades %f %f' % (lat, lon))


if __name__ == '__main__':

    # declara una constant amb el access token que llegeix de token.txt
    TOKEN = "864551856:AAGb7KYGbvfBLs6RjC-HdahBNaHitUPRN8Q"

    # crea objectes per treballar amb Telegram
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # funcions que es poden executar des del telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('author', author))
    dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True))
    dispatcher.add_handler(CommandHandler('nodes', nodes))
    dispatcher.add_handler(CommandHandler('edges', edges))
    dispatcher.add_handler(CommandHandler('components', components))
    dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_args=True))
    dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_args=True))
    dispatcher.add_handler(CommandHandler('route', route, pass_args=True))
    dispatcher.add_handler(CommandHandler('exemple', exemple))

    # posicio de l'usuari
    dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))

    # engega el bot
    updater.start_polling()
