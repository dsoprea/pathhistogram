import unittest
import os
import tempfile
import contextlib
import shutil
import io

import pathhistogram.histogram
import pathhistogram.test_support


class TestHistogram(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.maxDiff = None
        super(TestHistogram, self).__init__(*args, **kwargs)

    def test_read_files(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path, max_files=10)

            h = pathhistogram.histogram.Histogram()
            files, largest_size = h.read_files(path)

            self.assertEquals(largest_size, 35)

            files = sorted(files)

            expected = [
                ('file0', 1),
                ('file1', 2),
                ('file2', 2),
                ('file3', 3),
                ('file4', 4),
                ('file5', 6),
                ('file6', 9),
                ('file7', 14),
                ('file8', 22),
                ('file9', 35),
            ]

            self.assertEquals(files, expected)

    def test_load_histogram(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path)

            h = pathhistogram.histogram.Histogram()

            files, largest_size = h.read_files(path)
            binned_files, slice_size = h.load_histogram(files, largest_size, 20)

            self.assertEquals(int(slice_size), 43791)

            for i, files in binned_files.copy().items():
                binned_files[i] = sorted(files)

            expected = {
                0: sorted(['file20', 'file14', 'file15', 'file9', 'file21', 'file19', 'file17', 'file12', 'file18', 'file3', 'file5', 'file4', 'file23', 'file2', 'file6', 'file13', 'file8', 'file16', 'file7', 'file0', 'file10', 'file1', 'file11', 'file22']),
                1: ['file24', 'file25'],
                2: ['file26'],
                3: [],
                4: ['file27'],
                5: [],
                6: [],
                7: ['file28'],
                8: [],
                9: [],
                10: [],
                11: ['file29'],
                12: [],
                13: [],
                14: [],
                15: [],
                16: [],
                17: [],
                18: [],
                19: ['file30'],
            }

            self.assertEquals(binned_files, expected)

    def test_load_histogram__filter(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path)

            h = pathhistogram.histogram.Histogram()

            filters = [
                'file1*',
            ]

            files, largest_size = h.read_files(path, filters=filters)
            binned_files, slice_size = h.load_histogram(files, largest_size, 20)

            self.assertEquals(int(slice_size), 220)

            for i, files in binned_files.copy().items():
                binned_files[i] = sorted(files)

            expected = {
                0: ['file1', 'file10', 'file11', 'file12'],
                1: ['file13', 'file14'],
                2: ['file15'],
                3: [],
                4: ['file16'],
                5: [],
                6: [],
                7: ['file17'],
                8: [],
                9: [],
                10: [],
                11: ['file18'],
                12: [],
                13: [],
                14: [],
                15: [],
                16: [],
                17: [],
                18: [],
                19: ['file19']
            }

            self.assertEquals(binned_files, expected)

    def test_print_histogram(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path)

            h = pathhistogram.histogram.Histogram()

            files, largest_size = h.read_files(path)
            binned_files, slice_size = h.load_histogram(files, largest_size, 20)

            s = io.StringIO()
            h.print_histogram(binned_files, slice_size, f=s)

            output = s.getvalue()

            # Strip all of the lines.
            output = '\n'.join([line.rstrip() for line in output.split('\n')])

            expected = """\
(31) files found.

    0.0B 24 *****************************************************************************
  43.79K  2 ******
  87.58K  1 ***
 131.37K  0
 175.17K  1 ***
 218.96K  0
 262.75K  0
 306.54K  1 ***
 350.33K  0
 394.12K  0
 437.92K  0
 481.71K  1 ***
  525.5K  0
 569.29K  0
 613.08K  0
 656.87K  0
 700.67K  0
 744.46K  0
 788.25K  0
 832.04K  1 ***
"""

            self.assertEquals(output, expected)

    def test_print_histogram__minimum(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path)

            h = pathhistogram.histogram.Histogram()

            files, largest_size = h.read_files(path, minimum_size=int(43.80 * 1024.0))
            binned_files, slice_size = h.load_histogram(files, largest_size, 20)

            s = io.StringIO()
            h.print_histogram(binned_files, slice_size, f=s)

            output = s.getvalue()

            # Strip all of the lines.
            output = '\n'.join([line.rstrip() for line in output.split('\n')])

            expected = """\
(7) files found.

    0.0B 0
  43.79K 2 ****************************
  87.58K 1 **************
 131.37K 0
 175.17K 1 **************
 218.96K 0
 262.75K 0
 306.54K 1 **************
 350.33K 0
 394.12K 0
 437.92K 0
 481.71K 1 **************
  525.5K 0
 569.29K 0
 613.08K 0
 656.87K 0
 700.67K 0
 744.46K 0
 788.25K 0
 832.04K 1 **************
"""

            self.assertEquals(output, expected)

    def test_print_histogram__maximum(self):
        with pathhistogram.test_support.get_temp_path() as path:
            pathhistogram.test_support.populate_path(path)

            h = pathhistogram.histogram.Histogram()

            files, largest_size = h.read_files(path, maximum_size=832000)
            binned_files, slice_size = h.load_histogram(files, largest_size, 20)

            s = io.StringIO()
            h.print_histogram(binned_files, slice_size, f=s)

            output = s.getvalue()

            # Strip all of the lines.
            output = '\n'.join([line.rstrip() for line in output.split('\n')])

            expected = """\
(30) files found.

    0.0B 23 ****************************************************************************
  27.06K  2 ******
  54.13K  1 ***
  81.19K  0
 108.26K  1 ***
 135.32K  0
 162.39K  0
 189.45K  1 ***
 216.52K  0
 243.58K  0
 270.65K  0
 297.71K  1 ***
 324.78K  0
 351.84K  0
 378.91K  0
 405.97K  0
 433.04K  0
  460.1K  0
 487.17K  0
 514.23K  1 ***
"""

            self.assertEquals(output, expected)
