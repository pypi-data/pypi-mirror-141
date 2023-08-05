""" Default Phrases for user_answers
"""


class Phrase(object):
    def __init__(self, template: str, *args, **kwargs):
        self.template = template
        self.words = args
        self.keywords = kwargs

    def __str__(self):
        return self.template.format(*self.words, **self.keywords)

    def __repr__(self):
        return self.__str__()
