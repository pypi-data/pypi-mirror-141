from abc import ABC, abstractmethod

from dimod import SampleSet, BinaryQuadraticModel


class Selector(ABC):
    """
    An interface for collocating the population of the succeeding iteration.

    Instances of subclasses are usually created once by a suitable :class:`Selector` factory at the start of an
    optimisation run. In each iteration step :meth:`select` is called to assess which individuals of the current
    population are eligible to be preserved for the next iteration step and, potentially, to add completely new,
    e.g. random, ones.

    When iteration terminates, the :class:`Selector` is destroyed. Thus, each run should have its own
    :class:`Selector` that is independent from any other.
    """
    @abstractmethod
    def select(self, population: SampleSet) -> SampleSet:
        """
        Composes the population of the succeeding iteration step based on the current population.

        Implementations of this interface must ensure that in the result population no solution appears twice.
        Moreover, the best individual of the new population must be at least as good as the best one of the old population.

        :param population: The calling algorithm's current population.
        """
        pass


class Selection(ABC):
    """
    An interface that is used to configure, how to select the individuals for the next generation.

    In fact, it is a factory that produces instances of the interface :class:`Selector`.
    """
    @abstractmethod
    def initialise(self, problem: BinaryQuadraticModel) -> Selector:
        """
        Instantiates and configures a implementors of the interface `Selector`.

        :param problem: The problem that should be optimised in the current run.
        """
        pass
