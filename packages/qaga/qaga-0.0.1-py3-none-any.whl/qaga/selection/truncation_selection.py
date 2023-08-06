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

from .selection import Selector, Selection


class TruncationSelector(Selector):
    """
    Selects the best `num_preserved` individuals, i.e. those with the lowest
    energies.

    """
    def __init__(self, num_preserved: int):
        assert num_preserved > 1
        self._num_preserved = num_preserved

    def select(self, population: SampleSet) -> SampleSet:
        return population.truncate(self._num_preserved)


class TruncationSelection(Selection):
    """
    A factory that produces instances `TruncationSelection`.
    """
    def __init__(self, num_preserved: int):
        assert num_preserved > 1
        self._num_preserved = num_preserved

    def initialise(self, problem: BinaryQuadraticModel) -> Selector:
        return TruncationSelector(self._num_preserved)
