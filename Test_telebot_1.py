from aiogram import Bot, Dispatcher, executor, types
import random

API_TOKEN = '5825996680:AAFM17rZHyYm-Tn5iU2VCeD0eaRJ6Fa4yYk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

l_i = False
_list = []

def rand(a, b):
    l = [i for i in range(a, b + 1)]
    random.shuffle(l)
    return l[0]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")

@dp.message_handler(commands=['help'])
async def send_command_list(message: types.Message):
    await message.reply("На данный момент бот имеет следующие команды:\n" +
                        "/help - показывает список существующих команд\n" +
                        "/print_random_number n m - отправляет рандомное число от n до m включительно\n" +
                        "/shake_list - отправляет введённый вами список, каждому значению которого соответствует случайние значение данного списка, но не оно само\n")

@dp.message_handler(commands=['print_random_number'])
async def print_random_number(message: types.Message):
    text = message.text
    text = text[text.find(" ") + 1:]
    answer = str(random.randint(int(text[:text.find(" ")]), int(text[text.find(" ") + 1:])))
    await message.answer(answer)

@dp.message_handler(commands=['shake_list'])
async def shake_list(message: types.Message):
    global l_i, _list
    print(l_i, _list)
    await message.answer("Введите список через пробел, после этого, следующим сообщением, отправьте команду /end_of_list")
    l_i = True

@dp.message_handler(commands=['end_of_list'])
async def output_list(message: types.Message):
    global l_i, _list
    print(l_i, _list)
    answer = ""
    if not l_i:
        indexes = [i for i in range(len(_list))]
        for i in range(len(_list)):
            rand_i = rand(0, len(indexes) - 1)
            while indexes[rand_i] == i:
                rand_i = rand(0, len(indexes) - 1)
            answer += _list[i] + " - " + _list[indexes[rand_i]] + "\n"
            indexes.pop(rand_i)
    else:
        answer = "Вы не ввели список!\nведите список!"
    await message.answer(answer)

@dp.message_handler()
async def input_list(message: types.Message):
    global l_i, _list
    if l_i:
        _list = message.text.split()
        l_i = False

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
