=====
nanto
=====


.. image:: https://img.shields.io/pypi/v/nanto.svg
        :target: https://pypi.python.org/pypi/nanto

.. image:: https://img.shields.io/travis/mmore500/nanto.svg
        :target: https://travis-ci.com/mmore500/nanto

.. image:: https://readthedocs.org/projects/nanto/badge/?version=latest
        :target: https://nanto.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




nanto makes working with values that might be NaN safer and easier


* Free software: MIT license
* Documentation: https://nanto.readthedocs.io.



.. code-block:: python3

  from nanto import isanan, nantonone, nantozero


  isanan(7.0) # False
  isanan('string') # False
  isanan(None) # False
  isanan(float('nan')) # True


  nanto(float('nan'), 'fallback') # returns 'fallback'
  nanto(1.7, 'fallback') # returns 1.7
  nanto(float('inf'), 'fallback') # returns inf
  nanto(None, 'fallback') # returns None
  nanto('hello', 'fallback') # returns 'hello'


  nantonone(float('nan')) # returns None
  nantonone(1.7) # returns 1.7
  nantonone(float('inf')) # returns inf
  nantonone(None) # returns None
  nantonone('hello') # returns 'hello'


  nantozero(float('nan')) # returns 0
  nantozero(1.7) # returns 1.7
  nantozero(float('inf')) # returns inf
  nantozero(None) # returns None
  nantozero('hello') # returns 'hello'


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
