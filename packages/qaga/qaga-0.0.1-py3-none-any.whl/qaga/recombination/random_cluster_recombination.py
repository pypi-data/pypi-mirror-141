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
from dimod import SampleSet, BinaryQuadraticModel

from .recombination import Recombinator
from .pair_recombination import PairRecombinator, PairRecombination


class RandomClusterRecombinator(PairRecombinator):
    """
    Randomly chooses coherent regions of differing bits and flips them
    for randomly created pairs.

    :ivar bqm: The problem to optimise.
    :ivars recombination_rate: Amount of mates each individual should be with paired.
    :ivars rng: Random number generator for reproduciblility.
    """
    def __init__(self, bqm: BinaryQuadraticModel, recombination_rate: int, rng: np.random.Generator):
        self._bqm = bqm
        super().__init__(recombination_rate, rng)

    def _mate(self, population: SampleSet, pairs: np.ndarray) -> SampleSet:
        strings = population.record.sample
        left = strings[pairs[0]]
        right = strings[pairs[1]]

        result = np.zeros((2 * len(pairs), strings.shape[1]), dtype=strings.dtype)

        for i in range(len(pairs)):
            arg_xor = np.flatnonzero(left[i] != right[i])
            bit = self._rng.choice(arg_xor, size=1)[0]

            j = 2 * i
            result[i] = left[i]
            result[j] = right[i]

            cluster_start = bit
            while cluster_start >= 0 and right[i][cluster_start] != left[i][cluster_start]:
                result[i][cluster_start] = right[i][cluster_start]
                result[j][cluster_start] = left[i][cluster_start]
                cluster_start -= 1

            cluster_end = bit
            while cluster_end < strings.shape[1] and right[i][cluster_end] != left[i][cluster_end]:
                result[i][cluster_end] = right[i][cluster_end]
                result[j][cluster_end] = left[i][cluster_end]
                cluster_end += 1


        return SampleSet.from_samples_bqm((result, self._bqm.variables), self._bqm, aggregate_samples=True)


class RandomClusterRecombination(PairRecombination):
    """
    A factory that produces instances `RandomClusterRecombination`.
    """
    def initialise(self, problem: BinaryQuadraticModel) -> Recombinator:
        return RandomClusterRecombinator(problem, self._recombination_rate, self._rng())
