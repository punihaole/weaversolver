import heapq
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Dict

from weaversolver.utils import hamming_distance
from weaversolver.words import WordBank

ParentMap = Dict[str, str]
Distance = Dict[str, float]
Ladder = List[str]


def find_all_possible_next_words(word_bank: WordBank, current_word: str) -> Ladder:
    possibilities = []
    for word in word_bank.word_list:
        if can_change_word(current_word, word):
            possibilities.append(word)
    return possibilities


def can_change_word(last_word: str, next_word: str) -> bool:
    return hamming_distance(last_word, next_word) == 1


class GamePlayer:
    def __init__(self, word_bank: WordBank = None,
                 start: str = None, end: str = None):
        self.word_bank = word_bank
        self.words = []
        self.start = start
        self.end = end

    def play(self) -> Ladder:
        parents_map, _ = self._solve_with_dj()
        backtracked_path = self._backtrack(parents_map)
        actual_path = list(reversed(backtracked_path))
        return actual_path

    def _solve_with_dj(self) -> Tuple[ParentMap, Distance]:
        visited = set()
        parents_map = {}
        pq = []
        distance = defaultdict(lambda: float('inf'))
        distance[self.start] = 0
        heapq.heappush(pq, (0, self.start))

        while pq:
            _, current_word = heapq.heappop(pq)
            visited.add(current_word)

            if current_word == self.end:
                break
            possibilities = find_all_possible_next_words(self.word_bank, current_word)
            for next_word in possibilities:
                if next_word in visited:
                    continue
                weight = hamming_distance(next_word, self.end)
                new_cost = distance[current_word] + weight
                if distance[next_word] > new_cost:
                    parents_map[next_word] = current_word
                    distance[next_word] = new_cost
                    heapq.heappush(pq, (new_cost, next_word))
        return parents_map, distance

    def _backtrack(self, parents_map: ParentMap) -> Ladder:
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = parents_map[current]
        path.append(self.start)
        return path


def play_game(start, end):
    word_bank = WordBank()
    game = GamePlayer(word_bank, start, end)
    if path := game.play():
        for word in path:
            print(word)
    else:
        raise ValueError('kobayashi maru')
