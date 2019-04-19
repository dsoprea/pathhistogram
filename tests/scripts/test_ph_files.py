import unittest

import subprocess

import pathhistogram.test_support


class TestCommand(unittest.TestCase):
    def test_run(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path)

            cmd = ['ph_files', path]
            output = subprocess.check_output(cmd)
            output = output.decode('utf-8')

            # Strip all of the lines.
            output = '\n'.join([line.rstrip() for line in output.split('\n')])

            expected = """\
(31) files found.

    0.0B 24 *****************************************************************************
  28.69K  1 ***
  57.38K  1 ***
  86.07K  0
 114.76K  1 ***
 143.46K  0
 172.15K  1 ***
 200.84K  0
 229.53K  0
 258.22K  0
 286.91K  0
  315.6K  1 ***
 344.29K  0
 372.98K  0
 401.67K  0
 430.37K  0
 459.06K  0
 487.75K  1 ***
 516.44K  0
 545.13K  0
 573.82K  0
 602.51K  0
  631.2K  0
 659.89K  0
 688.59K  0
 717.28K  0
 745.97K  0
 774.66K  0
 803.35K  0
 832.04K  1 ***
"""

            self.assertEquals(output, expected)
