#!/usr/bin/env python3
"""
ONTOS Validator
Purpose: Checks Ontos statements for contradictions, vagueness, or invalid syntax.
Rules:
  1. Non-Contradiction: No statement can imply its own negation.
  2. Specificity: All terms must be unambiguously defined.
  3. No Raw Self-Reference: Avoids paradoxes like the liar's paradox.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class OntosStatement:
    """Represents a single Ontos statement."""
    raw: str
    line_number: int
    variables: List[str] = field(default_factory=list)
    is_comment: bool = False
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of validating a file or set of statements."""
    is_valid: bool
    statements: List[OntosStatement]
    errors: List[str]
    warnings: List[str]


class OntosValidator:
    """Validates Ontos statements for contradictions, vagueness, and syntax errors."""

    def __init__(self):
        self.variables: Dict[str, List[str]] = {}  # Maps variable names to their definitions
        self.allowed_symbols = {
            "λ_": "Variable prefix",
            "→": "Implication",
            "≡": "Equivalence",
            "IF": "Conditional start",
            "THEN": "Conditional then",
            "ELSE": "Conditional else",
            "END_IF": "Conditional end",
            "--": "Comment",
        }
        self.forbidden_patterns = [
            (r"λ_Statement\.value\s*=\s*[\"']This statement is false[\"']", "Liar's paradox detected"),
            (r"λ_.*\.value\s*=\s*[\"']This .* is false[\"']", "Self-contradictory statement"),
        ]
        self.vague_terms = [
            "maybe", "perhaps", "sort of", "kind of", "ish", "vague", "ambiguous",
            "somewhat", "rather", "quite", "pretty", "usually", "often"
        ]

    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate an Ontos file."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return self.validate_statements(lines)

    def validate_statements(self, lines: List[str]) -> ValidationResult:
        """Validate a list of Ontos statements."""
        statements: List[OntosStatement] = []
        errors: List[str] = []
        warnings: List[str] = []
        is_valid = True

        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("--"):
                statements.append(OntosStatement(raw=line, line_number=i, is_comment=True))
                continue

            stmt = OntosStatement(raw=line, line_number=i)
            self._extract_variables(stmt)
            self._check_syntax(stmt)
            self._check_contradictions(stmt, statements)
            self._check_vagueness(stmt)
            self._check_self_reference(stmt)

            if stmt.errors:
                is_valid = False
                errors.extend([f"Line {stmt.line_number}: {err}" for err in stmt.errors])

            statements.append(stmt)

        return ValidationResult(
            is_valid=is_valid,
            statements=statements,
            errors=errors,
            warnings=warnings
        )

    def _extract_variables(self, stmt: OntosStatement) -> None:
        """Extract variables from a statement (e.g., λ_Agent, λ_Door)."""
        pattern = r"λ_\w+"
        matches = re.findall(pattern, stmt.raw)
        stmt.variables = list(set(matches))  # Remove duplicates

    def _check_syntax(self, stmt: OntosStatement) -> None:
        """Check for basic syntax errors."""
        # Check for unclosed conditionals
        if "IF" in stmt.raw and "END_IF" not in stmt.raw:
            # This is a simplistic check; a full parser would track state across lines
            pass

        # Check for invalid symbols
        for char in stmt.raw:
            if char not in self.allowed_symbols and not char.isalnum() and char not in {" ", "=", ".", "(", ")", "\"", "'", ",", "+", "-", "*", "/"}:
                stmt.errors.append(f"Invalid symbol: '{char}'")

    def _check_contradictions(self, stmt: OntosStatement, previous_statements: List[OntosStatement]) -> None:
        """Check for contradictions with previous statements."""
        for prev_stmt in previous_statements:
            if prev_stmt.is_comment:
                continue
            # Example: λ_Door.state = "open" vs λ_Door.state = "closed"
            for var in stmt.variables:
                if var in prev_stmt.variables:
                    # Extract assignments for this variable
                    current_val = self._extract_assignment(stmt.raw, var)
                    prev_val = self._extract_assignment(prev_stmt.raw, var)
                    if current_val and prev_val and current_val != prev_val:
                        stmt.errors.append(
                            f"Contradiction: {var} is assigned '{current_val}' here but was '{prev_val}' on line {prev_stmt.line_number}"
                        )

    def _extract_assignment(self, stmt: str, var: str) -> Optional[str]:
        """Extract the value assigned to a variable in a statement."""
        pattern = rf"{re.escape(var)}\.(\w+)\s*=\s*[\"']?([^\"'\s;]+)[\"']?"
        match = re.search(pattern, stmt)
        if match:
            return match.group(2)
        return None

    def _check_vagueness(self, stmt: OntosStatement) -> None:
        """Check for vague terms in the statement."""
        lower_raw = stmt.raw.lower()
        for term in self.vague_terms:
            if term in lower_raw:
                stmt.errors.append(f"Vague term detected: '{term}'")

    def _check_self_reference(self, stmt: OntosStatement) -> None:
        """Check for raw self-reference (e.g., liar's paradox)."""
        for pattern, error_msg in self.forbidden_patterns:
            if re.search(pattern, stmt.raw, re.IGNORECASE):
                stmt.errors.append(error_msg)


def validate_file(file_path: str) -> ValidationResult:
    """Validate an Ontos file and print the results."""
    validator = OntosValidator()
    result = validator.validate_file(file_path)

    if result.is_valid:
        print(f"✅ {file_path} is valid!")
    else:
        print(f"❌ {file_path} has errors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print(f"⚠️  Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python validator.py <ontos_file>")
        sys.exit(1)
    validate_file(sys.argv[1])
