import pytest
from analysis.data_detectors.pattern_manager import PatternManager
import re

@pytest.fixture
def pattern_manager():
    pm = PatternManager()
    pm.patterns = {}  
    return pm

def test_pattern_loading(pattern_manager):
    test_pattern = {
        "test_pattern": {
            "regex": r"\d{3}-\d{2}-\d{4}",
            "confidence": 0.9,
            "context": ["ssn", "social"]
        }
    }
    pattern_manager.patterns = test_pattern
    pattern_manager._compile_patterns()
    
    assert "test_pattern" in pattern_manager.compiled
    assert isinstance(pattern_manager.compiled["test_pattern"]["pattern"], re.Pattern)

def test_custom_pattern_validation(pattern_manager, tmp_path):
    yaml_content = """
    - name: "test_rule"
      regex: "[A-Z]{5}"
      confidence: 0.8
      context: ["test"]
    """
    test_file = tmp_path / "test_rules.yaml"
    test_file.write_text(yaml_content)
    
    pattern_manager.load_custom_patterns(str(test_file))
    assert "test_rule" in pattern_manager.patterns

def test_invalid_pattern_rejection(pattern_manager, tmp_path):
    yaml_content = """
    - name: "bad_rule"
      regex: "[invalid(regex"
      confidence: 0.8
      context: ["test"]
    """
    test_file = tmp_path / "invalid_rules.yaml"
    test_file.write_text(yaml_content)
    
    with pytest.raises(ValueError):
        pattern_manager.load_custom_patterns(str(test_file))

def test_context_weighting(pattern_manager):
    pattern_manager.patterns = {
        "test": {"context": ["login", "auth"], "regex": "", "confidence": 0.9}
    }
    weights = pattern_manager.get_context_weights("Login page authentication")
    assert weights["test"] == 2
