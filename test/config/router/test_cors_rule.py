import unittest

from jivago.config.router.cors_rule import CorsRule


class CorsRuleTest(unittest.TestCase):

    def setUp(self):
        self.rule = CorsRule("/", {})

    def test_givenRootPathRule_whenMatching_thenRuleMatchesAnyRequest(self):
        self.assertTrue(self.rule.matches("/"))
        self.assertTrue(self.rule.matches("/foo/bar"))

    def test_whenComparingCorsRules_thenLongerPathRulesTakePrecedenceOverShorterOnes(self):
        self.longer_rule = CorsRule("/foobar", {})

        takes_precedence = self.longer_rule.takes_precedence_over(self.rule)

        self.assertTrue(takes_precedence)

    def test_givenSameLengthRule_whenComparingCorsRules_thenPriorityIsGivenToMostRecentRule(self):
        takes_precedence = self.rule.takes_precedence_over(self.rule)

        self.assertTrue(takes_precedence)
