Usage
=====

This page describes how to use the Sabbath School Lessons Reproducer.

Quick Start
----------

1. Generate a configuration file:

   .. code-block:: bash

      sabbath-school-reproducer --generate-config

2. Edit the generated ``config.yaml`` file with your desired settings.

3. Run the downloader:

   .. code-block:: bash

      sabbath-school-reproducer config.yaml

Basic Commands
-------------

Generate a Configuration File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sabbath-school-reproducer --generate-config

This will create a template configuration file (``config.yaml``) in the current directory.

Process a Configuration File
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sabbath-school-reproducer path/to/config.yaml

This will download the specified lessons and generate a PDF based on the configuration.

Debug Mode
^^^^^^^^^^

.. code-block:: bash

   sabbath-school-reproducer config.yaml --debug

This enables verbose logging for troubleshooting.

Debug HTML Only
^^^^^^^^^^^^^^

.. code-block:: bash

   sabbath-school-reproducer config.yaml --debug-html-only

This generates only the debug HTML without the PDF, which is useful for inspecting the content before PDF generation.

Workflow Examples
----------------

Basic Reproduction
^^^^^^^^^^^^^^^^^

To reproduce lessons from 1905 Quarter 2 for use in 2025 Quarter 2:

1. Create a configuration file:

   .. code-block:: yaml

      year: 2025
      quarter: q2
      language: en
      input_file: ./combined_lessons_2025_q2.md
      output_file: ./output/sabbath_school_lesson_2025_q2.pdf
      
      reproduce:
        year: 1905
        quarter: q2
        quarter_start_date: 2025-04-01

2. Run the processor:

   .. code-block:: bash

      sabbath-school-reproducer config.yaml

Selected Lessons
^^^^^^^^^^^^^^^

To reproduce only lessons 3-7 from the original quarter:

.. code-block:: yaml

   reproduce:
     year: 1905
     quarter: q2
     start_lesson: 3
     stop_lesson: 7
     quarter_start_date: 2025-04-01

Using Custom Covers
^^^^^^^^^^^^^^^^^^

Add paths to custom SVG files for the covers:

.. code-block:: yaml

   front_cover_svg: ./assets/front_cover.svg
   back_cover_svg: ./assets/back_cover.svg

Output Files
-----------

The processor generates the following files:

1. A combined markdown file (specified by ``input_file``)
2. A debug HTML file (derived from the output PDF path with ``_debug.html``)
3. The final PDF (specified by ``output_file``)

These files are useful for troubleshooting and can be examined if there are issues with the output.