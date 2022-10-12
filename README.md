**Subject-verb-object triplets** extractor for russian language with `stanza` library and own heuristics.

![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)

Prerequisites:
```commandline
pip install -r requirements
python -c "import stanza; stanza.download('ru')"
```

Example:
```python
import stanza

from svo.extractor import extract_svo


text = """
Мальчик купил интересную книгу, а через неделю он прочитал её.
Мужчина утром купил газету, а потом выпил кофе.
Сегодня охранник не рассказал анекдот, потому что ему было грустно.
Девушка искала ресторан и слушала музыку в наушниках.
Сегодня мой друг решил сделать приятный подарок.
Утром брат решил пойти выпить всё молоко.
Внезапно я решил прекратить ходить выпивать пиво по выходным.
Я решил отдохнуть и посмотреть новый фильм.
Она решила найти сериал и завтра его посмотреть.
"""


nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse')
doc = nlp(text)

for phrase in extract_svo(doc):
    print(str(phrase))
```

Output:
```
Мальчик купил книгу
он прочитал её
Мужчина купил газету
Мужчина выпил кофе
охранник не рассказал анекдот
Девушка искала ресторан
Девушка слушала музыку
друг решил сделать подарок
брат решил пойти выпить молоко
я решил прекратить ходить выпивать пиво
Я решил посмотреть фильм
Она решила найти сериал
Она решила его посмотреть
```

Run tests:
```commandline
pytest -v
```