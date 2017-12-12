import unittest

from main import fabric_helper


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        fab = fabric_helper.FabricHelper()
        uname_return = fab.capture()
        print(uname_return)
        #self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
