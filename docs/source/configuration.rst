Configuration
=============

This page provides details about configuring the Sabbath School Lessons Reproducer.

Configuration File Format
------------------------

The configuration is specified in YAML format. Below is a complete example with all available options:

.. code-block:: yaml

   # Target output options
   year: 2025              # Year for generated lessons
   quarter: q2             # Quarter (q1, q2, q3, q4)
   language: en            # Language code

   # File paths
   input_file: ./combined_lessons_2025_q2.md   # Path for intermediate markdown file
   output_file: ./output/sabbath_school_reproducer_2025_q2.pdf  # Final PDF path

   # Optional cover SVG files
   front_cover_svg: ./assets/front_cover.svg   # Custom front cover
   back_cover_svg: ./assets/back_cover.svg     # Custom back cover

   # Reproduction options
   reproduce:
     # Original content to adapt
     year: 1905            # Historical year to source from
     quarter: q2           # Historical quarter to source from
     
     # Lesson selection
     start_lesson: 1       # First lesson to include (starting from 1)
     stop_lesson: 13       # Last lesson to include (or null for all)
     
     # New date assignment
     quarter_start_date: 2025-04-01  # First lesson date (YYYY-MM-DD)

   # PDF metadata
   title: Sabbath School Lessons      # Title for the lesson quarterly
   subtitle: Quarter 2, 2025          # Subtitle
   publisher: Gospel Sounders         # Publisher name

Configuration Options
--------------------

Target Output Options
^^^^^^^^^^^^^^^^^^^^

* ``year`` (integer): The year for the generated lessons (e.g., 2025)
* ``quarter`` (string): The quarter identifier (q1, q2, q3, or q4)
* ``language`` (string): The language code (e.g., en, es)

File Paths
^^^^^^^^^^

* ``input_file`` (string): Path to save the combined markdown file
* ``output_file`` (string): Path to save the generated PDF

Cover Files
^^^^^^^^^^^

* ``front_cover_svg`` (string, optional): Path to SVG file for front cover
* ``back_cover_svg`` (string, optional): Path to SVG file for back cover

Reproduction Options
^^^^^^^^^^^^^^^^^^^

The ``reproduce`` section is optional and contains settings for adapting historical lessons:

* ``year`` (integer): Historical year to source from
* ``quarter`` (string): Historical quarter to source from
* ``start_lesson`` (integer, optional): First lesson to include (default: 1)
* ``stop_lesson`` (integer, optional): Last lesson to include (default: all)
* ``quarter_start_date`` (string): Start date for the first lesson in YYYY-MM-DD format

PDF Metadata
^^^^^^^^^^^

* ``title`` (string, optional): Title for the lesson quarterly
* ``subtitle`` (string, optional): Subtitle for the lesson quarterly
* ``publisher`` (string, optional): Publisher name

GitHub Repository Structure
--------------------------

The tool relies on the SabbathSchool/lessons GitHub repository structure:

.. code-block:: text

   /DECADE/YEAR/QUARTER/LANGUAGE/
     - contents.json
     - front-matter.md
     - back-matter.md
     - week-01.md
     - week-02.md
     - ...

Where:

* ``DECADE`` is formatted as, e.g., "1880s"
* ``YEAR`` is the full year, e.g., "1905"
* ``QUARTER`` is q1, q2, q3, or q4
* ``LANGUAGE`` is the language code, e.g., "en"

Environment Variables
--------------------

The tool supports the following environment variables:

* ``SSL_DEBUG``: Set to "1" to enable debug mode
* ``SSL_CONFIG_PATH``: Default path to look for configuration file