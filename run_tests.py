#!/usr/bin/env python2
from unittest import makeSuite, TextTestRunner, TestSuite
from sys import exit
from tests.test_cases import CreateTopic, TestBBCode

if __name__ == '__main__':
    suite = TestSuite((
        makeSuite(CreateTopic),
        makeSuite(TestBBCode),
    ))
    result = TextTestRunner().run(suite)
    exit(not result.wasSuccessful())