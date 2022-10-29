from random import randint
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from secret import token
from time import sleep
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)


# Define Constant
field = list(range(1, 10))
x = chr(10060)
o = chr(11093)
player = x
CHOICE = 0
count = 0


def win_combinations(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]]
    return n[0] if n else n


def paint_field(field: list) -> str:
    txt = ''
    for i in range(len(field)):
        if not i % 3:
            txt += f'\n{"." * 25}\n'
        txt += f'{field[i]:^8}'
    txt += f"\n{'.' * 25}"
    return txt

# У меня почему-то не получается сделать так чтобы бот ходил автоматически. без нажатия кнопки.
# Найти я так и не смог, где найти подсказку

def play_with_bot(field):
    while True:
        move = randint(1, 9)
        if move not in field:
            return str(move)
        else:
            continue


def start(update, _):
    global field, player, count
    field = list(range(1, 10))
    count = 0
    player = x
    update.message.reply_text("Hello, I want to play with you in 'tic-tac-toe'")
    sleep(1)
    update.message.reply_text("You'll play with my stupid bot which I created!!!")
    update.message.reply_text(paint_field(field))
    sleep(1)
    update.message.reply_text("Please, enter the number between 1 and 9")
    return CHOICE


def choice(update, _):
    global player, count
    if player == o:
        while True:
            move = randint(1, 9)
            if move in field:
                break
            else:
                continue
    else:
        move = update.message.text
        move = int(move)
    if move not in field:
        update.message.reply_text("Incorrect input \nTry again")
    else:
        field.insert(field.index(move), player)
        field.remove(move)
        update.message.reply_text(paint_field(field))
        if win_combinations(field):
            update.message.reply_text(f"{player} is the tic-tac-toe champion at the world championship")
            return ConversationHandler.END
        if player == x:
            update.message.reply_text("press any key to make the bot make a move")
        else:
            update.message.reply_text("Please, enter the number between 1 and 9")
        player = o if player == x else x
        count += 1

    if count == 9:
        update.message.reply_text("the game ended in a draw")
        return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text('Bye', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('Hooray, the server started working')

    updater.start_polling()
    updater.idle()
