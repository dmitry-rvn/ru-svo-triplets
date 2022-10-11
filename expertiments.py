import stanza

from svo.extractor import extract_svo


text = """
Мальчик купил интересную книгу, а через неделю он прочитал её.
Мужчина утром купил газету, а потом выпил кофе.
Сегодня охранник не рассказал анекдот, потому что ему было грустно.
Девушка искала ресторан и слушала музыку в наушниках.
Сегодня мой друг решил сделать приятный подарок.
Утром брат решил пойти выпить всё молоко.
Я решил прекратить ходить выпивать пиво по выходным.
"""


nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse')

doc = nlp(text)

for phrase in extract_svo(doc):
    print(str(phrase))
