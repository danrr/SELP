#!env/bin/python
import unittest

from app import app, db


class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config.from_object('tests.test_config')
        app.login_manager.init_app(app)
        self.app = app.test_client()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assert_contains_string(self, base, string):
        self.assertTrue(base.find(string) > -1, msg="{string} not found in {base}".format(string=string, base=base))

    def assert_does_not_contain_string(self, base, string):
        self.assertFalse(base.find(string) > -1, msg="{string} found in {base}".format(string=string, base=base))

if __name__ == '__main__':
    unittest.main()