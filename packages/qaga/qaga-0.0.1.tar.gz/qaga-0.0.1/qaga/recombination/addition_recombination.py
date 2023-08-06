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
from dimod import BinaryQuadraticModel
from dimod.sampleset import SampleSet, concatenate

from .recombination import Recombinator, Recombination

class AdditionRecombinator(Recombinator):
    """
    Executes a wrapped `Recombinator` and merges its result with the old population.
    This is a trivial way of preserving good solution quality.

    :ivars internal: Defines how new individuals are appended to current population.
    """
    def __init__(self, internal: Recombinator):
        self._internal = internal

    def recombine(self, population: SampleSet) -> SampleSet:
        return concatenate([population, self._internal.recombine(population)]).aggregate()


class AdditionRecombination(Recombination):
    """
    A factory that produces instances `AdditionRecombination`.
    """
    def __init__(self, internal: Recombination):
        self._internal = internal

    def initialise(self, problem: BinaryQuadraticModel) -> Recombinator:
        return AdditionRecombinator(self._internal.initialise(problem))
