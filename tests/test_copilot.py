import unittest
from src.copilot import analyze_inquiry


class TestInquiryCopilot(unittest.TestCase):
    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            analyze_inquiry("   ")

    def test_ai_service_detected(self):
        result = analyze_inquiry(
            "We need an AI chatbot for customer questions within four weeks. "
            "It should use our existing FAQ and product catalog."
        )
        self.assertEqual(result["service_category"], "AI Automation")
        self.assertTrue(result["timeline"])
        self.assertTrue(result["follow_up_questions"])

    def test_cloud_service_detected(self):
        result = analyze_inquiry(
            "We need AWS cloud migration for our Python application and Docker deployment."
        )
        self.assertEqual(result["service_category"], "Cloud and DevOps")

    def test_human_review_for_unknown_category(self):
        result = analyze_inquiry(
            "We have a unique project request and would like to discuss possible options."
        )
        self.assertEqual(result["service_category"], "Needs Human Review")

    def test_draft_not_automatically_sent(self):
        result = analyze_inquiry("We need a website for our small business.")
        self.assertIn("Subject:", result["draft_response"])
        self.assertIn("not sent automatically", " ".join(result["limitations"]).lower())


if __name__ == "__main__":
    unittest.main()
