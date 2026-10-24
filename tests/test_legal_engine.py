"""
Test Suite for CivicReach AI (India Edition)
Verifies search accuracy, multilingual translations, NALSA screener, and notice decryptor.
"""

import unittest
from civicreach.legal_engine import LegalEngine
from civicreach.nalsa_screener import NALSAScreener
from civicreach.i18n import SUPPORTED_LANGUAGES, get_text

class TestCivicReach(unittest.TestCase):
    def setUp(self):
        self.engine = LegalEngine()

    def test_supported_languages(self):
        self.assertIn("en", SUPPORTED_LANGUAGES)
        self.assertIn("hi", SUPPORTED_LANGUAGES)
        self.assertIn("bn", SUPPORTED_LANGUAGES)
        self.assertIn("mr", SUPPORTED_LANGUAGES)
        self.assertIn("ta", SUPPORTED_LANGUAGES)

    def test_search_bns_cheating(self):
        results = self.engine.search("cheating 420", lang="hi")
        self.assertGreater(len(results), 0)
        top = results[0]
        self.assertIn("318", top["section"])
        self.assertTrue(top["free_legal_aid_applicable"])

    def test_search_land_dispute(self):
        results = self.engine.search("land dispute", lang="ta")
        self.assertGreater(len(results), 0)
        found = any("168" in r["section"] or "BNSS" in r["act"] for r in results)
        self.assertTrue(found)

    def test_nalsa_screener_woman(self):
        data = {"is_woman_or_child": True, "annual_income": 500000}
        res = NALSAScreener.evaluate(data, lang="en")
        self.assertTrue(res["eligible"])
        self.assertTrue(any("Section 12(c)" in c for c in res["clauses"]))

    def test_nalsa_screener_low_income(self):
        data = {"annual_income": 120000, "state": "bihar"}
        res = NALSAScreener.evaluate(data, lang="hi")
        self.assertTrue(res["eligible"])

    def test_decrypt_sdm_notice(self):
        sample = "न्यायालय अनुमंडल दंडाधिकारी धारा 145 CrPC मौजा रामपुर भूमि विवाद"
        res = self.engine.decrypt_notice(sample, lang="hi")
        self.assertIn("168", res["detected_type"])
        self.assertTrue(res["free_lawyer_available"])

    def test_decrypt_hospital_pmjay(self):
        sample = "Hospital admission under PM-JAY denied advance deposit 45000"
        res = self.engine.decrypt_notice(sample, lang="en")
        self.assertIn("PM-JAY", res["detected_type"])
        self.assertTrue(res["free_lawyer_available"])

if __name__ == "__main__":
    unittest.main()
