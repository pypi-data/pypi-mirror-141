from itertools import accumulate
from functools import lru_cache
from statistics import median, mean, pstdev
from math import gcd

from numpy import log2, ndarray, float64, asarray

from tabulate import tabulate

from lvr.helpers import min_decimals, split_attr, in_bounds
from lvr.helpers import round_or_reasonable, entry2relation
from lvr.helpers import list_dict, skip_equivalent_effect_values
from lvr.helpers import merge_dicts


class Pareto:
    """Determines when a pareto distribution is present.

    Args:
        effects (iterable[number]): Effect values (≥ 0).
        decimals (Optional[int], default 2): Number of decimals to round to.

    1. Firstly, it calculates the entropy of values.
    2. Then it stretches benchmark of `[0.6, 0.1, 0.1, 0.1, 0.1]`
       to count of values by maintaining absolute entropy.
    3. In turn it divides entropy of values through entropy of benchmark.
    4. Whenever the entropy of the values is less than the
       benchmark (1 or less), a pareto distribution should be assumed.

    Example:

        >>> Pareto([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
        0.71
    """
    def __init__(self, effects, decimals=2):
        self.decimals = decimals
        self.effects = list(effects)
        self.n = len(effects)

    @property
    def control_limit(self):
        """Returns entropy of control group with
        same number of actual elements."""
        factor = self.n/5
        majority = 0.6 * log2(0.6/factor)
        minority = 0.4 * log2(0.4/(4*factor))
        return -1 * majority - minority

    @property
    def entropy(self):
        """Returns entropy of actual elements."""
        total = sum(self.effects)
        less_zeros = list(filter(lambda x: x != 0, self.effects)) # test case: with titanic_fares!
        the_array = asarray(less_zeros, dtype=float64)
        shares = the_array/total
        return -sum(log2(shares)*shares)

    @property
    def ratio(self):
        """Returns ratio of entropies actual elements vs. control group."""
        return round(self.entropy/self.control_limit, self.decimals)

    def __bool__(self):
        """Tells whether a pareto distribution is present.
        That is if entropy of actual elements is less or equal than
        the same of the control group."""
        return self.ratio <= 1

    def __repr__(self):
        return '{}'.format(self.ratio)


class Lvr:
    """Chief facility to explore cause-effect characteristics of
    a given list of effect (and optional cause) values.

    **Primary methods:**

    * Overview of relevant cause-effect relationships?
      => :meth:`lvr.Lvr.tbl`
    * Search for a specific cause-effect relationship?
      => :meth:`lvr.Lvr.summary`

    **Additional methods:**

    * :meth:`lvr.Lvr.select` restricts the list of :meth:`lvr.Lvr.tbl`
      incorporating :class:`lvr.Selector`.
    * :meth:`lvr.Lvr.first` returns the first, :meth:`lvr.Lvr.last` the last element of the restricted list.
    * :meth:`lvr.Lvr.throughput` determines the time and result share
      for elements selected by :class:`lvr.Selector` at a given `capacity`.
    * :meth:`lvr.Lvr.accounting` translates the different throughput for
      all elements, the vital few only and the useful many only
      into income statements employing `capex` and `opex` shares.

    Args:
        effects (Optional[iterable[number]], default None):
          Effect values (≥ 0)
        causes (Optional[iterable[number]], default None): Cause values.
        list_dict (Optional[:class:`~lvr.helpers.list_dict`], default None):
          List of dicts with cause and effect values,
          their cumulative values and indices.
        descending (Optional[bool], default True):
          Sort effect values (more precise: effect\/cause value ratio)
          from biggest to smallest.
        decimals (Optional[int], default 2): Number of decimals to round to.

    .. note::

        You may provide `effects` only or `effects` with `causes`.
        Alternatively you can provide a `list_dict` directly;
        but _not_ `effects` and\/or `causes` and `list_dict` together.
    """
    def __init__(self, effects=None, causes=None, list_dict=None,
                 descending=True, decimals=2):
        if list_dict is not None:
            if effects or causes:
                raise ValueError('You may provide only '
                                 '`lvr.helpers.list_dict` '
                                 'or `effects` optional with `causes` '
                                 'but not both') # test this
            self.src_dicts = list_dict
        elif effects:
            if not causes:
                self.src_dicts = self._only_effects_(effects)
            else:
                self.src_dicts = self._causes_effects_(causes, effects)
        self.decimals = decimals
        self.descending = descending

    @property
    def _effects_(self):
        return list(map(lambda x: x['effect'], self.src_dicts))

    @lru_cache(maxsize=32)
    def _the_dicts_(self, descending):
        return sorted(self.src_dicts,
                      key=lambda x: self._powerfulness_(x),
                      reverse=descending)


    def _only_effects_(self, values):
        return [dict(effect=value, cause=1, index=index)
                for value, index in zip(values, range(len(values)))]

    def _causes_effects_(self, causes, effects):
        return list(map(lambda x: dict(cause=x[0], effect=x[1], index=x[2]),
                    zip(causes, effects, range(len(causes)))))

    def _powerfulness_(self, entry):
        return entry['effect']/entry['cause']

    def _ranks_(self, descending):
        for c, e in self.tbl(descending).items():
            if int(c*100) == 0:
                yield 0
            else:
                #yield gcd(int(c*100), int(e*100))/e
                yield 1/e*(e/c)**2

    @property
    def ratio(self):
        """entropy of given values / control group."""
        return round(Pareto(self._effects_).ratio, 3)

    @lru_cache(maxsize=64)
    def running_share(self, descending):
        """Returns extended list of dicts of running cause-effect
        relations, including indices and cause and effect values.

        Args:
            descending (bool):
              Sort effect values (more precise: effect\/cause
              value ratio) from biggest to smallest.
        """
        the_dicts = self._the_dicts_(descending)
        causes = list(map(lambda x: x['cause'], the_dicts))
        effects = list(map(lambda x: x['effect'], the_dicts))
        indices = list(map(lambda x: x['index'], the_dicts))
        total_causes = sum(causes)
        total_effects = sum(effects)
        return [dict(cause=cause, effect=effect, cucau=the_causes/total_causes,
                     cueff=the_effects/total_effects, index=index)
                for cause, effect, the_causes, the_effects, index in
                    zip(causes, effects, accumulate(causes),
                        accumulate(effects), indices)]


    def summary(self, effects=None, causes=None, guess=False,
                descending=None, decimals=None):
        """Returns cause effect relation that is nearest to `effects`.

        Args:
            effects (number, default 0.5): Cumulative effect value
              to attain distribution to.
            causes (Optional[number], default None): Cumulative cause
              value to attain distribution to.
            guess (bool, default False): Determine most relevant
              cause-effect relation automatically.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int]): Number of decimals to round to.

        Examples:

            :meth:`lvr.Lvr.summary` is your friend::

                >>> Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9]).summary()
                {'causes': 0.1, 'effects': 0.46, 'entropy_ratio': 0.71, 'pareto': True}

            :meth:`lvr.Lvr.summary` returns you a relation near 50 percent
            of effects.

            You may insist on a specific *effects* threshold::

                >>> Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9]).summary(effects=0.8)
                {'causes': 0.2, 'effects': 0.8, 'entropy_ratio': 0.71, 'pareto': True}

            Alike for a *causes* threshold::

                >>> Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9]).summary(causes=0.2)
                {'causes': 0.2, 'effects': 0.8, 'entropy_ratio': 0.71, 'pareto': True}

        **Rule of 50\/5:**

        *The rule 50\/5 means that 50 percent of causes make up 5 percent of effects.*

        .. code-block:: python

            >>> from lvr import Lvr
            >>> from lvr.data import forest_fires, meteorites, debris_masses
            >>> Lvr(forest_fires()).summary()
            {'causes': 0.014, 'effects': 0.5, 'entropy_ratio': 0.8, 'pareto': True}

        50 percent of forest fire area goes back to 1.4 percent of fires.

        .. code-block:: python

            >>> dm = Lvr(debris_masses())
            >>> dm.first(s, descending=False)
            {'causes': 0.02, 'effects': 0.5, 'entropy_ratio': 0.73, 'pareto': True}

        50 percent of total mass is made up by 2 percent of debris.

        .. code-block:: python

            >>> Lvr(meteorites()).summary()
            {'causes': 0.004, 'effects': 0.5, 'entropy_ratio': 0.71, 'pareto': True}

        50 percent of total mass is made up by 0.4 percent of meteorites only.
        """
        descending = descending if descending is not None else self.descending

        if causes and effects:
            raise ValueError('Specify `causes` or `effects` but not both.')

        if guess and causes is not None and effects is not None:
            raise ValueError('If you use `guess`, do not '
                             'use `causes` or `effects`')
        if guess:
            effects = tuple(self.best().items())[0][1]
        elif causes is None and effects is None:
            effects = 0.5 # default value

        rs = self.running_share(descending=True)
        if effects is not None:
            indexed_diffs = [(r['index'], abs(effects-r['cueff']))
                             for r in rs]
        else:
            indexed_diffs = [(r['index'], abs(causes-r['cucau']))
                             for r in rs]

        index_asc, diff_asc = sorted(indexed_diffs,
                                     key=lambda x: x[1])[0] # [0] is risky
        selected = [r for r in rs
                    if r['index'] == index_asc][0] # [0] is risky

        if not descending:
            selected['cucau'] = 1-selected['cucau']
            selected['cueff'] = 1-selected['cueff']

        return dict(causes=round_or_reasonable(selected['cucau'], decimals),
                    effects=round_or_reasonable(selected['cueff'], decimals),
                    entropy_ratio=self.ratio,
                    pareto=self.ratio <= 1)


    def tbl(self, descending=None, decimals=None):
        """Returns dictionary of most relevant
        cumulative cause-effect relations.

        Args:
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int]): Number of decimals to round to.

        Example:
            >>> l = Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
            >>> l.tbl()
            {0.1: 0.46, 0.2: 0.8, 0.3: 0.9, 0.6: 0.96, 0.9: 1.0}
        """
        descending = descending if descending is not None else self.descending
        causes = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.33, 0.4]
        effects = [0.5, 0.6, 0.66, 0.7, 0.75, 0.8, 0.9, 0.95, 0.99]

        def selcau(cause):
            s = Selector(causes=cause)
            result = self.first(s, descending, extended=True)
            return (result['cucau'], result['cueff'])

        def seleff(effect):
            s = Selector(effects=effect)
            result = self.first(s, descending, extended=True)
            return (result['cucau'], result['cueff'])

        def the_causes(causes):
            result = dict()
            for cause in causes:
                cucaueff = selcau(cause)
                actual_cucause = round_or_reasonable(cucaueff[0], decimals)
                actual_cueffect = round_or_reasonable(cucaueff[1], decimals)
                result[actual_cucause] = actual_cueffect
            return result


        def the_effects(effects):
            result = dict()
            for effect in effects:
                cucaueff = seleff(effect)
                actual_cucause = round_or_reasonable(cucaueff[0], decimals)
                actual_cueffect = round_or_reasonable(cucaueff[1], decimals)
                result[actual_cucause] = actual_cueffect
            return result

        both = dict(the_causes(causes))
        both.update(the_effects(effects))
        return skip_equivalent_effect_values(both)

    def select(self, selector=None, descending=None,
               decimals=None, extended=False):
        """Returns dictionary of cumulative cause-effect
        relations selected by selector.

        Args:
            selector (Optional[:class:`~lvr.Selector`], default None):
              Subset definition.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int]): Number of decimals to round to.
            extended (Optional[bool], default False):
              Return extended list of dicts.

        Example:

            >>> l = lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
            >>> s = Selector(causes=(0, 0.2))
            >>> l.select(s)
            {0.1: 0.46, 0.2: 0.8}

        """
        selector = selector if selector is not None else Selector()
        descending = descending if descending is not None else self.descending
        results = filter(selector.selected, self.running_share(descending))
        if extended:
            return list(results)
        else:
            merged = merge_dicts(list(map(lambda x: entry2relation(x, decimals),
                                          results)))
            return skip_equivalent_effect_values(merged)

    def best(self, descending=None, decimals=None):
        """Returns most relevant cumulative cause-effect relation.

        Args:
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int], default None): Number of
              decimals to round to.
        """
        highest = 0
        the_cause = None
        descending = descending if descending is not None else self.descending
        for (cause, effect), rank in zip(self.tbl(descending,
                                                  decimals).items(),
                                         self._ranks_(descending)):
            if descending:
                if effect < 0.5 or cause > 0.5:
                    continue
            elif not descending:
                if cause < 0.5 or effect > 0.5:
                    continue
            the_rank = (rank**10 if cause+effect >= 0.98 and
                                    cause+effect <= 1.02 else rank)
            if the_rank > highest:
                highest = the_rank
                the_cause = cause
        if the_cause:
            return {the_cause: self.tbl(descending)[the_cause]}

    def indices(self, selector, descending=None, counterpart=False):
        """Returns indices of elements selected by `selector`.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            counterpart (Optional[bool], default False): Return result
              of complement if `True`.
        """
        descending = descending if descending is not None else self.descending
        selected = list(filter(selector.selected,
                               self.running_share(descending)))
        if counterpart:
            result = list(filter(lambda x: x not in selected,
                                 self.running_share(descending)))
        else:
            result = selected
        return list(map(lambda x: x['index'], result))

    def effect_values(self, selector, descending=None, counterpart=False):
        """Returns effect_values selected by `selector`.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            counterpart (Optional[bool], default False): Return result
              of complement if `True`.
        """
        descending = descending if descending is not None else self.descending
        effect_values = []
        selected = list(filter(selector.selected,
                               self.running_share(descending)))
        if counterpart:
            result = list(filter(lambda x: x not in selected,
                                 self.running_share(descending)))
            #print('in counterpart: ', result)
            return list(map(lambda x: x['effect'], result))
        else:
            return list(map(lambda x: x['effect'], selected))

    def separate(self, selector, descending=None, decimals=None):
        """Shows effect of separating elements by `selector` on spread of
        mean and median and stdev\/mean ratio for all elements, vital few only
        and useful many only.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int], default None): Number of
              decimals to round to.

        Usually mean\/median and stdev\/mean ratio drop for each subset compared
        to all elements.

        Example:

            >>> l = Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
            >>> s = Selector(causes=(0, 0.2))
            >>> l.separate(s)
            GROUP          MEAN/MEDIAN    STDEV/MEAN
            -----------  -------------  ------------
            {1: 1}                4.59          1.57
            {0.1: 0.46}           1             0.12
            {0.9: 0.54}           1.37          0.81
        """

        descending = descending if descending is not None else self.descending

        def mean_vs_median(values):
            return round(mean(values)/median(values), self.decimals)

        def stdev_vs_mean(values):
            return round(pstdev(values)/mean(values), self.decimals)

        complete = self.effect_values(Selector(), descending)
        vfew = self.effect_values(selector, descending)
        umany = self.effect_values(selector, descending, counterpart=True)
        entry = self.first(selector, descending, extended=True)
        counterpart = {round_or_reasonable(1-entry['cucau'], decimals):
                       round_or_reasonable(1-entry['cueff'], decimals)}
        relation = entry2relation(entry, decimals)
        result = [{'group': {1: 1},
                   'mean/median': mean_vs_median(complete),
                   'stdev/mean': stdev_vs_mean(complete)},
                  {'group': relation,
                   'mean/median': mean_vs_median(vfew),
                   'stdev/mean': stdev_vs_mean(vfew)},
                  {'group': counterpart,
                   'mean/median': mean_vs_median(umany),
                   'stdev/mean': stdev_vs_mean(umany)}]
        return result

    def _calc_delta_(self, lower, upper, decimals=None):
        causes_delta = upper['cucau']-lower['cucau']
        effects_delta = upper['cueff']-lower['cueff']
        return {round_or_reasonable(causes_delta, decimals):
                round_or_reasonable(effects_delta, decimals)}

    def __repr__(self):
        best = self.best
        if best:
            (cause, effect) = tuple(best().items())[0]
            ratio = self.ratio
            txt = 'PARETO '
            if ratio <= 1:
                txt += 'PRESENT'
            else:
                txt += 'NOT PRESENT'
            return '{} => {} [{} {}]'.format(cause, effect, txt, ratio)
        else:
            return ''

    def first(self, selector, descending=None, decimals=None, extended=False):
        """Returns first cumulative cause-effect relation
        selected by `selector`.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int], default None): Number of
              decimals to round to.
            extended (Optional[bool], default False): Returns
              extended list of dicts.
        """
        descending = descending if descending is not None else self.descending
        result = self.select(selector, descending, extended=True)[0]
        if extended:
            return result
        else:
            return entry2relation(result, decimals)

    def last(self, selector, descending=None, decimals=None, extended=False):
        """Returns last cumulative cause-effect relation
        selected by `selector`.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int], default None): Number of
              decimals to round to.
            extended (Optional[bool], default False): Returns
              extended list of dicts.
        """
        descending = descending if descending is not None else self.descending
        result = self.select(selector, descending, extended=True)[-1]
        if extended:
            return result
        else:
            return entry2relation(result, decimals)

    def throughput(self, selector, capacity, descending=None,
                   counterpart=False, decimals=None):
        """Tells how much periods are required to process elements
        selected by `selector` at given `capacity` per period.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            capacity (number): Available capacity (causes per period).
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            counterpart (Optional[bool], default False): Return result
              of complement if `True`.
            decimals (Optional[int], default None): Number of
              decimals to round to.

        Example:

            >>> l = Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
            >>> l = Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
            >>> s = Selector(causes=(0, 0.2))
            >>> l.throughput(s, capacity=0.5)
            {'periods': 4.0, 'results': 0.8}

        We need four periods to get 80 percent of results.

            >>> s = Selector(effects=(0, 1))
            >>> l.throughput(s, capacity=0.5)
            {'periods': 20.0, 'results': 1.0}

        But for 100 percent, we need 20 periods.
        For the remaining 20 percentage points in results
        we need four times the previous time.
        """

        descending = descending if descending is not None else self.descending

        def sum_indices_key(indices, key, descending):
            filtered = filter(lambda x: x['index'] in indices,
                              self._the_dicts_(descending))
            extracted = map(lambda x: x[key],
                            filtered)
            return sum(extracted)

        complete_results = sum(map(lambda x: x['effect'],
                                   self._the_dicts_(descending)))
        complete_efforts = sum(map(lambda x: x['cause'],
                                   self._the_dicts_(descending)))

        indices = self.indices(selector, descending, counterpart)
        results = sum_indices_key(indices, 'effect', descending)
        efforts = sum_indices_key(indices, 'cause', descending)
        return dict(periods=round_or_reasonable(efforts/capacity, decimals),
                    results=round_or_reasonable(results/complete_results,
                                                decimals))

    def accounting(self, selector, capacity, capex, opex, descending=None,
                   counterpart=False, decimals=None):
        """Assess financial effect of putting through elements selected
        by `selector` at given `capacity`.

        Args:
            selector (:class:`~lvr.Selector`): Subset definition.
            capacity (number): Available capacity (causes per period).
            capex (number): Share of capital expenditures of revenue.
            opex (number): Share of operational expenditures of revenue.
            descending (Optional[bool]):
              Sort effect values (more precise: effect\/cause value ratio)
              from biggest to smallest.
            decimals (Optional[int], default None): Number of
              decimals to round to.

        `capex` and `opex` are shares, hence must add up to 1.

        Example:

            >>> l = Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
            >>> s = Selector(causes=(0, 0.2))
            >>> results = l.accounting(s, capacity=0.5, capex=0.55, opex=0.45)
            >>> from pandas import DataFrame # requires pandas module
            >>> pd = DataFrame.from_dict(results, orient='index')
            >>> pd.round(2)
                         periods  revenue  capex  opex  income  period_income
            complete_tp     20.0    100.0   55.0  45.0    -0.0          -0.00
            umany_tp        16.0     20.0   44.0  36.0   -60.0          -3.75
            vfew_tp          4.0     80.0   11.0   9.0    60.0          15.00

        We can get an income of 15 for each of four periods.
        Or an income of 0 for 20 periods.
        That is since the useful many incur a loss of -3.75 per period.
        """

        groups = dict(vfew_tp=self.throughput(selector, capacity),
                      umany_tp=self.throughput(selector, capacity,
                                               counterpart=True),
                      complete_tp=self.throughput(Selector(),
                                                  capacity))

        def income_statement(periods, total_periods, revenue,
                             capex, opex, decimals):
            result = dict(periods=periods,
                          revenue=100*revenue,
                          capex=capex*100*periods/total_periods,
                          opex=opex*100*periods/total_periods)
            result['income'] = (result['revenue']
                                -result['capex']-result['opex'])
            result['period_income'] = result['income']/periods

            return {key: round_or_reasonable(value, decimals)
                    for key, value in result.items()}

        stmts = dict()
        for name, results in groups.items():
            stmts[name] = income_statement(results['periods'],
                                           groups['complete_tp']['periods'],
                                           results['results'],
                                           capex,
                                           opex,
                                           decimals)
        return stmts



class Selector:
    """Selector specifies a subset to retrieve from cause-effect relations.

    `causes=0.2` will select a range from 0.2 to 1.0 of causes.
    `effects` works alike.

    Examples:

        >>> s = Selector(causes=0.2)
        >>> Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9]).first(s)
        {0.2: 0.8}

        >>> s = Selector(causes=0.2, effects=(0.6, 0.95))
        >>> Lvr([789, 621, 109, 65, 45, 30, 27, 15, 12, 9]).first(s)
        {0.5: 0.95}
    """

    def __init__(self, causes=None, effects=None):
        self.causes = (split_attr(causes) if causes
                         else {'lower': 0, 'upper': 1})
        self.effects = (split_attr(effects) if effects
                         else {'lower': 0, 'upper': 1})

    def selected(self, entry):
        causes = self.causes is None or in_bounds(entry['cucau'],
                                                  self.causes['lower'],
                                                  self.causes['upper'])
        effects = self.effects is None or in_bounds(entry['cueff'],
                                                    self.effects['lower'],
                                                    self.effects['upper'])
        return causes and effects
