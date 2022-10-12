"""
For dependency relations (`nsubj`, `obj`, etc.) reference see https://universaldependencies.org/u/dep/
"""

from collections import defaultdict

import stanza
from stanza.models.common.doc import Word

from .entities import Phrase


def extract_svo(doc: stanza.Document) -> list[Phrase]:
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
                # "subj verb1 obj1 and verb2 obj2" -> [(subj, verb1, obj1), (subj, verb2, obj2)]
                conj_nsubj = svo[(sent.index, verb.id)].nsubj
                svo[(sent.index, other.id)].add('nsubj', conj_nsubj)
                svo[(sent.index, other.id)].add('verb', other)

            elif dep_type == 'xcomp':
                # "subj verb1 ... verbN objN" -> [(subj, verb1 + ... + verbN, objN)]
                try:
                    initial_verb = _xcomp[(sent.index, verb.id)]
                except:
                    initial_verb = verb
                    _xcomp[(sent.index, verb.id)] = verb
                _xcomp[(sent.index, other.id)] = initial_verb
                svo[(sent.index, initial_verb.id)].add('verb', other)
                try:
                    other_obj = svo[(sent.index, other.id)].obj
                    svo[(sent.index, initial_verb.id)].add('obj', other_obj)
                except:
                    pass

    svo_list = [x for x in svo.values() if x.complete]
    return svo_list
