# Copyright (C) 2019 Cancer Care Associates

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version (the "AGPL-3.0+").

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License and the additional terms for more
# details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
# Affero General Public License. These additional terms are Sections 1, 5,
# 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
# where all references to the definition "License" are instead defined to
# mean the AGPL-3.0+.

# You should have received a copy of the Apache-2.0 along with this
# program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.

import numpy as np

from pymedphys_analysis.mocks.profiles import create_dummy_profile_function
from pymedphys_analysis.winstonlutz.profiles import penumbra_flip_diff


# pylint: disable=bad-whitespace,C1801

def test_profile_flip_diff():
    profile_centre = 1.7
    field_width = 10
    penumbra_width = 0.3

    dummy_profile = create_dummy_profile_function(
        profile_centre, field_width, penumbra_width)

    centre_tests = [0, 1, 1.6, 1.69, 1.699, 1.7, 1.701, 1.71, 1.8, 2, 3, 10]
    expected_smallest_index = centre_tests.index(profile_centre)

    flip_diffs = [
        penumbra_flip_diff(dummy_profile, centre_test, penumbra_width,
                           field_width)
        for centre_test in centre_tests
    ]

    assert np.argmin(flip_diffs) == expected_smallest_index
