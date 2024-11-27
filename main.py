import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
from chatbot import handle_response
from handle_db import db_new_reserva
#from reservas import new_reserva
from tokens import TOKEN, BOT_USERNAME


# Comands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text= "Hello I'm here to help you in your booking and info of Sol Dorado hotel \nThanks for chattting with me how can I help you"
    
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
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)

    print('BOT', response)

    await update.message.reply_text(response)

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

# Cancelar la conversación
async def cancel_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("El cuestionario ha sido cancelado. ¡Hasta luego!")
    user_data.clear()
    return ConversationHandler.END
#______________________________________________________________________________________________________________

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting.....')
    app = Application.builder().token(TOKEN).build()

    # Quiz
    conv_handler = ConversationHandler(
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
    
    # Commands
    app.add_handler(CommandHandler('Start', start_command))
    app.add_handler(conv_handler)
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)

    print('Polling.....')
    app.run_polling()