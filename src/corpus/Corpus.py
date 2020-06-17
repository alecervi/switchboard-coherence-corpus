import csv
from builtins import dict


class Corpus:
    def __init__(self, corpus_folder):
        raise NotImplementedError()

    def load_csv(self):
        raise NotImplementedError()

    def create_csv(self, dialogs):
        raise NotImplementedError()

    def update_tags(self):
        self.tags_list = list(set([turn[0] for conversation in self.csv_corpus.values() for turn in conversation]))

    def get_tags(self):
        return self.tags_list
