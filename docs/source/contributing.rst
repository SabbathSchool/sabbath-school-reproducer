Contributing
============

Thank you for your interest in contributing to the Sabbath School Lessons Reproducer! This page provides guidelines for contributing to the project.

Setting Up Development Environment
---------------------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/SabbathSchool/sabbath-school-reproducer.git
      cd sabbath-school-reproducer

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install in development mode:

   .. code-block:: bash

      pip install -e .
      pip install -r requirements-dev.txt

Code Standards
-------------

* Follow PEP 8 style guidelines
* Use docstrings for all modules, classes, and functions
* Write unit tests for new functionality
* Keep functions focused and reasonably sized

Workflow for Contributing
------------------------

1. Create a fork of the repository
2. Clone your fork to your local machine
3. Create a feature branch:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

4. Make your changes and commit them:

   .. code-block:: bash

      git add .
      git commit -m "Description of your changes"

5. Push your changes to your fork:

   .. code-block:: bash

      git push origin feature/your-feature-name

6. Create a pull request from your fork to the main repository

Adding New Features
------------------

When adding new features:

1. Start by creating an issue to discuss the feature
2. Write tests for the new functionality
3. Update documentation to reflect the changes
4. Submit a pull request

Testing
-------

Run the test suite with pytest:

.. code-block:: bash

   pytest

For more thorough testing:

.. code-block:: bash

   pytest --cov=sabbath_school_reproducer tests/

Building Documentation
---------------------

To build the documentation:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in the ``docs/_build/html`` directory.

Releasing
---------

The release process is automated through GitHub Actions when a new tag is created.

To prepare a release:

1. Update version in ``__init__.py``
2. Update CHANGELOG.md
3. Commit changes:

   .. code-block:: bash

      git add .
      git commit -m "Prepare for release X.Y.Z"

4. Tag the release:

   .. code-block:: bash

      git tag vX.Y.Z
      git push origin vX.Y.Z

5. The GitHub Actions workflow will build and publish the package to PyPI

Code of Conduct
--------------

Please be respectful and considerate of others when contributing. We aim to foster an inclusive and welcoming community.

License
-------

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.