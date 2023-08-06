"""The building blocks for the core functions."""

import csv
from decimal import Decimal
from pkg_resources import resource_filename
from functools import reduce


def unfold_values(values):
    """Unfolds list of observation-frequency mappings.

    Args:
        values (tuple[number, int]): Observation-frequency mapping.

    Returns:
        List of values.

    Example:
        >>> from effectus.helpers import unfold_values
        >>> unfold_values([(1, 3), (2, 1), (3, 1)])
        [1, 1, 1, 2, 3]
    """
    result = []
    for observation, frequency in values:
        result += [observation] * frequency
    return result


def get_values_from_csv(csv_reader, observations_col=1, frequency_col=2):
    """Gets values from csv file.

    Args:
        csv_reader:
        observations_col (int, default 1): Column number of observations.
        frequency_col (int, default 2): Column number of frequency.
          if < 0 or csv file has only one column, values will only
          be considered.

    Returns:
        A list of observation-frequency tuples like::

            [(23.3, 1), (80.1, 3), (99.3, 2)]
    """
    result = []
    for row in csv_reader:
        try:
            observation = float(row[observations_col-1])
            frequency = 1
        except (ValueError, IndexError):
            continue
        if len(row) > 1:
            try:
                if frequency_col < 0:
                    frequency = 1
                else:
                    frequency = int(row[frequency_col-1])
            except (ValueError, IndexError):
                raise ValueError
        else:
            frequency = 1
        result.append((observation, frequency))
    return result


def get_data(filepath, observations_col=1, frequencies_col=2):
    """Read and unfold value-frequency mappings from file.

    Args:
        filepath (str): File path to source file.
        observations_col (Optional[int], default 1): Column of observations.
        frequencies_col (Optional[int], default 2): Only relevant if
          file has more than two comma separated columns.

          .. note::
              Set this to -1 to deactivate value-frequency mode for a file
              having more than one column.

    Returns:
        A list of unfolded values.
    """
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        vafreqs = get_values_from_csv(reader, observations_col, frequencies_col)
        return unfold_values(vafreqs)


def get_example(filepath):
    """Read and unfold value-frequency mappings from example file.

    Args:
        filepath (str): File path to source file.

    Returns:
        A list of unfolded values.
    """
    return get_data(resource_filename(__name__, filepath))

# FIXME 2017-12-26: what if 0.7366 gets rounded up to 0.74
#   and then first_non_zero considers 0.7366 as input but should 0.74!
def min_decimals(number):
    number = str(Decimal(number))
    if '.' not in number:
        return 1
    _, decimals = number.split('.')
    scinot = decimals.split('E')
    if len(scinot) > 1:
        scinot_count = -int(scinot[1])
        decimals = scinot[0]
    else:
        scinot_count = None

    fnz = first_non_zero(decimals, count=scinot_count or 1)
    if len(decimals) > fnz:
        if decimals[fnz] in '456':
            fnz += 1
    return fnz


def first_non_zero(the_string, count=1):
    for c in the_string:
        if c != '0':
            break
        count += 1
    return count


def round_reasonable(number):
    return round(number, min_decimals(number))


def round_or_reasonable(number, decimals):
    if decimals:
        return round(number, decimals)
    else:
        return round_reasonable(number)


def list_dict(src_dict, effect, cause=None):
    """Constructs list of dicts to feed :class:`lvr.Lvr` with.

    Args:
        src_dict (dict): Dictionary like
          {'elem1': 'attr1': 45, 'attr2': 56}, ...}.
        effect (str): Name of key of effect value.
        cause (:obj:`str`, optional): Name of key of cause value."""

    if cause is None:
        def build_entry(key, values):
            return dict(index=key,
                        cause=1,
                        effect=values[effect])
    else:
        def build_entry(key, values):
            return dict(index=key,
                        cause=values[cause],
                        effect=values[effect])
    result = map(lambda x: build_entry(x[0], x[1]),
                 src_dict.items())
    return list(result)


def split_attr(attr):
    result = dict()
    if isinstance(attr, list) or isinstance(attr, tuple):
        result['lower'], result['upper'] = attr
    else:
        result['lower'] = attr
        result['upper'] = 1
    return result


def in_bounds(value, lower, upper):
            if lower is None and upper is None:
                return True
            elif lower is not None and upper is not None:
                return lower <= value <= upper
            elif lower is None:
                return value <= upper
            elif upper is None:
                return lower <= value


def entry2relation(entry, decimals=None):
    return {round_or_reasonable(entry['cucau'], decimals):
            round_or_reasonable(entry['cueff'], decimals)}


def skip_equivalent_effect_values(causes_effects):
    """Returns only first key: value mapping for equivalent
    effect values."""
    effects = set()
    result = dict()
    for cause, effect in causes_effects.items():
        if effect not in effects:
            effects.add(effect)
            result[cause] = effect
    return result


def merge_dicts(dicts):
    return reduce(lambda x, y: x.update(y) or x, dicts, {})
