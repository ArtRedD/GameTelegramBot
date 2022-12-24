import telebot
import database
from telebot import types

bot = telebot.TeleBot('5950759208:AAESInotawb_mGBNkVRVAk73o_-gOjGo4pc')


@bot.message_handler(commands=['start'])
def start(message):
    m = f"Hello, <i>{message.from_user.first_name} {message.from_user.last_name}</i>\nWe are glad to welcome you \
in a <b>Poison Tester</b> game!\nTo start a game print <b>/newgame</b>\nFor help print <b>/help</b>"
    bot.send_message(message.chat.id, m, parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    b1 = types.KeyboardButton("/newgame")
    b2 = types.KeyboardButton("/help")
    b3 = types.KeyboardButton("/rules")

    b4 = types.KeyboardButton("/meal")
    b5 = types.KeyboardButton("/ingredients")
    b6 = types.KeyboardButton("/highscore")
    markup.add(b1, b2, b3, b4, b5, b6)
    bot.send_message(message.chat.id, "Or use keyboard buttons:", reply_markup=markup)

    database.add_user(message.chat.id, message.from_user.first_name, message.from_user.last_name)


@bot.message_handler(commands=['rules'])
def rules(message):
    m = f"""
Rules of <b>Poison Tester</b> are pretty simple.
You are given <b>6</b> meals one by one and you need to identify whether a meal contains a poison or not.
If it contains a poison, give meal to a <b>dog</b>. If not, to a <b>king</b>.
If the king dies, you are beheaded.
If the dog survives after a meal, you are beheaded.
You win if you survive all the 6 meals.
If you are beheaded, you go back in time. Meals are the same, but poison contained in a meal may differ or be absent.
Try to feed the king with all 6 meals in a least number of attempts.
Good luck!
        """
    bot.send_message(message.chat.id, m, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    m = f"""
To start a new game press <i>newgame</i>.
For rules press <i>rules</i>.
            
In a game type <i>/ingredients</i> for a list of ingredients to use.
And to see your current meal type <i>/meal</i>.
        """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("newgame", callback_data="/newgame"))
    markup.add(types.InlineKeyboardButton("rules", callback_data="/rules"))
    bot.send_message(message.chat.id, m, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=['ingredients'])
def show_ingredients(message):
    if database.is_in_game(database.get_user_id(message.chat.id)):
        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("silver_dust", callback_data="/apply_silver_dust"))
        markup.add(types.InlineKeyboardButton("golden_dust", callback_data="/apply_golden_dust"))
        markup.add(types.InlineKeyboardButton("tripotassium_phosphate", callback_data="/apply_tripotassium_phosphate"))
        markup.add(types.InlineKeyboardButton("sodium_chloride", callback_data="/apply_sodium_chloride"))
        markup.add(types.InlineKeyboardButton("oxalic_acid", callback_data="/apply_oxalic_acid"))
        markup.add(types.InlineKeyboardButton("hydrogen_peroxide", callback_data="/apply_hydrogen_peroxide"))
        markup.add(types.InlineKeyboardButton("rose", callback_data="/apply_rose"))

        bot.send_message(message.chat.id, "Ingredients", reply_markup=markup, parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Not in a game!", parse_mode='html')


@bot.message_handler(commands=['meal'])
def show_meal(message):
    if database.is_in_game(database.get_user_id(message.chat.id)):
        meal = database.current_meal(database.get_user_id(message.chat.id))
        m = meal

        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("Give to dog", callback_data="/give_to_dog"))
        markup.add(types.InlineKeyboardButton("Give to king", callback_data="/give_to_king"))
        markup.add(types.InlineKeyboardButton("End game", callback_data="/end_game"))

        bot.send_message(message.chat.id, m, reply_markup=markup, parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Not in a game!", parse_mode='html')


@bot.message_handler(commands=['highscore'])
def show_highscore(message):
    res = database.highscore(database.get_user_id(message.chat.id))
    bot.send_message(message.chat.id, res, parse_mode='html')


@bot.message_handler(commands=['newgame'])
def newgame(message):
    database.start_game(database.get_user_id(message.chat.id))
    bot.send_message(message.chat.id, "Welcome to <b>Poison Tester</b>!", parse_mode='html')

    rules(message)

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton("Show meal", callback_data="/show_meal"))
    markup.add(types.InlineKeyboardButton("Use ingredients", callback_data="/use_ingredients"))

    m = f"Press <i>Show meal</i> to see your current meal.\nPress <i>Use ingredients</i> to see and use ingredients \
to test the meal"

    bot.send_message(message.chat.id, m, reply_markup=markup, parse_mode="html")

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # b1 = types.KeyboardButton("/meal")
    # b2 = types.KeyboardButton("/ingredients")
    # markup.add(b1, b2)
    # bot.send_message(message.chat.id, "Or use buttons:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "/rules":
        rules(call.message)
    elif call.data == "/newgame":
        newgame(call.message)
    elif call.data == "/show_meal":
        show_meal(call.message)
    elif call.data == "/use_ingredients":
        show_ingredients(call.message)
    elif call.data.split("_")[0] == "/apply":  # applying an ingredient
        if database.is_in_game(database.get_user_id(call.message.chat.id)):
            ingredient = '_'.join(call.data.split("_")[1:])
            bot.send_message(call.message.chat.id, f"You apply {ingredient} to the meal", parse_mode='html')
            res = database.apply(database.get_user_id(call.message.chat.id), ingredient)
            bot.send_message(call.message.chat.id, res, parse_mode='html')
        else:
            bot.send_message(call.message.chat.id, "Not in a game!", parse_mode='html')
    elif call.data.split('_')[0] == "/give":
        if database.is_in_game(database.get_user_id(call.message.chat.id)):
            if call.data == "/give_to_dog":
                res = database.give_to_dog(database.get_user_id(call.message.chat.id))
                bot.send_message(call.message.chat.id, res, parse_mode='html')
                if database.is_in_game(database.get_user_id(call.message.chat.id)):
                    show_meal(call.message)
                    show_ingredients(call.message)
            elif call.data == "/give_to_king":
                res = database.give_to_king(database.get_user_id(call.message.chat.id))
                bot.send_message(call.message.chat.id, res, parse_mode='html')
                if database.is_in_game(database.get_user_id(call.message.chat.id)):
                    show_meal(call.message)
                    show_ingredients(call.message)
        else:
            bot.send_message(call.message.chat.id, "Not in a game!", parse_mode='html')
    elif call.data == "/end_game":
        database.end_game(database.get_user_id(call.message.chat.id))
        bot.send_message(call.message.chat.id, "ENDING A GAME", parse_mode='html')
    else:
        print(f"Unknown call received: {call.data}")


bot.polling(none_stop=True)
