from pathlib import Path
from unittest import TestCase

from weaversolver.game import GamePlayer, can_change_word, find_all_possible_next_words
from weaversolver.words import WordBank


class TestCase(TestCase):
    def test_can_change_word_to_work(self):
        self.assertTrue(can_change_word('word', 'work'))
        self.assertTrue(can_change_word('work', 'word'))

    def test_cannot_change_word_to_fork(self):
        self.assertFalse(can_change_word('word', 'fork'))
        self.assertFalse(can_change_word('fork', 'word'))

    def test_cannot_change_to_invalid(self):
        self.assertFalse(can_change_word('word', 'words'))
        self.assertFalse(can_change_word('word', 'wor'))
        self.assertFalse(can_change_word('word', ''))

    def test_cannot_change_word_to_word(self):
        self.assertFalse(can_change_word('word', 'word'))

    def test_find_possible_words_for_word(self):
        bank = WordBank()
        bank.set_word_list(['word', 'work', 'bord', 'ward', 'soup', 'blah'])
        possibilities = find_all_possible_next_words(bank, 'word')
        self.assertListEqual(['work', 'bord', 'ward'], possibilities)

    def test_integration(self):
        word_bank = WordBank()
        game = GamePlayer(word_bank, 'word', 'work')
        winning_game = game.play()
        print(winning_game)
        self.assertListEqual(['word', 'work'], winning_game)
