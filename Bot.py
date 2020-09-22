from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

TOKEN = "1259867714:AAGNxEDGGxC9gjdyG7rG3BGvFIkjutB3x9I"

persona = {}

def start(update,context):
    reply_keyboard = [['Chico'], ['Chica'], ['Eh...']]

    update.message.reply_text(
        'Hola! Me llamo Arielito. Soy el hijo robot de Ariel. Y voy a intentar tener una conversacion contigo'
        'Escribe /cancel si te caigo mal y quieres dejar de hablarme.\n\n'
        'Eres chico o chica?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER

def gender(update, context):
    user = update.message.from_user
    persona.__setitem__('Genero', update.message.text)
    if update.message.text == 'Eh...':
        logger.info("Bueno %s, no importa si no quieres decirlo, aqui no discriminamos a nadie :-D", user.first_name)
        update.message.reply_text('Bueno '+user.first_name+', no importa si no quieres decirlo, aqui no discriminamos a nadie :-D')
    else:
        logger.info("Bueno %s, asi que eres %s", user.first_name, update.message.text)
        update.message.reply_text('Bueno '+user.first_name+', asi que eres '+update.message.text)
    update.message.reply_text('Ahora por favor, dibujame una ov......ehh, enviame una foto tuya para saber como luces(seguro luces genial).'
                              'Si no quieres puedes tocar /skip . ',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO

def photo(update, context):
    user = update.message.from_user

    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    persona.__setitem__('Foto', 'user_photo.jpg')
    logger.info("Tu foto seria %s", 'user_photo.jpg')
    update.message.reply_text('Genial, ves, te dije que lucias genial! Me dejas saber donde estas? Si me envias tu ubicacion...'
    'no es para nada malo, lo juro (los robots podemos jurar??)'
                              'o envia /skip si no quieres hacerlo.')

    return LOCATION

def skip_photo(update, context):
    user = update.message.from_user
    persona.__setitem__('Foto', "Sin Foto")
    logger.info("Asi q prefieres permanecer en las sombras, esta bien, no pasa nada.")
    update.message.reply_text("Asi q prefieres permanecer en las sombras, esta bien, no pasa nada.")
    update.message.reply_text('Estoy seguro de que luces genial! Me dejas saber donde estas? Si me envias tu ubicacion...'
    'no es para nada malo, lo juro (los robots podemos jurar??)'
                              'o envia /skip si no quieres hacerlo.')
    return LOCATION

def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    persona.__setitem__('Ubicacion', user_location)
    logger.info("Entonces, tu ubicacion es: %f / %f", user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Entonces, tu ubicacion es: '+ str(user_location.latitude) +' / '+str(user_location.longitude))
    update.message.reply_text('Quizas te visite un dia de estos...por la noche...con un cuchillo...cuando estes solo, Buajajajajaja. '
                              'Ejem, creo que me sali del papel'
                              'Ahora, Me cuentas algo sobre ti??.')

    return BIO

def skip_location(update, context):
    user = update.message.from_user
    persona.__setitem__('Ubicacion', 'Sin ubicacion')
    logger.info("Asi que no me quieres decir donde vives, esta bien, no hay problema...PARANOICO!!!!!!!!")
    update.message.reply_text('Asi que no me quieres decir donde vives, esta bien, no hay problema...PARANOICO!!!!!!!!')
    update.message.reply_text('Ahora, Me cuentas algo sobre ti??.')

    return BIO

def bio(update, context):
    user = update.message.from_user
    persona.__setitem__('Bio', update.message.text)
    logger.info("Asi que todo eso has hecho. Muy interesante.")
    update.message.reply_text('Graciasssss! Puede que pienses que has perdido el tiempo...y tienes toda la razon, nos vemoooos.')
    final(update)
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("Hey %s, por que no quieres hablar conmigo? Bueno, otra vez sera.", user.first_name)
    update.message.reply_text('Hey '+user.first_name+', por que no quieres hablar conmigo? Bueno, otra vez sera.', reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Chau!!', reply_markup=ReplyKeyboardRemove())
    final(update)
    return ConversationHandler.END

def final(update):
    update.message.reply_text('Probando si se guardo todo bien')
    for i in persona:
        update.message.reply_text(i+':')
        print(type(persona[i]))
        if isinstance(persona[i], str):
            update.message.reply_text(persona[i])
        elif isinstance(persona[i], telegram.files.file.File):
            print(persona[i])
        elif isinstance(persona[i], telegram.files.location.Location):
            update.message.reply_text('Latitud: '+str(persona[i].latitude)+' /nLongitud: '+str(persona[i].longitude))
    return

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [MessageHandler(Filters.regex('^(Chico|Chica|Eh...)$'), gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__== '__main__':
    main()