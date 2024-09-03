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
from PIL.Image import Image


class FileSource(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def data(self):
      """return source data
      """

class ImageFileSource(FileSource):
    def __init__(self, source_input):
        self.source_input = source_input

    @property
    def data(self):
        file_path = self.source_input.input
        return Image.open(file_path)

class PCDFileSource(FileSource):
    def __init__(self, source_input):
        self.source_input = source_input

    @property
    def data(self):
        raise NotImplementedError("Not support pcd for now!")
