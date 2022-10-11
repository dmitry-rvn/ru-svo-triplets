"""
Subject-verb-object triplets finder for russian language.

Prerequisites:
>>> import stanza; stanza.download('ru')

Dependency relations (`deprel`) reference:
    https://universaldependencies.org/u/dep/
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

import stanza
from stanza.models.common.doc import Word


text = """
Мальчик купил интересную книгу, а через неделю он прочитал её.
Мужчина утром купил газету, а потом выпил кофе.
Сегодня охранник не рассказал анекдот, потому что ему было грустно.
Девушка искала ресторан и слушала музыку в наушниках.
Сегодня мой друг решил сделать приятный подарок.
Утром брат решил пойти выпить всё молоко.
"""


@dataclass
class Phrase:
    nsubj: Optional[Word] = None
    verbs: Optional[set[Word]] = field(default_factory=set)
    obj: Optional[Word] = None
    advmod: Optional[Word] = None

    @property
    def completed(self) -> bool:
        return all((self.nsubj, self.obj)) and len(self.verbs) > 0

    def add(self, dep_type: str, word: Word):
        if dep_type in ('verb', 'xcomp'):
            self.verbs.add(word)
        else:
            setattr(self, dep_type, word)

    def to_list(self) -> list[Word]:
        words = [self.nsubj, *self.verbs, self.obj]
        words += [self.advmod] if self.advmod else []
        return [w for w in sorted(words, key=lambda w: w.id)]

    def __str__(self) -> str:
        return ' '.join(w.text for w in self.to_list())


def get_svo(doc: stanza.Document) -> list[Phrase]:
    svo = defaultdict(Phrase)
    _xcomp = defaultdict(Word)
    for sent in doc.sentences:
        for word_1, dep_type, word_2 in sent.dependencies:
            if word_1.pos != 'VERB' and word_2.pos != 'VERB':
                continue
            verb, other = (word_1, word_2) if word_1.pos == 'VERB' else (word_2, word_1)

            if dep_type in ('nsubj', 'obj') or (dep_type == 'advmod' and other.text == 'не'):
                svo[(sent.index, verb.id)].add(dep_type, other)
                svo[(sent.index, verb.id)].add('verb', verb)
        for word_1, dep_type, word_2 in sent.dependencies:
            if word_1.pos != 'VERB' and word_2.pos != 'VERB':
                continue
            verb, other = (word_1, word_2) if word_1.pos == 'VERB' else (word_2, word_1)

            if dep_type == 'conj' and svo[(sent.index, other.id)].nsubj is None:
                conj_nsubj = svo[(sent.index, verb.id)].nsubj
                svo[(sent.index, other.id)].add('nsubj', conj_nsubj)
                svo[(sent.index, other.id)].add('verb', other)

            elif dep_type == 'xcomp':
                try:
                    initial_verb = _xcomp[(sent.index, verb.id)]
                except:
                    initial_verb = verb
                _xcomp[(sent.index, other.id)] = verb
                svo[(sent.index, initial_verb.id)].add('verb', other)
                try:
                    other_obj = svo[(sent.index, other.id)].obj
                    svo[(sent.index, initial_verb.id)].add('obj', other_obj)
                except:
                    pass

    svo_list = [x for x in svo.values() if x.completed]
    return svo_list


if __name__ == '__main__':
    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse')

    doc: stanza.Document = nlp(text)

    for phrase in get_svo(doc):
        print(str(phrase))
