# Case Conductor is a Test Case Management system.
# Copyright (C) 2011 uTest Inc.
# 
# This file is part of Case Conductor.
# 
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
"""
Tests for global Django caching config.

"""
from unittest2 import TestCase



class MakeKeyTest(TestCase):
    @property
    def func(self):
        from ccui.core.cacheconfig import make_key
        return make_key


    def test_make_key(self):
        self.assertEqual(
            self.func("key", "prefix", 4),
            "131ad3a66fb91dd513d364c8a7a35eacb9084757")
