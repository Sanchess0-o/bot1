import random
import telebot
import config


commands = {  
    'start': 'приветствие',
    'help': 'информация о коммандах',
    'coin': 'подбрасывает монетку',
    'password': 'генерирует пароль',
    'info': 'информация о боте'
}

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

def flip_coin():
    flip = random.randint(0, 1)  
    if flip == 0:
        return "ОРЕЛ"
    else:
        return "РЕШКА"

class MyBOT:
    def __init__(self, token=config.TOKEN):
        self.bot = telebot.TeleBot(token)
        self.commands = commands 
                
        @self.bot.message_handler(commands=['start'])
        def message_start(message):
            self.bot.reply_to(message, 'Привет!')
            self.bot.send_message(message.chat.id, 'Я просто отправляю сообщения')
            
        @self.bot.message_handler(commands=['password'])
        def send_password(message):
            password = gen_pass(10)
            self.bot.reply_to(message, f'Твой сгенерированный пароль: {password}')
            
        @self.bot.message_handler(commands=['coin'])
        def send_coin(message):
            coin = flip_coin()
            self.bot.reply_to(message, f"Монетка выпала так: {coin}")
        
        @self.bot.message_handler(commands=['help'])
        def command_help(message):
            help_text = "Команды: \n"
            for key in self.commands: 
                help_text += "/" + key + ": "
                help_text += self.commands[key] + "\n"
            self.bot.send_message(message.chat.id, help_text)
        
        @self.bot.message_handler(commands=['info'])
        def command_info(message):
            info_text = " Информация о боте:\n\n"
            info_text += "• Этот бот создан для генерации паролей\n"
            info_text += "• Используй /password для создания случайного пароля\n"
            info_text += "• Бот также может повторять твои сообщения\n"
            info_text += "• Для просмотра всех команд используй /help\n\n"
            info_text += "Разработано с помощью библиотеки pyTelegramBotAPI и telebot"
            self.bot.send_message(message.chat.id, info_text)
        
        @self.bot.message_handler(content_types=['photo'])
        def handle_photos(message):
            self.bot.reply_to(message, "Спасибо за фото")
            photo_info = f"ID фото: {message.photo[-1].file_id}\n"
            photo_info += f"Размер: {message.photo[-1].file_size} байт\n"
            photo_info += f"Ширина: {message.photo[-1].width}px\n"
            photo_info += f"Высота: {message.photo[-1].height}px"
            
            if message.caption:
                self.bot.send_message(message.chat.id, f"Подпись к фото: {message.caption}")
           
            self.bot.send_message(message.chat.id, photo_info)
        
        @self.bot.message_handler(func=lambda message: True)
        def echo_message(message):
            self.bot.reply_to(message, message.text)

    def run(self):
        print("Бот запущен...")
        self.bot.infinity_polling()

if __name__ == '__main__':
    mybot = MyBOT()
    mybot.run()
