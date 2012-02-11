# Case Conductor is a Test Case Management system.
# Copyright (C) 2011-12 Mozilla
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
from django.core.management.base import BaseCommand, CommandError

import json

from ...auth import admin
from ....testcases.models import TestCase, TestSuiteList, TestCaseList

"""
Exports this format::

    {
        "suites": [
            {
                "name": "fucci name",
                "description": "suite description"
            },
        ],
        "cases": [
            {
                "name": "case title",
                "description": "case description",
                "tags": ["tag1", "tag2", "tag3"],
                "suites": ["suite1 name", "suite2 name", "suite3 name"],
                "steps": [
                    {
                        "instruction": "action text",
                        "expected": "expected text"
                    },
                ]
            }
        ]
    }

"""

class Command(BaseCommand):
    args = '["Product Name"]'
    help = 'Exports the cases for the Product to JSON'


    def handle(self, *args, **options):

        try:
            cases = self.get_cases(args[0])
        except IOError as (errno, strerror):
            raise CommandError("I/O error({0}): {1}".format(errno, strerror))

        self.stdout.write(json.dumps(cases, indent=4))


    def get_cases(self, product_name):

        # gather all the suites for the Product

        # gather all the cases for the Product

        suites = []
        cases = []

        for suite in TestSuiteList.ours(auth=admin):
            if suite.product.name == product_name:
                suites.append({"name": suite.name,
                               "description": suite.description
                               })


        for one_case in TestCaseList.ours(auth=admin):
            if one_case.product.name == product_name:
                case = one_case.latestversion

                case_name = case.name
                if case.name.startswith("Test that "):
                    case_name = case_name[10:]

                # build this case
                resp_case = {
                    "name": case_name,
                    "description": case.description
                    }


                # build the tags for this case
                resp_case["tags"] = [x.name for x in case.tags]


                # build the tags for this case
                case_suites = TestSuiteList.ours(auth=admin).filter(
                    testCase=case.id)
                resp_case["suites"] = [x.name for x in case_suites]

                # build the steps for this case
                resp_case["steps"] = [{"instruction": step.instruction,
                                  "expected": step.expectedResult}
                         for step in case.steps]

                cases.append(resp_case)


        return {"suites": suites,
                "cases": cases,
                "casecount": len(cases)}

