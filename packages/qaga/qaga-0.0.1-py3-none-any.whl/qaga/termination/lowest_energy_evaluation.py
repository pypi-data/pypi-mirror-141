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

from dimod import SampleSet, BinaryQuadraticModel
from typing import Callable

from .termination import Terminator, Termination


class LowestEnergyTerminator(Terminator):
    """
    Requests termination, if a `predicate` is satisfied by the current
    populations's lowest energy.

    """
    def __init__(self, predicate: Callable[[float], bool]):
        self._predicate = predicate

    def should_terminate(self, population: SampleSet) -> bool:
        return self._predicate(population.first.energy)



class LowestEnergyTermination(Termination):
    """
    A factory that produces instances `LowestEnergyTerminator`.
    """
    def __init__(self, predicate: Callable[[float], bool]):
        self._predicate = predicate

    def initialise(self, problem: BinaryQuadraticModel) -> Terminator:
        return LowestEnergyTerminator(self._predicate)
