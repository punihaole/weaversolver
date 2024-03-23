from unittest import TestCase

from weaversolver.game import GamePlayer, can_change_word, find_all_possible_next_words, play_game, GameIsImpossible, \
    Strategy
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
        winning_game = play_game("word", "work")
        self.assertListEqual(['word', 'work'], winning_game)

    def test_impossible_game_timeout(self):
        with self.assertRaises(GameIsImpossible):
            word_bank = WordBank()
            game = GamePlayer(word_bank, "abos", "abri",
                              strategy=Strategy(timeout=0.1, max_steps=float("inf")))
            game.play()

    def test_impossible_game_max_steps(self):
        with self.assertRaises(GameIsImpossible):
            word_bank = WordBank()
            game = GamePlayer(word_bank, "abos", "abri",
                              strategy=Strategy(timeout=float("inf"), max_steps=1_000))
            game.play()

    def test_hard_game(self):
        word_bank = WordBank()
        game = GamePlayer(word_bank, "vile", "foul")
        ladder = game.play()
        self.assertEqual(7, len(ladder))
