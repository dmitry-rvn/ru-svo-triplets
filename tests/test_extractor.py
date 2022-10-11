import pytest
import stanza

from svo.extractor import extract_svo


nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse')


def _extract_svo(text: str) -> list[str]:
    doc = nlp(text)
    svo_list = extract_svo(doc)
    return [str(phrase) for phrase in svo_list]


@pytest.mark.parametrize(
    'text,expected',
    [
        pytest.param('Мальчик купил интересную книгу.', ['Мальчик купил книгу'], id='simple'),
        pytest.param('Мальчик купил интересную книгу, а через неделю он прочитал её.', ['Мальчик купил книгу', 'он прочитал её'], id='two parts'),
        pytest.param('Мужчина утром купил газету, а потом выпил кофе.', ['Мужчина купил газету', 'Мужчина выпил кофе'], id='1 subj, 2 verbs (with conj)'),
        pytest.param('Сегодня охранник не рассказал анекдот, потому что ему было грустно.', ['охранник не рассказал анекдот'], id='verb with `не`'),
        pytest.param('Девушка искала ресторан и слушала музыку в наушниках.', ['Девушка искала ресторан', 'Девушка слушала музыку'], id='1 subj, 2 verbs (with conj) [2]'),
        pytest.param('Сегодня мой друг решил сделать приятный подарок.', ['друг решил сделать подарок'], id='2 linked verbs (with xcomp)'),
        pytest.param('Утром брат решил пойти выпить всё молоко.', ['брат решил пойти выпить молоко'], id='3 linked verbs (with xcomp)'),
        pytest.param('Я решил прекратить ходить выпивать пиво по выходным.', ['Я решил прекратить ходить выпивать пиво'], id='4 linked verbs (with xcomp)'),
    ]
)
def test_extract_svo(text: str, expected: str):
    assert _extract_svo(text) == expected
