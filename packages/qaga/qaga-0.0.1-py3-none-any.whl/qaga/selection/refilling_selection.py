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

from typing import Callable
from dimod import BinaryQuadraticModel
from dimod.sampleset import SampleSet, concatenate
from numpy.random import Generator

from .selection import Selector, Selection
from ..startup.random_startup import create_random


MAX_FILLING_ITERATION = 1_000

class RefillingSelector(Selector):
    """
    Wraps an `internal` `Selector` and ensures that the next generation's
    population contains at least `num_preserved` individuals by adding random
    ones.

    This helps to prevent so called elitism, i.e. the degeneration of the
    population of later generations because all individuals have been mutated to
    the same, possibly local, minima. New, unrelated solution widen the search
    space and increase the chance of finding global minima.
    """
    def __init__(self, num_preserved: int, problem: BinaryQuadraticModel,
                 internal: Selector, rng: Generator):
        assert num_preserved > 1
        self._num_preserved = num_preserved
        self._bqm = problem
        self._internal = internal
        self._rng = rng

    def select(self, population: SampleSet) -> SampleSet:
        # Do not try to pick more states that available.
        new_population = self._internal.select(population)

        for _ in range(MAX_FILLING_ITERATION):
            if len(new_population) == self._num_preserved:
                return new_population

            # Compute how many additional elements must be created including the replanishing ones.
            num_missing = self._num_preserved - len(new_population)

            additional_individuals = create_random(len(self._bqm), num_missing,
                                                   self._bqm.vartype, MAX_FILLING_ITERATION, self._rng)
            sampleset = SampleSet.from_samples_bqm((additional_individuals, self._bqm.variables),
                                                   self._bqm)
            new_population = concatenate([new_population, sampleset]).aggregate()

        raise Exception("Tried to create new individuals but failed {MAX_FILLING_ITERATION}-times!")


class RefillingSelection(Selection):
    """
    A factory that produces instances `RefillingSelection`.
    """
    def __init__(self, num_preserved: int, internal: Selection, rng: Callable[[], Generator]):
        assert num_preserved > 1
        self._num_preserved = num_preserved
        self._internal = internal
        self._rng = rng

    def initialise(self, problem: BinaryQuadraticModel) -> Selector:
        return RefillingSelector(
            self._num_preserved,
            problem,
            self._internal.initialise(problem),
            self._rng()
            )
