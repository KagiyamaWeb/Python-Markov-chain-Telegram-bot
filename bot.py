import config
import telebot
from telebot import apihelper
import json
import os
from histograms import Dictogram
import random
from collections import deque
import re
import markov
import hmarkov

def generate_random_start(model):
    # Чтобы сгенерировать любое начальное слово, раскомментируйте строку:
    # return random.choice(model.keys())

    # Чтобы сгенерировать "правильное" начальное слово, используйте код ниже:
    # Правильные начальные слова - это те, что являлись началом предложений в корпусе
    if 'END' in model:
        seed_word = 'END'
        while seed_word == 'END':
            seed_word = model['END'].return_weighted_random_word()
        return seed_word
    return random.choice(list(model.keys())) #Allright let's try list


def generate_random_sentence(length, markov_model):
    current_word = generate_random_start(markov_model)
    sentence = [current_word]
    for i in range(0, length):
        current_dictogram = markov_model[current_word]
        random_weighted_word = current_dictogram.return_weighted_random_word()
        current_word = random_weighted_word
        sentence.append(current_word)
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '.'
    return sentence

bot = telebot.TeleBot(config.TOKEN)
apihelper.proxy = {'https': config.PROXY}

#file = open('corpus.txt','w')



@bot.message_handler(content_types=["text"])
def hear_message(message):
    file = open('corpus.txt','a')
    words = message.text.split()
    #words.append('*END*')
    file.write('\n' + (' ').join(words))
    file.close()
    #bot.send_message(message.chat.id, message.text)
    file = open('corpus.txt', 'r')
    words = file.read().split()
    #bot.send_message(message.chat.id, generate_random_sentence(random.randint(2, 20), hmarkov.make_higher_order_markov_model(2, words)))
    bot.send_message(message.chat.id, generate_random_sentence(random.randint(1, 15), markov.make_markov_model(words)))
    file.close()


if __name__ == '__main__':
    bot.infinity_polling()
