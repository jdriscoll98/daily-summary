import unittest


class TestExample(unittest.TestCase):

    def test_passing(self):
        self.assertEqual(1, 1)

    def test_failing(self):
        self.assertEqual(1, 0)
