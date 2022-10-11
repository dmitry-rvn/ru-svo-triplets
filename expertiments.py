"""
Subject-verb-object triplets finder for russian language.

Prerequisites:
>>> import stanza; stanza.download('ru')

Dependency relations (`deprel`) reference:
    https://universaldependencies.org/u/dep/
"""
import stanza

from svo.extractor import extract_svo


text = """
Мальчик купил интересную книгу, а через неделю он прочитал её.
Мужчина утром купил газету, а потом выпил кофе.
Сегодня охранник не рассказал анекдот, потому что ему было грустно.
Девушка искала ресторан и слушала музыку в наушниках.
Сегодня мой друг решил сделать приятный подарок.
Утром брат решил пойти выпить всё молоко.
"""


nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse')

doc = nlp(text)

for phrase in extract_svo(doc):
    print(str(phrase))
