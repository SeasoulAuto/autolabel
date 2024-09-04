#!/usr/bin/env python

# Copyright 2024 wheelos <daohu527@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import csv
import glob
import re
from pathlib import Path

from autolabel.source.source import SourceFactory


class IterSource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass


class DirSource(IterSource):
    """
    use SourceFactory.create iter create each object in
    path (can be a path, a file)
    """

    def __init__(self, source_input):
        self.source_input = source_input
        self.path = Path(self.source_input.input)

    def __iter__(self):
        for p in self.path.iterdir():
            yield SourceFactory.create(p)


class CSVSource(IterSource):
    def __init__(self, source_input):
        self.source_input = source_input
        self.file_path = Path(self.source_input.input)

    def __iter__(self):
        with open(self.file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yield SourceFactory.create(row)


class GlobSource(IterSource):
    def __init__(self, source_input):
        self.source_input = source_input
        self.pattern = self._extract_glob_pattern(self.source_input.input)

    def _extract_glob_pattern(self, glob_string):
        pattern = r'^glob\(([^)]+)\)$'
        match = re.search(pattern, glob_string)
        if match:
            return match.group(1)
        else:
            return None

    def __iter__(self):
        for file in glob.glob(self.pattern):
            yield SourceFactory.create(file)
