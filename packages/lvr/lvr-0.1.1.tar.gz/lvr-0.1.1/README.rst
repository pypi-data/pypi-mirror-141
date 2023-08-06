**Lvr**
*******

*lvr* tells you which causes provoke which effects:

.. code-block:: python

    >>> from lvr import Lvr
    >>> values = [789, 621, 109, 65, 45, 30, 27, 15, 12, 9]
    >>> Lvr(values).summary(guess=True)
    {'causes': 0.2, 'effects': 0.8, 'entropy_ratio': 0.71, 'pareto': True}

Links
=====

  * code repository: https://bitbucket.org/hyllos/lvr
  * docs: https://lvr.rtfd.io
