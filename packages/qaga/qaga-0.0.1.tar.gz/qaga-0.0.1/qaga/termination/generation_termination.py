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

from .termination import Terminator, Termination


class GenerationTerminator(Terminator):
    """
    Requests termination, after it has been called a `num_generations` times.

    It is used to restrict the number of generations, i.e. iterations, and force terminate.

    :ivar num_generations: Number of iterations after that the algorithm should terminate.
    """
    def __init__(self, num_generations: int):
        assert num_generations > 0
        self._num_generations = num_generations
        self._current_generation = 0

    def should_terminate(self, population: SampleSet) -> bool:
        self._current_generation += 1
        return self._current_generation > self._num_generations


class GenerationTermination(Termination):
    """
    A factory that produces instances `GenerationTerminator`.

    :ivar num_generations: Number of iterations after that an algorithm should terminate.
    """
    def __init__(self, num_generations: int):
        assert num_generations > 0
        self.num_generations = num_generations

    def initialise(self, problem: BinaryQuadraticModel) -> Terminator:
        """
        Instantiates a `GenerationTerminator` that stops after `self.num_generations` generations.

        :param problem: The problem that should be optimised in the current run. However, it is ignored here.
        :return: A a new `GenerationTerminator`.
        """
        return GenerationTerminator(self.num_generations)
