from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
from chatbot import handle_response
from tokens import TOKEN, BOT_USERNAME

# States for the conversation
NAME, DATE, DAYS, ROOM, GUESTS = range(5)

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bienvenido al cuestionario.\n¿Cuál es tu nombre?")
    return NAME

async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("¿Cuál es la fecha de llegada? (Formato: YYYY-MM-DD)")
    return DATE

async def ask_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("¿Cuántos días te quedarás?")
    return DAYS

async def ask_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["days"] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Por favor ingresa un número válido para los días.")
        return DAYS

    keyboard = [
        [InlineKeyboardButton("Tier 1", callback_data="tier_1")],
        [InlineKeyboardButton("Tier 2", callback_data="tier_2")],
        [InlineKeyboardButton("Tier 3", callback_data="tier_3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("¿Qué tipo de habitación deseas?", reply_markup=reply_markup)
    return ROOM

async def ask_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["room"] = query.data
    await query.edit_message_text(f"Habitación seleccionada: {query.data}")
    await query.message.reply_text("¿Cuántos huéspedes serán?")
    return GUESTS

async def finish_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["guests"] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Por favor ingresa un número válido para los huéspedes.")
        return GUESTS

    summary = (
        f"¡Gracias por completar el cuestionario!\n"
        f"Nombre: {context.user_data['name']}\n"
        f"Fecha de llegada: {context.user_data['date']}\n"
        f"Días de estancia: {context.user_data['days']}\n"
        f"Habitación: {context.user_data['room']}\n"
        f"Número de huéspedes: {context.user_data['guests']}"
    )
    await update.message.reply_text(summary)
    context.user_data.clear()
    return ConversationHandler.END

async def cancel_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("El cuestionario ha sido cancelado. ¡Hasta luego!")
    context.user_data.clear()
    return ConversationHandler.END

if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    # Conversation Handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_quiz)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_date)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_days)],
            DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_room)],
            ROOM: [CallbackQueryHandler(ask_guests)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_quiz)],
        },
        fallbacks=[CommandHandler("cancel", cancel_quiz)],
    )

    # Add handlers
    app.add_handler(conv_handler)
    print('Polling...')
    app.run_polling()
