#
# Copyright (c) 2019 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os.path

from packagedcode import build
from scancode.cli_test_utils import check_json_scan
from scancode.cli_test_utils import run_scan_click
from scancode.resource import Codebase
from packages_test_utils import PackageTester


class TestBuild(PackageTester):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_end2end_scan_can_detect_bazel(self):
        test_file = self.get_test_loc('build/bazel')
        expected_file = self.get_test_loc('build/bazel-expected.json')
        result_file = self.get_temp_file('results.json')
        run_scan_click(['--package', test_file, '--json-pp', result_file])
        check_json_scan(expected_file, result_file, regen=False)

    def test_end2end_scan_can_detect_buck(self):
        test_file = self.get_test_loc('build/buck')
        expected_file = self.get_test_loc('build/buck-expected.json')
        result_file = self.get_temp_file('results.json')
        run_scan_click(['--package', test_file, '--json-pp', result_file])
        check_json_scan(expected_file, result_file, regen=False)

    def test_buck_parse(self):
        test_file = self.get_test_loc('build/buck-parse/BUCK')
        result = build.buck_parse(test_file)
        expected = build.BuckPackage(
            name='app'
        )
        assert expected == result

    def test_buck_parse_with_license(self):
        test_file = self.get_test_loc('build/buck-parse/license/BUCK')
        result = build.buck_parse(test_file)
        expected = build.BuckPackage(
            name='app',
            declared_license=['LICENSE'],
            license_expression='apache-2.0'
        )
        assert expected == result

    def test_build_get_package_resources(self):
        test_loc = self.get_test_loc('build/get_package_resources')
        codebase = Codebase(test_loc)
        root = codebase.root
        expected = [
            'get_package_resources',
            'get_package_resources/BUCK',
            'get_package_resources/file1',
        ]
        results = [r.path for r in build.BaseBuildManifestPackage.get_package_resources(root, codebase)]
        assert expected == results
