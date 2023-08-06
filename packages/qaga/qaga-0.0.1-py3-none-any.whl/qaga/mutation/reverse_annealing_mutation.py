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

from dimod import Sampler, SampleSet, BinaryQuadraticModel
from typing import Dict, Any

from .mutation import Mutator, Mutation


class ReverseAnnealingMutator(Mutator):
    """
    Improves the population by starting an annealing run at each individuals
    """
    def __init__(self, sampler: Sampler, bqm: BinaryQuadraticModel, sampler_config: Dict[str, Any] = {}):
        self._sampler = sampler
        self._sampler_config = sampler_config
        self._bqm = bqm

    def mutate(self, population: SampleSet) -> SampleSet:
        return self._sampler.sample(self._bqm, initial_states=population, **self._sampler_config)


class ReverseAnnealingMutation(Mutation):
    """
    A factory that produces instances `ReverseAnnealingMutation`.
    """
    def __init__(self, sampler: Sampler, sampler_config: Dict[str, Any] = {}):
        self._sampler = sampler
        self._sampler_config = sampler_config

    def initialise(self, problem: BinaryQuadraticModel) -> Mutator:
        return ReverseAnnealingMutator(self._sampler, problem, self._sampler_config)
