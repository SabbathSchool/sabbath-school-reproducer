Installation
============

This page provides instructions for installing the Sabbath School Lessons Reproducer package.

From PyPI
---------

The simplest way to install the package is using pip:

.. code-block:: bash

   pip install sabbath-school-reproducer

This will install the latest stable version along with all required dependencies.

From Source
-----------

To install from source for development:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/SabbathSchool/sabbath-school-reproducer.git
      cd sabbath-school-reproducer

2. Install in development mode:

   .. code-block:: bash

      pip install -e .

Dependencies
-----------

The package requires the following dependencies:

* Python 3.6+
* pyyaml
* requests
* markdown
* weasyprint
* beautifulsoup4

System Requirements
------------------

For PDF generation using WeasyPrint, you may need additional system dependencies:

**On Ubuntu/Debian:**

.. code-block:: bash

   apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

**On macOS:**

.. code-block:: bash

   brew install cairo pango gdk-pixbuf libffi

**On Windows:**

WeasyPrint has specific requirements for Windows. See the `WeasyPrint documentation <https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows>`_ for details.

Verifying Installation
---------------------

To verify that the installation was successful, run:

.. code-block:: bash

   sabbath-school-reproducer --version

This should display the version number of the installed package.