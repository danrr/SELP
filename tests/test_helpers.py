from app.helpers import parse_search_query
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