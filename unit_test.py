#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

# import xenoslib
# import xenoslib.dev
# import xenoslib.onedrive
from dockerfile_generator import Dockerfile


class UnitTest(unittest.TestCase):
    def setUp(self):
        """run before each test"""
        print('*' * 79)

    def tearDown(self):
        """run after each test"""
        print('*' * 79)

    @classmethod
    def setUpClass(cls):
        """run before all tests"""
        print('=' * 79)

    @classmethod
    def tearDownClass(cls):
        """run after all tests"""
        print('=' * 79)

    def test_1(self):
        df = Dockerfile('python:3.8.13-alpine3.15')
        self.assertEqual(df.get_deps('cffi'), 'build-base libffi-dev')
        df = Dockerfile('python:3.11-rc-slim')
        self.assertEqual(df.get_deps('cffi'), 'build-essential libffi-dev')


if __name__ == '__main__':
    unittest.main()  # run all unit tests
