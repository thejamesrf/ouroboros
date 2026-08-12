#!/usr/bin/env python3
"""
Tests for the ONTOS Validator
"""

import unittest
from ontos-language.ONTOSplayground.tools.validator import OntosValidator, OntosStatement, ValidationResult


class TestOntosValidator(unittest.TestCase):
    """Test cases for the OntosValidator class."""

    def setUp(self):
        self.validator = OntosValidator()

    def test_validate_valid_statement(self):
        """Test validating a simple valid statement."""
        lines = ["λ_Agent.act(open_door) → λ_Door.state = \"open\""]
        result = self.validator.validate_statements(lines)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_validate_comment(self):
        """Test that comments are ignored."""
        lines = ["-- This is a comment", "λ_Agent.act(open_door)"]
        result = self.validator.validate_statements(lines)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_validate_liars_paradox(self):
        """Test detecting the liar's paradox."""
        lines = ['λ_Statement.value = "This statement is false"']
        result = self.validator.validate_statements(lines)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Liar's paradox" in err for err in result.errors))

    def test_validate_vague_term(self):
        """Test detecting vague terms."""
        lines = ['λ_Door.state = "sort of open"']
        result = self.validator.validate_statements(lines)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Vague term" in err for err in result.errors))

    def test_validate_contradiction(self):
        """Test detecting contradictions between statements."""
        lines = [
            'λ_Door.state = "open"',
            'λ_Door.state = "closed"'
        ]
        result = self.validator.validate_statements(lines)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Contradiction" in err for err in result.errors))

    def test_validate_multiple_statements(self):
        """Test validating multiple statements."""
        lines = [
            "λ_Agent.name = \"Alpha\"",
            "λ_Agent.act(open_door) → λ_Door.state = \"open\"",
            "-- This is a comment",
            "λ_Sensor.detect(\"intruder\") → λ_Alarm.trigger()"
        ]
        result = self.validator.validate_statements(lines)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_extract_variables(self):
        """Test extracting variables from a statement."""
        stmt = OntosStatement(raw="λ_Agent.act(open_door) → λ_Door.state = \"open\"", line_number=1)
        self.validator._extract_variables(stmt)
        self.assertIn("λ_Agent", stmt.variables)
        self.assertIn("λ_Door", stmt.variables)

    def test_check_syntax_invalid_symbol(self):
        """Test detecting invalid symbols."""
        lines = ["λ_Agent.act(open_door) # invalid symbol"]
        result = self.validator.validate_statements(lines)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("Invalid symbol" in err for err in result.errors))


if __name__ == "__main__":
    unittest.main()
