import sys
import os
import fnmatch
import math


class Histogram(object):
    def read_files(
            self, root_path, filters=[], minimum_size=None, maximum_size=None):
        root_path = root_path.rstrip(os.sep)
        prefix_len = len(root_path)
        files = []
        largest_size = 0
        for path, _, filenames in os.walk(root_path):
            for filename in filenames:
                if filters:
                    hit = False
                    for filter_filespec in filters:
                        if fnmatch.fnmatch(filename, filter_filespec) is True:
                            hit = True
                            break

                    if hit is False:
                        continue

                filepath = os.path.join(path, filename)

                if os.path.islink(filepath) is True:
                    s = os.lstat(filepath)
                else:
                    s = os.stat(filepath)

                filesize = s.st_size

                if minimum_size is not None and minimum_size > filesize:
                    continue
                elif maximum_size is not None and maximum_size < filesize:
                    continue

                largest_size = max(largest_size, filesize)

                filepath = os.path.join(path, filename)
                rel_filepath = filepath[prefix_len + 1:]
                files.append((rel_filepath, filesize))

        return files, largest_size

    def load_histogram(self, files, largest_size, n):
        assert \
            n > 0, \
            "N must be more than zero."

        largest_size = float(largest_size)

        binned_files = {
            i: []
            for i
            in range(int(n))
        }

        # Allocate one less bins so that the largest file (read: 100% of the
        # maximum size) will not be directed to a non-existent bin.
        n = float(n - 1)

        for rel_filepath, size in files:
            bin_ = float(size) / largest_size * n
            bin_ = int(math.floor(bin_))
            binned_files[bin_].append(rel_filepath)

        return binned_files, largest_size / n

    def print_histogram(self, binned_files, slice_size, f=None):
        if f is None:
            f = sys.stdout

        total_count = sum([
            len(files)
            for files
            in binned_files.values()
        ])

        f.write("({}) files found.\n".format(total_count))
        f.write("\n")

        count_width = int(math.log10(total_count)) + 1
        for i in range(len(binned_files)):
            tally = len(binned_files[i])
            slice_floor = slice_size * float(i)

            unit_name = 'B'

            if slice_floor > 1000:
                unit_name = 'K'
                slice_floor /= 1000.0

            if slice_floor > 1000:
                unit_name = 'M'
                slice_floor /= 1000.0

            if slice_floor > 1000:
                unit_name = 'G'
                slice_floor /= 1000.0

            if slice_floor > 1000:
                unit_name = 'T'
                slice_floor /= 1000.0

            if slice_floor > 1000:
                unit_name = 'P'
                slice_floor /= 1000.0

            # Congratulations on having these on one filesystem and serially
            # counting all of the files within your lifetime.
            if slice_floor > 1000:
                unit_name = 'E'
                slice_floor /= 1000.0

            # We cast the slice-floor as a strign or else Python prints it as
            # scientific notation.
            slice_floor_phrase = '{}{}'.format(str(round(slice_floor, 2)), unit_name)

            tally_phrase = '*' * int(float(tally) / float(total_count) * 100.0)
            f.write(("{:>8} {:" + str(count_width) + "} {}\n").format(slice_floor_phrase, tally, tally_phrase))
