[![Build Status](https://travis-ci.org/dsoprea/pathhistogram.svg?branch=master)](https://travis-ci.org/dsoprea/pathhistogram)
[![Coverage Status](https://coveralls.io/repos/github/dsoprea/pathhistogram/badge.svg?branch=master)](https://coveralls.io/github/dsoprea/pathhistogram?branch=master)

# Overview

This is a tool that visualizes the distribution of file-sizes under a given directory (recursively) from the command-line.


# Install

Via Git:

```
$ git clone https://github.com/dsoprea/pathhistogram.git
$ sudo pip install .
```

Via PIP:

```
$ sudo pip install pathhistogram
```


# Example Usages

Simple histogram:

```
$ ph_files ~/development/go/src
(30896) files found.

    0.0B 30851 ***************************************************************************************************
   4.94M    28 
   9.88M     7 
  14.82M     2 
  19.76M     3 
   24.7M     1 
  29.64M     0 
  34.58M     1 
  39.52M     1 
  44.46M     0 
   49.4M     0 
  54.34M     0 
  59.28M     0 
  64.22M     0 
  69.17M     0 
  74.11M     0 
  79.05M     1 
  83.99M     0 
  88.93M     0 
  93.87M     0 
  98.81M     0 
 103.75M     0 
 108.69M     0 
 113.63M     0 
 118.57M     0 
 123.51M     0 
 128.45M     0 
 133.39M     0 
 138.33M     0 
 143.27M     1 
```

Add size constraints:

```
$ ph_files ~/development/go/src --minimum-size 100000 --maximum-size 7000000
(777) files found.

    0.0B 412 *****************************************************
 235.77K 161 ********************
 471.53K  57 *******
  707.3K  39 *****
 943.06K  18 **
   1.18M  11 *
   1.41M   4 
   1.65M  12 *
   1.89M   6 
   2.12M  13 *
   2.36M   2 
   2.59M   5 
   2.83M   5 
   3.06M   1 
    3.3M   2 
   3.54M   1 
   3.77M   4 
   4.01M   1 
   4.24M   2 
   4.48M   2 
   4.72M   4 
   4.95M   3 
   5.19M   1 
   5.42M   5 
   5.66M   2 
   5.89M   1 
   6.13M   1 
   6.37M   0 
    6.6M   1 
   6.84M   1 
```

Add filename filtering:

```
$ ph_files ~/development/go/src --filter '*.txt' --maximum-size 100000
(173) files found.

    0.0B  58 *********************************
   1.79K  10 *****
   3.58K   7 ****
   5.37K   1 
   7.16K  24 *************
   8.95K  10 *****
  10.74K   9 *****
  12.54K   5 **
  14.33K  11 ******
  16.12K   3 *
  17.91K   6 ***
   19.7K   0 
  21.49K   9 *****
  23.28K   0 
  25.07K   9 *****
  26.86K   3 *
  28.65K   0 
  30.44K   2 *
  32.23K   3 *
  34.02K   0 
  35.82K   0 
  37.61K   0 
   39.4K   0 
  41.19K   0 
  42.98K   0 
  44.77K   0 
  46.56K   0 
  48.35K   0 
  50.14K   0 
  51.93K   3 *
```

Dump binned files:

```
$ ph_files ~/development/go/src --minimum-size 100000 --maximum-size 7000000 --dump-filepath -
(777) files found.

    0.0B 412 *****************************************************
 235.77K 161 ********************
 471.53K  57 *******
  707.3K  39 *****
 943.06K  18 **
   1.18M  11 *
   1.41M   4 
   1.65M  12 *
   1.89M   6 
   2.12M  13 *
   2.36M   2 
   2.59M   5 
   2.83M   5 
   3.06M   1 
    3.3M   2 
   3.54M   1 
   3.77M   4 
   4.01M   1 
   4.24M   2 
   4.48M   2 
   4.72M   4 
   4.95M   3 
   5.19M   1 
   5.42M   5 
   5.66M   2 
   5.89M   1 
   6.13M   1 
   6.37M   0 
    6.6M   1 
   6.84M   1 

Binned Files
============

n 30
total_count 777
largest_size 6837217
slice_size 235766.10344827586

# 0
cloud.google.com/go/cmd/go-cloud-debug-agent/internal/debug/elf/elf.go
cloud.google.com/go/.git/index
honnef.co/go/js/dom/.git/objects/pack/pack-734fd8e636f78b113acf659b99bf294b70980608.pack
istio.io/gogo-genproto/.git/objects/pack/pack-41660cfadfe8eaf02a68a4131f83f74b493f448b.pack
istio.io/gogo-genproto/opencensus/proto/trace/v1/trace.pb.go
...
go.opencensus.io/.git/objects/pack/pack-571baecd3cb823ae1c93f689a64acde6a00a747c.idx

# 1
sourcegraph.com/sourcegraph/go-git/.git/objects/pack/pack-00486269f82abf90affb26f40452e24b695ab253.pack
golang.org/x/text/secure/precis/tables10.0.0.go
golang.org/x/text/secure/precis/tables9.0.0.go
golang.org/x/text/unicode/norm/tables10.0.0.go
golang.org/x/text/unicode/norm/tables9.0.0.go
...
github.com/gopherjs/gopherjs/.git/objects/pack/pack-82229e71cbaa7ec424a00dcaa608931814f72288.idx

# 2
cloud.google.com/go/.git/objects/pack/pack-2158290a8566a62df206245295606e5a10b0d26e.idx
golang.org/x/text/encoding/charmap/tables.go
golang.org/x/text/encoding/korean/tables.go
golang.org/x/crypto/sha3/testdata/keccakKats.json.deflate
golang.org/x/perf/vendor/github.com/mattn/go-sqlite3/sqlite3-binding.h
...
```


# Testing

```
$ ./test.sh
```
