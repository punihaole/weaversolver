import dataclasses
import heapq
import math
import time
from collections import defaultdict
from typing import List, Tuple, Dict

from weaversolver.utils import hamming_distance
from weaversolver.words import WordBank

ParentMap = Dict[str, str]
Distance = Dict[str, float]
Ladder = List[str]


class GameIsImpossible(Exception):
    pass


def find_all_possible_next_words(word_bank: WordBank, current_word: str) -> Ladder:
    possibilities = []
    for word in word_bank.word_list:
        if can_change_word(current_word, word):
            possibilities.append(word)
    return possibilities


def can_change_word(last_word: str, next_word: str) -> bool:
    return hamming_distance(last_word, next_word) == 1


@dataclasses.dataclass
class Strategy:
    timeout: float | int
    max_steps: float | int


DEFAULT_STRATEGY = Strategy(
    timeout=math.inf, max_steps=math.inf
)


class GamePlayer:
    def __init__(self, word_bank: WordBank = None,
                 start: str = None, end: str = None, *,
                 strategy: Strategy = DEFAULT_STRATEGY):
        self.word_bank = word_bank
        self.words = []
        self.start = start
        self.end = end
        self._timeout = strategy.timeout
        self._max_steps = strategy.max_steps

    def play(self) -> Ladder:
        parents_map, _ = self._solve_with_dj()
        backtracked_path = self._backtrack(parents_map)
        actual_path = list(reversed(backtracked_path))
        return actual_path

    def _solve_with_dj(self) -> Tuple[ParentMap, Distance]:
        t1 = time.perf_counter()
        visited = set()
        parents_map = {}
        pq = []
        distance = defaultdict(lambda: float('inf'))
        distance[self.start] = 0
        heapq.heappush(pq, (0, self.start))

        steps = 0
        while pq:
            _, current_word = heapq.heappop(pq)
            visited.add(current_word)

            if current_word == self.end:
                break
            possibilities = find_all_possible_next_words(self.word_bank, current_word)
            for next_word in possibilities:
                steps += 1
                if steps > self._max_steps:
                    return {}, {}
                if next_word in visited:
                    continue
                weight = hamming_distance(next_word, self.end)
                new_cost = distance[current_word] + weight
                if distance[next_word] > new_cost:
                    parents_map[next_word] = current_word
                    distance[next_word] = new_cost
                    heapq.heappush(pq, (new_cost, next_word))
                if time.perf_counter() - t1 > self._timeout:
                    return {}, {}
        return parents_map, distance

    def _backtrack(self, parents_map: ParentMap) -> Ladder:
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = parents_map.get(current, None)
            if not current:
                raise GameIsImpossible()
        path.append(self.start)
        return path


def play_game(start: str, end: str) -> list[str]:
    word_bank = WordBank()
    game = GamePlayer(word_bank, start, end)
    return game.play()
