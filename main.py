import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler, CallbackContext
from chatbot import handle_response
from handle_db import db_new_reserva, db_check_reserva
#from reservas import new_reserva
from tokens import TOKEN, BOT_USERNAME
GET_RESERVA = 1

# Comands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text= "Hola soy un BOT diseñado para proporcionarte informacion y ayudarte en tu reserva en el hotel El Sol Dorado \nGracias por chatear conmigo en que puedo ayudarte"
    
    image_path = "images/logo.png"

    if not os.path.exists(image_path):
        await update.message.reply_text("SOL DORADO!")
        return
    
    await update.message.reply_photo(photo=open(image_path, 'rb'), caption=message_text)


"""
async def booking_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Aqui tenes tu lista de Reservas')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello thanks for chattting with me how can I help you')

"""

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response, tag = handle_response(new_text)
        else:
            return
    else:
        response, tag = handle_response(text)

    print('BOT', response)
    print('TAG', tag)
    await update.message.reply_text(response)
    
    if tag == "info-habitaciones":
        "Tenemos tres tipos de habitaciones: Tipo 1, 2 y Tipo 3."
        
        image_t1 = "images/t1.jpg"
        image_t2 = "images/t2.jpg"
        image_t3 = "images/t3.jpg"
        
        t1_text = "Tipo 1: La selección más economica."
        t2_text = "Tipo 2: Disfruta de hermosas vistas, acceso a piscina publica, entre otras amenidades"
        t3_text = "Tipo 3: Nuestra suite más lujosa, con piscina privada entre otras amenidades"

        await update.message.reply_photo(photo=open(image_t1, 'rb'), caption=t1_text)
        await update.message.reply_photo(photo=open(image_t2, 'rb'), caption=t2_text)
        await update.message.reply_photo(photo=open(image_t3, 'rb'), caption=t3_text)
        await update.message.reply_text("Por favor, indícame cuál te interesa para más detalles.")
    
    if tag == "info-t1":
    
        image_bar = "images/bar.jpg"
        image_rest = "images/rest.jpg"
        image_pool = "images/pool.jpg"

        bar_text = "La habitacion Tipo 1 cuenta con acceso a bar"
        rest_text = "El restaurante donde podra seleccionar tres platos diarios gratuitos."
        pool_text = "acceso a la piscina publica."

        await update.message.reply_photo(photo=open(image_bar, 'rb'), caption=bar_text)
        await update.message.reply_photo(photo=open(image_rest, 'rb'), caption=rest_text)
        await update.message.reply_photo(photo=open(image_pool, 'rb'), caption=pool_text)
    
    
    if tag == "info-t2":

        image_buff = "images/buff.jpg"
        image_kar = "images/kar.jpg"

        buff_text = "Restaurante y buffet con las mejores comidas, "
        kar_text = "karaoke entre otros eventos."

        await update.message.reply_photo(photo=open(image_buff, 'rb'), caption=buff_text)
        await update.message.reply_photo(photo=open(image_kar, 'rb'), caption=kar_text)
    
    if tag == "info-t3":
        image_indoor = "images/indoor.jpg"
        image_indoor_pool = "images/indoor_pool.jpg"

        indoor_pool_text= "Una habitación enorme con piscina privada"
        indoor_pool = "canchas deportiva entre otras actividades."

        await update.message.reply_photo(photo=open(image_indoor_pool, 'rb'), caption=indoor_pool_text)
        await update.message.reply_photo(photo=open(image_indoor, 'rb'), caption=indoor_pool)

# Quiz Nueva reserva handler 
# _________________________________________________________________________________
# Estados para la conversación
NAME, DATE, DAYS, ROOM, GUESTS = range(5)

# Diccionario para almacenar los datos del usuario temporalmente
user_data = {}

# Inicia el cuestionario
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bienvenido al cuestionario.\n¿Cuál es tu nombre?")
    return NAME

# Solicitar fecha
async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["name"] = update.message.text
    await update.message.reply_text("¿Cuál es la fecha de llegada? (Formato: YYYY-MM-DD)")
    return DATE

# Solicitar días de estancia
async def ask_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["date"] = update.message.text
    await update.message.reply_text("¿Cuántos días te quedarás?")
    return DAYS

# Solicitar tipo de habitación
async def ask_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["days"] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Por favor ingresa un número válido para los días.")
        return DAYS

    keyboard = [
        [InlineKeyboardButton("Tier 1", callback_data="Tier 1")],
        [InlineKeyboardButton("Tier 2", callback_data="Tier 2")],
        [InlineKeyboardButton("Tier 3", callback_data="Tier 3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("¿Qué tipo de habitación deseas?", reply_markup=reply_markup)
    return ROOM

# Guardar la habitación seleccionada y solicitar el número de huéspedes
async def ask_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data["room"] = query.data
    await query.edit_message_text(f"Habitación seleccionada: {query.data}")
    await query.message.reply_text("¿Cuántos huéspedes serán?")
    return GUESTS

# Finalizar el cuestionario
async def finish_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["guests"] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Por favor ingresa un número válido para los huéspedes.")
        return GUESTS

    # Insertar en reserva en BD
    db_new_reserva(user_data['name'], user_data['date'], user_data['days'], user_data['room'], user_data['guests'])

    # Resumen de los datos capturados
    summary = (
        f"¡Gracias por completar el cuestionario!\n"
        f"Nombre: {user_data['name']}\n"
        f"Fecha de llegada: {user_data['date']}\n"
        f"Días de estancia: {user_data['days']}\n"
        f"Habitación: {user_data['room']}\n"
        f"Número de huéspedes: {user_data['guests']}"
    )
    await update.message.reply_text(summary)

    # Reiniciar datos para futuros usuarios
    user_data.clear()
    return ConversationHandler.END

# Cancelar el quiz
async def cancel_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("El cuestionario ha sido cancelado. ¡Hasta luego!")
    user_data.clear()
    return ConversationHandler.END
#______________________________________________________________________________________________________________

# obtener info de reserva con nombre de usuario de reserva
async def start_get_reserva(update: Update, context: CallbackContext) -> str:
    await update.message.reply_text("Ingresar nombre de usuario")
    return GET_RESERVA

async def get_reserva(update: Update, context: CallbackContext) -> str:
    try:
        print("Llego aca --2")
        # Try to convert the input to an integer
        res_num = str(update.message.text)
        # Save the integer into context
        context.user_data['res_num'] = res_num
# cursor.execute("SELECT reserva_num, reserva_fecha, reserva_dias, reserva_huespedes, reserva_room FROM reserva WHERE reserva_num = ?", (reserva_num,))
        usuario, fecha, dias, huespedes, habitacion = db_check_reserva(res_num)

        summary = (
        f"Esta es la información de reserva, deacuerdo con el nombre de usuario proporcionado:\n"
        f"{usuario}\n"
        f"{fecha}\n"
        f"{dias}\n"
        f"{huespedes}\n"
        f"{habitacion}"
    )
        await update.message.reply_text(summary)

        return ConversationHandler.END
    except ValueError:
        # Handle the case when the input is not an integer
        await update.message.reply_text('Oops! Por favor ingrese un numero entero correcto.')
        return GET_RESERVA

async def cancel_info_reserva(update: Update, context: CallbackContext) -> str:
    await update.message.reply_text('Conversation canceled.')
    return ConversationHandler.END

#Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting.....')
    app = Application.builder().token(TOKEN).build()

    # Quiz
    quiz_handler = ConversationHandler(
        entry_points=[CommandHandler("reservar", start_quiz)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_date)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_days)],
            DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_room)],
            ROOM: [CallbackQueryHandler(ask_guests)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_quiz)],
        },
        fallbacks=[CommandHandler("cancelar_quiz", cancel_quiz)],
    )
    
    # 
    info_reserva = ConversationHandler(
        entry_points=[CommandHandler('consultar_reserva', start_get_reserva)],
        states={
            GET_RESERVA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reserva)]
        }, fallbacks=[CommandHandler('cancel_info_reserva', cancel_info_reserva)]
    )

    # Commands
    app.add_handler(CommandHandler('Start', start_command))
    app.add_handler(quiz_handler)
    app.add_handler(info_reserva)
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)

    print('Polling.....')
    app.run_polling()