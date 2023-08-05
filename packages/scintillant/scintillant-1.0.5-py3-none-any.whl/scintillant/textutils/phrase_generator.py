from random import randint


class RandomPhrase(object):
    def __init__(self, template: str, *args, **kwargs):
        """
        template_format: "{hello}, Niel. {day} is such a great!"
        """
        self.template = template
        self.keywords = kwargs

    def get_keyword(self) -> list:
        keywords = []
        for i, val in enumerate(self.template):
            if val == '{':
                for k, sval in enumerate(self.template[i+1:]):
                    if sval == '}':
                        keywords.append(self.template[i+1:i+k+1])
                        break
        return keywords

    def __str__(self):
        keywords = self.get_keyword()
        positions = {}
        for word in keywords:
            if word not in self.keywords:
                raise KeyError(f"{word} not found in {self.keywords.keys()} arguments.")
            positions[word] = self.keywords[word][randint(0, len(self.keywords[word]) - 1)]
        print(positions)
        return self.template.format(**positions)

    def __repr__(self):
        return self.__str__()
