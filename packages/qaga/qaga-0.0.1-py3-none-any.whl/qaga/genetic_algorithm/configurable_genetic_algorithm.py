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

from dataclasses import dataclass

from dimod import SampleSet, BinaryQuadraticModel
from toolz.curried import pipe

from ..mutation import Mutation
from ..recombination import Recombination
from ..selection import Selection
from ..startup import Startup
from ..termination import Termination


@dataclass
class GeneticAlgorithm:
    """
    A configurable implementation of a genetic algorithm, that solves a minimisation problem given as a
    :class:`QuadraticModel` and returns a solution as :class:`SampleSet`. It is thus fully compatible with the
    `dimod`-API.

    This class itself is just a template that must be filled with the following components to work:

    :param Startup startup: Determines the initial population. For instance, it can be random or used as a warm start.

    :param Mutation mutation: Improves quality of the current population by starting a local search from its individuals.

    :param Recombination recombination: Procreates new individuals by combining existing ones.

    :param Selection selection: Truncates low quality solutions to keep the population small.

    :param Termination termination: Allows to stop the algorithm if the population has achieved a certain quality
    level or takes too long.

    Note that this class is stateless, i.e. calling `optimise` multiple times parallelly works without any problems.
    """
    startup: Startup
    mutation: Mutation
    recombination: Recombination
    selection: Selection
    termination: Termination

    def optimise(self, problem: BinaryQuadraticModel) -> SampleSet:
        # Instantiate each component for a each optimisation run. Therefore, they have their own internal state that
        # should not interfere with the outside environment.
        mutator = self.mutation.initialise(problem)
        recombinator = self.recombination.initialise(problem)
        selector = self.selection.initialise(problem)
        terminator = self.termination.initialise(problem)

        # Produce a first population
        population = self.startup.startup(problem)
        while True:
            # Add new individuals by mutation and recombination.
            population = pipe(population,
                              mutator.mutate,
                              recombinator.recombine)
            # Check termination condition, e.g. existence of a good solution.
            if terminator.should_terminate(population):
                break

            # Truncate low quality individuals.
            population = selector.select(population)
        return population


