**Subject-verb-object triplets** finder for russian language with `stanza` library and own heuristics.

Prerequisits:
```commandline
pip install -r requirements
python -c "import stanza; stanza.download('ru')"
```

Example (see [experiments.py](expertiments.py)):
```python
text = """
Мальчик купил интересную книгу, а через неделю он прочитал её.
Мужчина утром купил газету, а потом выпил кофе.
Сегодня охранник не рассказал анекдот, потому что ему было грустно.
Девушка искала ресторан и слушала музыку в наушниках.
Сегодня мой друг решил сделать приятный подарок.
Утром брат решил пойти выпить всё молоко.
"""

...

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
```