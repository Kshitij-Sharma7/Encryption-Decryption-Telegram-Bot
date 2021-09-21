import telebot
import random
import os
from keep_alive import keep_alive

API_KEY= os.environ['API_KEY']
s= int(os.environ['n'])

def encrypt(msg):
    st=""
    random.seed(s)
    for i in msg:
        key=random.randint(1,255)
        st=st+hex(ord(i)^key)[2:].zfill(2)
    return st

def decrypt(msg):
    res=''
    random.seed(s)
    for i in range(0,len(msg),2):
        key=random.randint(1,255)
        res=res+chr(int(msg[i]+msg[i+1],16)^key)
    return res

def send(msg):
    if(msg[:2]!='0x'):
        bi=encrypt(msg)
        return '0x'+bi
    else:
        bi=decrypt(msg[2:])
    return bi

bot=telebot.TeleBot(API_KEY)
keep_alive()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"Welcome to @Encr_decr_bot!\nTo get started, type any message and hit 'send' to get an encrypted message. Give this to the bot again to reveal your original message!\nThis bot also decrypts your friend's messages, so you can send your encrypted messages safely across any network!")

@bot.message_handler(commands=['greet','Greet'])
def greet(message):
    bot.reply_to(message,"Hey there!")

@bot.message_handler(commands=['hello','Hello','Hey','hey'])
def hello(message):
    bot.reply_to(message,"Hey, how are you?")

@bot.message_handler(func=lambda m:True)
def echo_all(message):	
    try:
      x=send(message.text)
    except:
      x='Currently only plain texts are supported, check back later for updates!'
    bot.reply_to(message,x)

@bot.message_handler(func=lambda m:True ,content_types=['document','audio','sticker','photo'])
def echo_(message):
    x='Currently only plain texts are supported, check back later for updates!'
    bot.reply_to(message,x)
    
bot.polling()