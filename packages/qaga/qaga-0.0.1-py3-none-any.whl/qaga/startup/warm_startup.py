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

from .startup import Startup

class WarmStartup(Startup):
    def __init__(self, population: SampleSet):
        self._population = population

    def startup(self, problem: BinaryQuadraticModel) -> SampleSet:
        assert self._population.variables == problem.variables
        assert self._population.vartype == problem.vartype

        return self._population
