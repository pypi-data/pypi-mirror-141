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

from abc import ABC, abstractmethod

from dimod import SampleSet, BinaryQuadraticModel


class Mutator(ABC):
    """
    An interface for improving solution candidates individually.

    Instances of subclasses are usually created once by a suitable :class:`Mutation` factory at the start of an
    optimisation run. In each iteration step :meth:`mutate` is called to generate new individuals with lower/better
    energies based on the current population by means of some local search algorithm.

    When iteration terminates, the :class:`Mutator` is destroyed. Thus, each run should have its own :class:`Mutator`
    that is independent from any other.
    """
    @abstractmethod
    def mutate(self, population: SampleSet) -> SampleSet:
        """
        Improves individuals of the calling algorithm's current population.

        Implementations of this interface must ensure that in the result population no individual appears twice.
        Moreover, the best individual of the new population must be at least as good as the best one of the old population.

        :param population: The calling algorithm's current population.
        """
        pass


class Mutation(ABC):
    """
    An interface that is used to configure, how solution candidates are improved individually per iteration.

    In fact, it is a factory that produces instances of the interface :class:`Mutator`.
    """
    @abstractmethod
    def initialise(self, problem: BinaryQuadraticModel) -> Mutator:
        """
        Instantiates and configures implementors of the interface `Mutator`.

        :param problem: The problem that should be optimised in the current run.
        """
        pass
