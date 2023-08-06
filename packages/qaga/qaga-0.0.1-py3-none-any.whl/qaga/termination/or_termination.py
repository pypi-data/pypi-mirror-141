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
from typing import List

from .termination import Terminator, Termination


class OrTerminator(Terminator):
    """
    Combines multiple instances of `Terminator` and requests termination
    if at least one of the children do.

    :ivar stoppers: Children to combine
    """
    def __init__(self, stoppers: List[Terminator]):
        self.stoppers = stoppers

    def should_terminate(self, population: SampleSet) -> bool:
        return any(s.should_terminate(population) for s in self.stoppers)


class OrTermination(Termination):
    """
    A factory that produces instances `OrTerminator`.
    """
    def __init__(self, stops: List[Termination]):
        self.stops = stops

    def initialise(self, problem: BinaryQuadraticModel) -> Terminator:
        return OrTerminator([s.initialise(problem) for s in self.stops])
