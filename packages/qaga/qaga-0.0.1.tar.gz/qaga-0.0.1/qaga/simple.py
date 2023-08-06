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

from dimod import Sampler, BinaryQuadraticModel
from typing import Callable, Dict, Any
from numpy.random import Generator

from qaga import mutation as _mutation
from qaga import recombination as _recombination
from qaga import selection as _selection
from qaga import termination as _termination

from .genetic_algorithm import GeneticAlgorithm
from .startup import RandomStartup, WarmStartup


class IdentityMutation(_mutation.IdentityMutation):
    """
    Passes the input population without any changes.
    """
    pass


class IdentityRecombination(_recombination.IdentityRecombination):
    """
    Passes the input population without any changes.
    """
    pass


class IdentitySelection(_selection.IdentitySelection):
    """
    Passes the input population without any changes.
    """
    pass


class ReverseAnnealingMutation(_mutation.Mutation):
    """
    Improves each individual by running a `Sampler` `sampler`.
    The new solutions are added to the population.

    To improve performance it is advised to restrict the in general global
    search to a local one, e.g. by using Reverse Annealing.

    If `sampler` needs an embedding, `FixedEmbeddingComposite` or
    `LazyFixedEmbeddingComposite` are strongly advised to avoid recalculation in
    each generation.

    """
    def __init__(self, sampler: Sampler, sampler_config: Dict[str, Any] = {}):
        mutation = _mutation.ReverseAnnealingMutation(sampler, sampler_config)
        self._internal = _mutation.AdditionMutation(mutation)

    def initialise(self, problem: BinaryQuadraticModel) -> _mutation.Mutator:
        return self._internal.initialise(problem)


class RandomBitsRecombination(_recombination.RandomBitsRecombination):
    """
    Procreates new solutions by combining pairs of differing individuals. Each
    element of the old population is paired about `recombination_rate` times,
    eliminating duplications.

    For a single pair `num_bits` differing bits are randomly selected and
    flipped creating two offsprings that are added to the population.

    :ivar rng: A random number generator, that might be used for reproducibility.
    """
    def __init__(self, num_bits: int, recombination_rate: int, rng: Callable[[], Generator]):
        recombination = _recombination.RandomBitsRecombination(num_bits, recombination_rate, rng)
        self._internal = _recombination.AdditionRecombination(recombination)

    def initialise(self, problem: BinaryQuadraticModel) -> _recombination.Recombinator:
        return self._internal.initialise(problem)


class RandomClusterRecombination(_recombination.RandomClusterRecombination):
    """
    Procreates new solutions by combining pairs of differing individuals. Each
    element of the old population is paired about `recombination_rate` times,
    eliminating duplications.

    For a single pair a coherent region of differing bits is randomly selected and
    flipped creating two offsprings that are added to the population.

    :ivar rng: A random number generator, that might be used for reproducibility.
    """
    def __init__(self, recombination_rate: int, rng: Callable[[], Generator]):
        recombination = _recombination.RandomClusterRecombination(recombination_rate, rng)
        self._internal = _recombination.AdditionRecombination(recombination)

    def initialise(self, problem: BinaryQuadraticModel) -> _recombination.Recombinator:
        return self._internal.initialise(problem)


class TruncationSelection(_selection.TruncationSelection):
    """
    Selects the best `num_preserved` solutions, i.e. those with the lowest
    energies, and adds `num_new_states` random individuals. If the old
    population's size is less `num_preserved`, the deficit is compensated with
    random solutions, too.

    This helps to prevent so called elitism, i.e. the degeneration of the
    population of later generations because all individuals have been mutated to
    the same, possibly local, minima. New, unrelated solution widen the search
    space and increase the chance of finding global minima.

    :ivar rng: A random number generator, that might be used for reproducibility.
    """
    def __init__(self, num_preserved: int, num_new_solutions: int, rng: Callable[[], Generator]):
        assert num_preserved > 1
        assert num_new_solutions > 1
        recombination = _selection.TruncationSelection(num_preserved)
        self._internal = _selection.RefillingSelection(num_preserved + num_new_solutions, recombination, rng)

    def initialise(self, problem: BinaryQuadraticModel) -> _selection.Selector:
        return self._internal.initialise(problem)


class GenerationTermination(_termination.GenerationTermination):
    """
    Requests termination, after it has been called a `num_generations` times.

    It is used to restrict the number of generations, i.e. iterations, and force terminate.
    """


class LowestEnergyTermination(_termination.LowestEnergyTermination):
    """
    Requests termination, if a `predicate` is satisfied by the current
    populations's lowest energy.
    """


class AndTermination(_termination.AndTermination):
    """
    Combines multiple instances of `Terminator` and requests termination
    if all children do.
    """

class OrTermination(_termination.OrTermination):
    """
    Combines multiple instances of `Terminator` and requests termination
    if at least one of the children do.
    """
