"""
Unit Tests for SmartHire AI-Powered Hiring System
Core tests (10 test cases) for GenAI-only system
"""

import os
import unittest
from dotenv import load_dotenv

load_dotenv()

from state import CandidateState
from config import validate_config
from analyzers import AIAnalyzer, SemanticAnalyzer
from agents import ResumeParserAgent, ExperiencePredictorAgent, QuestionGeneratorAgent
from workflows import build_hiring_workflow
import pandas as pd


class TestSmartHire(unittest.TestCase):
    """Core tests for SmartHire system"""

    def setUp(self):
        """Setup test data"""
        self.sample_resume = """
        John Doe
        john@example.com
        5 years Python and JavaScript experience
        Skills: Python, JavaScript, SQL, React, Node.js
        Projects: E-commerce platform, Data analysis tool
        Education: B.S. Computer Science
        """

        self.job_description = """
        Software Engineer with 3-5 years experience.
        Required: Python, JavaScript, SQL
        """

    def test_1_api_keys_loaded(self):
        """Test that Gemini API keys are loaded from .env"""
        api_key = os.getenv("GEMINI_API_KEY_1")
        self.assertIsNotNone(api_key, "GEMINI_API_KEY_1 should be loaded")
        self.assertTrue(len(api_key) > 0, "API key should not be empty")

    def test_2_config_validation(self):
        """Test configuration validation"""
        try:
            validate_config()
            self.assertTrue(True, "Configuration should be valid")
        except ValueError as e:
            self.fail(f"Configuration validation failed: {e}")

    def test_3_job_descriptions_exists(self):
        """Test that job descriptions CSV file exists"""
        csv_path = "data/job_descriptions.csv"
        self.assertTrue(os.path.exists(csv_path), "job_descriptions.csv should exist")

        # Verify it's not empty
        df = pd.read_csv(csv_path)
        self.assertGreater(len(df), 0, "CSV should have job data")

    def test_4_state_creation(self):
        """Test CandidateState object creation"""
        state = CandidateState(
            resume_text=self.sample_resume,
            job_description=self.job_description,
            job_title="Software Engineer"
        )

        self.assertIsNotNone(state)
        self.assertEqual(state.resume_text, self.sample_resume)
        self.assertEqual(state.job_title, "Software Engineer")

    def test_5_state_cloning(self):
        """Test state cloning for parallel execution"""
        state = CandidateState(resume_text="Test", job_description="Test", job_title="Test")
        cloned = state.clone()

        # Should be different objects
        self.assertIsNot(cloned, state)

        # But have same values
        self.assertEqual(cloned.resume_text, state.resume_text)

    def test_6_ai_analyzer(self):
        """Test AI Analyzer initialization and functionality"""
        analyzer = AIAnalyzer("GEMINI_API_KEY_1")
        self.assertIsNotNone(analyzer)
        self.assertIsNotNone(analyzer.client)

    def test_7_semantic_analyzer(self):
        """Test Semantic Analyzer functionality"""
        analyzer = SemanticAnalyzer()

        # Test similarity calculation
        ref = "Python is a programming language"
        cand = "Python is a coding language"

        similarity = analyzer.calculate_similarity(ref, cand)
        self.assertGreater(similarity, 0.5, "Similar texts should have high similarity")

    def test_8_resume_parser_agent(self):
        """Test resume parsing agent"""
        agent = ResumeParserAgent()
        result = agent.analyze(self.sample_resume)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('skills', result, "Should extract skills")

    def test_9_experience_predictor_agent(self):
        """Test experience level prediction agent"""
        agent = ExperiencePredictorAgent()

        resume_features = {
            'total_experience_years': 5.0,
            'skills': ['Python', 'JavaScript', 'SQL'],
            'projects': ['Project1', 'Project2'],
            'certifications': [],
            'leadership_experience': 0,
            'has_research_work': 0
        }

        result = agent.analyze(resume_features)
        self.assertIn('experience_level', result)
        valid_levels = ['Junior', 'Mid-Level', 'Senior']
        self.assertIn(result['experience_level'], valid_levels)

    def test_10_workflow_creation(self):
        """Test hiring workflow creation"""
        workflow = build_hiring_workflow()

        self.assertIsNotNone(workflow)
        self.assertIsNotNone(workflow.stages)
        self.assertGreater(len(workflow.stages), 0, "Workflow should have stages")


def run_tests():
    """Run all tests and display summary"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSmartHire)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests:    {result.testsRun}")
    print(f"Passed:         {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed:         {len(result.failures)}")
    print(f"Errors:         {len(result.errors)}")
    print("=" * 60)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    exit_code = run_tests()
    sys.exit(exit_code)
