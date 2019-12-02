import unittest

from bin.jumper_expect import jumper_login


class MyTestCase(unittest.TestCase):
    def test_login(self, ):
        child = jumper_login()
        self.assertEqual(child, False)


if __name__ == '__main__':

    unittest.main()
