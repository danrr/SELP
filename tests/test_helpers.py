from app.helpers import parse_search_query, build_query_string
from tests.base_test import BaseTest


class TestHelpers(BaseTest):
    def test_parse_search_query(self):
        self.assertEquals(parse_search_query(""), ("", None, None))
        self.assertEquals(parse_search_query("cheese"), ("cheese", None, None))
        self.assertEquals(parse_search_query("cheese   "), ("cheese", None, None))
        self.assertEquals(parse_search_query("cheese  tag:curry "), ("cheese", None, "curry"))
        self.assertEquals(parse_search_query("cheese tag:curry bay leaves"), ("cheese  bay leaves", None, "curry"))
        self.assertEquals(parse_search_query("cheese tag:curry tag:blood"), ("cheese", None, "curry"))
        self.assertEquals(parse_search_query("cheese difficulty:hard"), ("cheese", "hard", None))
        self.assertEquals(parse_search_query("cheese difficulty:har"), ("cheese difficulty:har", None, None))
        self.assertEquals(parse_search_query("cheese difficulty:hard tag:curry"), ("cheese", "hard", "curry"))

    def test_build_query_string(self):
        self.assertEquals(build_query_string(""), "")
        self.assertEquals(build_query_string("cheese"),
                          "cheese")
        self.assertEquals(build_query_string("cheese", tag="curry"),
                          "cheese tag:curry")
        self.assertEquals(build_query_string("cheese", difficulty="hard"),
                          "cheese difficulty:hard")
        self.assertEquals(build_query_string("cheese", difficulty="hard", tag="curry"),
                          "cheese tag:curry difficulty:hard")