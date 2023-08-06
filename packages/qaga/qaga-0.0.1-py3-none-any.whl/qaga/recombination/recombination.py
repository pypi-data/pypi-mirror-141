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


class Recombinator(ABC):
    """
    An interface for improving solution candidates by combining them.

    Instances of subclasses are usually created once by a suitable :class:`Recombinator` factory at the start of an
    optimisation run. In each iteration step :meth:`recombine` is called to assign individuals of the current
    population to mating partners. Then offsprings are procreated by finding bits in which the parents differ and
    swapping them.

    When iteration terminates, the :class:`Recombinator` is destroyed. Thus, each run should have its own
    :class:`Recombinator` that is independent from any other.
    """
    @abstractmethod
    def recombine(self, population: SampleSet) -> SampleSet:
        """
        Creates improved solution candidates by combining individuals of the calling algorithm's current population.

        Implementations of this interface must ensure that in the result population no solution appears twice.
        Moreover, the best individual of the new population must be at least as good as the best one of the old population.

        :param population: The calling algorithm's current population.
        """
        pass


class Recombination(ABC):
    """
    An interface that is used to configure, how to combine individuals to procreate enhanced ones per iteration.

    In fact, it is a factory that produces instances of the interface :class:`Recombinator`.
    """
    @abstractmethod
    def initialise(self, problem: BinaryQuadraticModel) -> Recombinator:
        """
        Instantiates and configures a implementors of the interface `Recombinator`.

        :param problem: The problem that should be optimised in the current run.
        """
        pass
