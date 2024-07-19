# """
# Write a function which detects if entered string is http/https domain name with optional slash at the and
# Restriction: use re module
# Note that address may have several domain levels
#     >>> is_http_domain('http://wikipedia.org')
#     True
#     >>> is_http_domain('https://ru.wikipedia.org/')
#     True
#     >>> is_http_domain('griddynamics.com')
#     False
# """
import re


def is_http_domain(domain: str) -> bool:
    pattern = r'^(http://|https://)[\w.-]+\.[a-z]{2,6}/?$'
    return bool(re.match(pattern, domain))


"""
write tests for is_http_domain function
"""

import unittest


class TestIsHttpDomain(unittest.TestCase):

        def test_is_http_domain(self):
            self.assertEqual(is_http_domain('http://wikipedia.org'), True)
            self.assertEqual(is_http_domain('https://ru.wikipedia.org/'), True)
            self.assertEqual(is_http_domain('griddynamics.com'), False)
            self.assertEqual(is_http_domain('http://www.griddynamics.com'), True)
            self.assertEqual(is_http_domain('https://www.griddynamics.com/'), True)
            self.assertEqual(is_http_domain('https://www.griddynamics.com'), True)
            self.assertEqual(is_http_domain('https://www.griddynamics.com/'), True)
            self.assertEqual(is_http_domain('https://www.griddynamics.com//'), False)


if __name__ == '__main__':
    unittest.main()