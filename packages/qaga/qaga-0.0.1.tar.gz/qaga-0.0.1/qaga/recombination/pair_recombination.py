# Copyright (C) 2022 PlanQK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
from abc import abstractmethod
from numpy.random import Generator, default_rng
from typing import Callable

from dimod import SampleSet

from .recombination import Recombinator, Recombination



def create_pairs(population_size: int, recombination_rate: int, rng: Generator = default_rng()):
    """
    Tries to choose randomly `recombination_rate` mates for each element in population_size.
    An element cannot be mated with itself and there are no dublicate pairs.

    :param population_size: Number of individuals that should be mated.
    :param recombination_rate: Amount of mates each individual should be with paired.
    :param rng: Random number generator.
    """
    assert population_size >= 2
    assert recombination_rate >= 1

    # If recombination rate is too large, create all possible pairs
    if population_size <= recombination_rate:
        recombination_rate = population_size - 1


    # Stores pairs
    assignment = np.zeros((2, population_size * recombination_rate), dtype=int)
    # Stores which mates are choosable in the respective iteration
    assignable = np.arange(1, population_size, dtype=int)

    # Sample mates for first individual
    assignment[1, :recombination_rate] = rng.choice(assignable, size=recombination_rate, replace=False)

    chosen = recombination_rate
    for individual in range(1, population_size):
        # Prohibit choosing one self
        assignable[individual-1] -= 1

        # Sample mates for current individual
        new_chosen = chosen + recombination_rate
        assignment[0, chosen:new_chosen] = individual
        assignment[1, chosen:new_chosen] = rng.choice(assignable, size=recombination_rate, replace=False)

        chosen = new_chosen

    # Eliminate duplicates
    assignment = np.unique(np.sort(assignment, axis=0), axis=1)

    return assignment


class PairRecombinator(Recombinator):
    """
    An auxiliary class for instances of `Recombinator` that combine pairs of individuals.
    Their random creation is implemented here.

    :ivars population_size: Number of individuals that should be mated.
    :ivars recombination_rate: Amount of mates each individual should be with paired.
    :ivars rng: Random number generator.
    """
    def __init__(self, recombination_rate: int, rng: np.random.Generator):
        assert recombination_rate > 1
        self._recombination_rate = recombination_rate
        self._rng = rng

    def recombine(self, population: SampleSet) -> SampleSet:
        pairs = create_pairs(len(population), self._recombination_rate)
        return self._mate(population, pairs)

    @abstractmethod
    def _mate(self, population: SampleSet, pairs: np.ndarray) -> SampleSet:
        pass


class PairRecombination(Recombination):
    """
    A factory that produces instances `PairRecombination`.
    """
    def __init__(self, recombination_rate: int, rng: Callable[[], np.random.Generator]):
        assert recombination_rate > 1
        self._recombination_rate = recombination_rate
        self._rng = rng
