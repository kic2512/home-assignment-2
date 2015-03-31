#!/usr/bin/env python2
from unittest import makeSuite, TextTestRunner, TestSuite
from sys import exit
from tests.test_cases import CreateMessage

if __name__ == '__main__':
    suite = TestSuite((
        makeSuite(CreateMessage),
    ))
    result = TextTestRunner().run(suite)
    exit(not result.wasSuccessful())