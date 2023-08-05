from random import randint

from scintillant.textutils import Phrase


class RandomPhrase(Phrase):
    """ Generator of random phrases.
    :template: str = '{name}, hello!'
    :**kwargs: dict of lists = {
        'name': ['Niel', 'Almaz']
    }
    """

    def get_keyword(self) -> list:
        keywords = []
        for i, val in enumerate(self.template):
            if val == '{':
                for k, sval in enumerate(self.template[i+1:]):
                    if sval == '}':
                        keywords.append(self.template[i+1:i+k+1])
                        break
        return [keyword for keyword in keywords if keyword]

    def __str__(self):
        keywords = self.get_keyword()
        positions = {}
        for word in keywords:
            if word not in self.keywords:
                raise KeyError(f"{word} not found in {self.keywords.keys()} arguments.")
            positions[word] = self.keywords[word][randint(0, len(self.keywords[word]) - 1)]
        return self.template.format(*self.words, **positions)
