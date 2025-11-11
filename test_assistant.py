"""
Test suite for Data Visualization Assistant
Run with: python test_assistant.py
"""

from services.visualization_assistant import VisualizationAssistant
import json


def test_intent_detection():
    """Test intent detection for various data goals."""
    print("=" * 80)
    print("TEST 1: Intent Detection")
    print("=" * 80)
    
    assistant = VisualizationAssistant()
    
    test_cases = [
        ("Compare monthly sales across regions", "comparison"),
        ("Show growth trend of revenue over 5 years", "trend"),
        ("Display distribution of customer ages", "distribution"),
        ("Show market share percentages by product", "proportion"),
        ("Analyze relationship between price and demand", "relationship"),
        ("Compare Q1 vs Q2 performance", "comparison"),
        ("Track changes over time", "trend"),
        ("How many customers in each age bracket", "distribution"),
        ("What percentage of total revenue", "proportion"),
        ("Correlation between temperature and sales", "relationship"),
    ]
    
    passed = 0
    failed = 0
    
    for goal, expected_intent in test_cases:
        detected = assistant.detect_intent(goal)
        status = "✓ PASS" if detected == expected_intent else "✗ FAIL"
        
        if detected == expected_intent:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} | Goal: '{goal}'")
        print(f"       Expected: {expected_intent}, Got: {detected}")
        print()
    
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("\n")
    return passed, failed


def test_recommendations_structure():
    """Test that recommendations have the correct structure."""
    print("=" * 80)
    print("TEST 2: Recommendations Structure")
    print("=" * 80)
    
    assistant = VisualizationAssistant()
    
    test_goals = [
        "Compare sales across regions",
        "Show revenue trend",
        "Display age distribution",
        "Show market share",
        "Analyze price vs demand"
    ]
    
    all_valid = True
    
    for goal in test_goals:
        result = assistant.analyze_data_goal(goal)
        
        # Check structure
        has_intent = 'intent' in result
        has_recommendations = 'recommendations' in result
        has_three_recs = len(result.get('recommendations', [])) == 3
        
        valid = has_intent and has_recommendations and has_three_recs
        
        if valid:
            # Check each recommendation structure
            for rec in result['recommendations']:
                if not all(key in rec for key in ['name', 'rationale', 'constraints']):
                    valid = False
                    break
                if not all(key in rec['constraints'] for key in ['color', 'axis', 'label']):
                    valid = False
                    break
        
        status = "✓ PASS" if valid else "✗ FAIL"
        all_valid = all_valid and valid
        
        print(f"{status} | Goal: '{goal}'")
        print(f"       Intent: {result.get('intent', 'N/A')}")
        print(f"       Recommendations: {len(result.get('recommendations', []))}")
        print()
    
    print(f"Overall: {'All tests passed!' if all_valid else 'Some tests failed!'}")
    print("\n")
    return all_valid


def test_json_output():
    """Test JSON serialization."""
    print("=" * 80)
    print("TEST 3: JSON Output")
    print("=" * 80)
    
    assistant = VisualizationAssistant()
    
    try:
        result = assistant.analyze_data_goal("Compare monthly sales")
        json_str = json.dumps(result, indent=2)
        
        # Try to parse it back
        parsed = json.loads(json_str)
        
        print("✓ PASS | JSON serialization successful")
        print(f"JSON output sample (first 500 chars):")
        print(json_str[:500] + "...")
        print()
        return True
    except Exception as e:
        print(f"✗ FAIL | JSON serialization failed: {str(e)}")
        print()
        return False


def test_empty_input():
    """Test handling of empty or invalid input."""
    print("=" * 80)
    print("TEST 4: Empty/Invalid Input Handling")
    print("=" * 80)
    
    assistant = VisualizationAssistant()
    
    test_cases = [
        "",
        "   ",
        None
    ]
    
    all_passed = True
    
    for test_input in test_cases:
        try:
            result = assistant.analyze_data_goal(test_input or "")
            
            # Should return fallback recommendations
            has_fallback = (
                result.get('intent') == 'comparison' and
                len(result.get('recommendations', [])) == 3
            )
            
            status = "✓ PASS" if has_fallback else "✗ FAIL"
            all_passed = all_passed and has_fallback
            
            print(f"{status} | Input: {repr(test_input)}")
            print(f"       Returns fallback recommendations: {has_fallback}")
            
        except Exception as e:
            print(f"✗ FAIL | Input: {repr(test_input)}")
            print(f"       Exception: {str(e)}")
            all_passed = False
        
        print()
    
    print(f"Overall: {'All tests passed!' if all_passed else 'Some tests failed!'}")
    print("\n")
    return all_passed


def test_all_intents_covered():
    """Test that all intents have recommendations."""
    print("=" * 80)
    print("TEST 5: All Intents Have Recommendations")
    print("=" * 80)
    
    assistant = VisualizationAssistant()
    
    intents = ['comparison', 'trend', 'distribution', 'proportion', 'relationship']
    
    all_covered = True
    
    for intent in intents:
        recommendations = assistant.get_recommendations(intent)
        has_three = len(recommendations) == 3
        
        status = "✓ PASS" if has_three else "✗ FAIL"
        all_covered = all_covered and has_three
        
        print(f"{status} | Intent: {intent}")
        print(f"       Recommendations count: {len(recommendations)}")
        if recommendations:
            print(f"       Charts: {', '.join(r['name'] for r in recommendations)}")
        print()
    
    print(f"Overall: {'All intents covered!' if all_covered else 'Some intents missing recommendations!'}")
    print("\n")
    return all_covered


def run_all_tests():
    """Run all tests and display summary."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "DATA VISUALIZATION ASSISTANT - TEST SUITE" + " " * 17 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    results = []
    
    # Run tests
    passed, failed = test_intent_detection()
    results.append(("Intent Detection", passed > 0 and failed == 0))
    
    results.append(("Recommendations Structure", test_recommendations_structure()))
    results.append(("JSON Output", test_json_output()))
    results.append(("Empty Input Handling", test_empty_input()))
    results.append(("All Intents Covered", test_all_intents_covered()))
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status} | {test_name}")
    
    print()
    print(f"Total: {total_passed}/{total_tests} test suites passed")
    print()
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! 🎉")
    else:
        print("⚠️ Some tests failed. Please review the output above.")
    
    print("\n")


if __name__ == "__main__":
    run_all_tests()
