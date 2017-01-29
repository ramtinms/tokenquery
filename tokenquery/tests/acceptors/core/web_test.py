import unittest
from tokenquery.acceptors.web import web_is_url
from tokenquery.acceptors.web import web_is_email


class TestWebCoreAcceptorsClass(unittest.TestCase):

    def test_web_methods(self):
        self.assertEqual(web_is_url('http://test.com'), True)
        self.assertEqual(web_is_url('localhost'), True)
        self.assertEqual(web_is_email('mailto:ramtin@yahoo.com'), True)
        self.assertEqual(web_is_email('ramtin@yahoo.com'), True)
        self.assertEqual(web_is_email('ramtin@yahoo.co.us'), True)
        self.assertEqual(web_is_email('yahoo.co.us'), False)

if __name__ == '__main__':
    unittest.main()
