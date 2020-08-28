============
Contributing
============

Bug reports, feature suggestions and other contributions are greatly
appreciated! While I can't promise to implement everything, I will always try
to respond in a timely manner.

You can also contribute by testing pull request or performing code reviews.  If
you help out in ways that don't involve hacking the code, please add your name
under the **Thanks** header in the ``AUTHORS.rst`` file.  We appreciate the
time you have given to improve this project.

Short version
=============

* Submit bug reports and feature requests at `GitHub <https://github.com/aburrell/aacgmv2/issues>`_
* Make pull requests to the ``develop`` branch

Bug reports
===========

When `reporting a bug <https://github.com/aburrell/aacgmv2/issues>`_ please
include:

* Your operating system name and version
* Any details about your local setup that might be helpful in troubleshooting
* Detailed steps to reproduce the bug

Feature requests and feedback
=============================

The best way to send feedback is to file an issue at
`GitHub <https://github.com/aburrell/aacgmv2/issues>`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions
  are welcome :)

Development
===========

To set up `aacgmv2` for local development:

1. `Fork aacgmv2 on GitHub <https://github.com/aburrell/aacgmv2/fork>`_.
2. Clone your fork locally::

    git clone git@github.com:your_name_here/aacgmv2.git

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally. Add tests for bugs and new features
   in ``tests/test_py_aacgmv2.py`` (for the wrapper), ``test_c_aacgmv2.py``
   (for the C extension), or ``tests/test_cmd_aacgmv2.py`` (for the
   command-line interface). ``tests/test_dep_aacgmv2.py`` includes tests for
   deprecated functions.  The tests are run with ``py.test`` and can be
   written as normal functions (starting with ``test_``) containing a standard
   ``assert`` statement for testing output, or use the numpy testing suite.

4. When you're done making changes, run all the checks, doc builder and spell
   checker with `tox <https://tox.readthedocs.io/en/latest/install.html>`_ [1]_::

    tox

5. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Brief description of your changes"
    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website. Pull requests should be
   made to the ``develop`` branch.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code, just
make a pull request.

For merging, you should:

1. Include passing tests (run ``tox``) [1]_
2. Update/add documentation if relevant
3. Add a note to ``CHANGELOG.rst`` about the changes
4. Add yourself to ``AUTHORS.rst``

.. [1] If you don't have all the necessary Python versions available locally or
       have trouble building all the testing environments, you can rely on
       Travis and AppVeyor - they will run the tests for each change you add in
       the pull request.

Tips
----

To run a subset of tests::

    tox -e envname -- py.test -k test_myfeature

To run all the test environments in parallel (you need to ``pip install detox``)::

    detox
