import random


class RandomWord:
    def __init__(self, template: str):
        self.template = template
        self.choices = []
        if "|" in self.template:
            self._parse()
        else:
            self.choices.append(self.template)

    def _parse(self):
        word_begins = 0
        opens = 0
        for i, symbol in enumerate(self.template):
            if symbol == ">":
                opens += 1
            if symbol == "<":
                opens -= 1
            if symbol == "|" and opens == 0:
                self.choices.append(RandomSentence(self.template[word_begins:i]))
                word_begins = i + 1
        if word_begins < len(self.template):
            self.choices.append(RandomSentence(self.template[word_begins:]))

    def generate(self):
        choice = random.choice(self.choices)
        if isinstance(choice, RandomSentence):
            return choice.generate()
        return choice


class RandomSentence(object):
    def __init__(self, template: str, *args, **kwargs):
        self.template = template
        self.kwargs = kwargs
        self.words = []
        self._parse_template()

    def _parse_template(self):
        word = ""
        opens = 0
        for i, symbol in enumerate(self.template):
            if symbol not in (">", "<") or opens != 0:
                word += symbol
            if symbol == "<":
                if opens == 0:
                    self.words.append(RandomWord(word))
                    word = ""
                opens += 1
            if symbol == ">":
                opens -= 1
                if opens == 0:
                    self.words.append(RandomWord(word[:-1]))
                    word = ""
        if word:
            self.words.append(RandomWord(word))

    def generate(self):
        res = "".join(choicer.generate() for choicer in self.words)
        if self.kwargs:
            return res.format(**self.kwargs)
        return res

    def __str__(self):
        return self.generate()

    def __repr__(self):
        return self.generate()
