# -*- coding: utf-8 -*-
import logging
import os
import sys
import importlib
import unittest as UnitTest

LOGGER = logging.getLogger(__name__)


class SequentialTestLoader(UnitTest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        testcase_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        testcase_names.sort(key=testcase_methods.index)
        return testcase_names


def load_module(filename):
    if not os.path.isfile(filename):
        raise ImportError('file not founded')

    module_dir, module_file = os.path.split(os.path.abspath(filename))
    module_name, module_ext = os.path.splitext(module_file)

    if module_dir not in sys.path:
        sys.path.append(module_dir)

    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        LOGGER.exception(e)
        raise
    
    return module

def unittest(filename):
    module = load_module(filename)
    suite = SequentialTestLoader().loadTestsFromModule(module)
    result = UnitTest.TextTestRunner().run(suite)

    return  result