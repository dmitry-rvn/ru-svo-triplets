from dataclasses import dataclass, field
from typing import Optional

from stanza.models.common.doc import Word


@dataclass
class Phrase:
    nsubj: Optional[Word] = None
    verbs: Optional[set[Word]] = field(default_factory=set)
    obj: Optional[Word] = None
    advmod: Optional[Word] = None

    @property
    def complete(self) -> bool:
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
