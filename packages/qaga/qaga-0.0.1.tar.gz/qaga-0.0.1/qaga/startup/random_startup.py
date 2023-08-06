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
from dimod import SampleSet, Vartype, BinaryQuadraticModel, as_samples
from numpy.random import Generator

from .startup import Startup

MAX_ITERATIONS = 1_000

def create_random(num_qubits: int, size: int, vartype: Vartype, max_tries: int, rng: Generator) -> np.ndarray:
    assert num_qubits > 0
    assert size > 0

    choosable = np.array(list(vartype.value), dtype='i1')

    sample = np.unique(rng.choice(choosable, size=(size, num_qubits)), axis=0)
    tries = 1

    while len(sample) != size and tries <= max_tries:
        additional = rng.choice(choosable, size=(size-len(sample), num_qubits))
        sample = np.unique(np.concatenate([sample, additional]), axis=0)
        tries += 1

    return sample


class RandomStartup(Startup):
    def __init__(self, population_size: int, rng: np.random.Generator):
        assert population_size > 1
        self._population_size = population_size
        self._rng = rng

    def startup(self, problem: BinaryQuadraticModel) -> SampleSet:
        sample = create_random(len(problem), self._population_size, problem.vartype, MAX_ITERATIONS, self._rng)
        return SampleSet.from_samples_bqm((sample, problem.variables), problem, aggregate_samples=True)
