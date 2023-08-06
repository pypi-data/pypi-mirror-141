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
from numpy.random import Generator
from dimod import SampleSet, BinaryQuadraticModel
from typing import Callable

from .recombination import Recombinator
from .pair_recombination import PairRecombinator, PairRecombination


class RandomBitsRecombinator(PairRecombinator):
    """
    Randomly flips differing bits for randomly created pairs.

    :ivar bqm: The problem to optimise.
    :ivar num_bits: Number of bits to flip.
    :ivars recombination_rate: Amount of mates each individual should be with paired.
    :ivars rng: Random number generator for reproduciblility.
    """
    def __init__(self, bqm: BinaryQuadraticModel, num_bits: int, recombination_rate: int, rng: np.random.Generator):
        self._bqm = bqm
        self._num_bits = num_bits
        super().__init__(recombination_rate, rng)

    def _mate(self, population: SampleSet, pairs: np.ndarray) -> SampleSet:
        strings = population.record.sample
        left = strings[pairs[0]]
        right = strings[pairs[1]]

        result = np.zeros((2 * len(pairs), strings.shape[1]), dtype=strings.dtype)

        for i in range(len(pairs)):
            arg_xor = np.flatnonzero(left[i] != right[i])
            num_bits = min(self._num_bits, len(arg_xor))
            bits = self._rng.choice(arg_xor, size=num_bits)

            result[i] = left[i]
            result[i][bits] = right[i][bits]

            j = 2 * i
            result[j] = right[i]
            result[j][bits] = left[i][bits]

        return SampleSet.from_samples_bqm((result, self._bqm.variables), self._bqm, aggregate_samples=True)


class RandomBitsRecombination(PairRecombination):
    """
    A factory that produces instances `RandomBitsRecombination`.
    """
    def __init__(self, num_bits: int, recombination_rate: int, rng: Callable[[], Generator]):
        self._num_bits = num_bits
        super().__init__(recombination_rate, rng)

    def initialise(self, problem: BinaryQuadraticModel) -> Recombinator:
        return RandomBitsRecombinator(problem, self._num_bits, self._recombination_rate, self._rng())
