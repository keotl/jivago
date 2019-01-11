import unittest

from jivago.wsgi.routing.routing_rule import RoutingRule


class RoutingRuleTest(unittest.TestCase):

    def test_matchingPrefixRootPrefix(self):
        rule = RoutingRule("/", None)

        self.assertTrue(rule.matches("/foo"))
        self.assertTrue(rule.matches("/"))

    def test_matchingPrefix(self):
        rule = RoutingRule("/users", None)

        self.assertTrue(rule.matches("/users"))
        self.assertTrue(rule.matches("/users/foo/bar/delete"))
        self.assertFalse(rule.matches("/admin"))

    def test_givenPathWhichDoesNotMatchRule_whenGettingRouteRegistrations_thenReturnEmptyList(self):
        rule = RoutingRule("/users", None)

        routes = rule.get_route_registrations("/foobar")

        self.assertEqual(0, len(routes))
