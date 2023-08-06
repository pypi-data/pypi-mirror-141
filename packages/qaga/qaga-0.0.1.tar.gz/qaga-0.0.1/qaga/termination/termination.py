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


class Terminator(ABC):
    """
    An interface for terminating an algorithm.

    Instances of subclasses are usually created once by a suitable :class:`Termination` factory at the start of an
    optimisation run. After each iteration step :meth:`should_terminate` is called
    to decide with respect to the current population and possibly a custom, encapsulated state if an algorithm should
    terminate. If so, iteration stops and the :class:`Terminator` is destroyed. Thus,
    each run should have its own :class:`Terminator` that is independent from any other.
    """
    @abstractmethod
    def should_terminate(self, population: SampleSet) -> bool:
        """
        Decides if the calling algorithm should stop iteration.

        :param population: The calling algorithm's current population.
        :return: :code:`True` to terminate, :code:`False` to continue.
        """
        pass


class Termination(ABC):
    """
    An interface that is used to configure the termination condition of a genetic algorithm.

    In fact, it is a factory that produces instances of the interface :class:`Terminator`.
    """
    @abstractmethod
    def initialise(self, problem: BinaryQuadraticModel) -> Terminator:
        """
        Instantiates and configures a implementors of the interface `Terminator`.

        :param problem: The problem that should be optimised in the current run.
        """
        pass
