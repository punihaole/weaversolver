from pathlib import Path
from typing import List


def generate_word_list(source: Path, num_letters: int) -> List[str]:
    with source.open('r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == num_letters:
                yield line


def get_four_letter_words():
    all_words = Path('/usr/share/dict/words')
    return generate_word_list(all_words, 4)


def create_wordlist():
    with open('data/four_letter_words.txt', 'w') as f:
        for word in get_four_letter_words():
            f.write(f'{word}\n')


class WordBank:
    def __init__(self, lazy=True):
        self._word_list: List[str] = None
        self.word_length = None
        if not lazy:
            self._load()

    @property
    def word_list(self) -> List[str]:
        if self._word_list is None:
            self._load()
        return self._word_list

    def set_word_list(self, word_list: List[str]):
        self._word_list = word_list
        self.word_length = len(word_list[0])

    def _load(self):
        word_list = []
        with self._get_path().open('r') as f:
            while line := f.readline():
                self._try_add_word(line.strip(), word_list)
        self.set_word_list(word_list)

    def _try_add_word(self, word: str, word_list: List[str]):
        if word and not word[0].isupper():
            word_list.append(word)

    def _get_path(self) -> Path:
        return Path(__file__).parent / 'data' / 'official_four_letter_words.txt'
