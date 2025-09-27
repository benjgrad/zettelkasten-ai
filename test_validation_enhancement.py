#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.diagram_generator import diagram_generator

def test_enhanced_validation():
    print("🧪 Running Enhanced MermaidJS Validation Tests")
    print("=" * 60)

    # Test 1: Valid MermaidJS should pass
    print("\n1. Testing valid MermaidJS...")
    valid_mermaid = """flowchart TD
    A["Person"] --> B["Organization"]
    style A fill:#FFE4B5
    style B fill:#B0E0E6"""

    result = diagram_generator.validate_mermaid_syntax(valid_mermaid)
    if not result["valid"]:
        print(f"❌ FAIL: Valid MermaidJS rejected - {result['errors']}")
        return False
    print(f"✅ Valid syntax correctly accepted")

    # Test 2: Missing flowchart declaration
    print("\n2. Testing missing flowchart declaration...")
    invalid_no_flowchart = """A["Person"] --> B["Organization"]
    style A fill:#FFE4B5"""

    result = diagram_generator.validate_mermaid_syntax(invalid_no_flowchart)
    if result["valid"] or "Missing 'flowchart' declaration at start" not in result["errors"]:
        print(f"❌ FAIL: Should detect missing flowchart declaration - {result}")
        return False
    print(f"✅ Missing flowchart declaration detected")

    # Test 3: Invalid flowchart direction
    print("\n3. Testing invalid flowchart direction...")
    invalid_direction = """flowchart XY
    A["Person"] --> B["Organization"]"""

    result = diagram_generator.validate_mermaid_syntax(invalid_direction)
    if not any("Unknown flowchart direction" in w for w in result["warnings"]):
        print(f"❌ FAIL: Should warn about invalid direction - {result}")
        return False
    print(f"✅ Invalid flowchart direction warning generated")

    # Test 4: Unbalanced brackets
    print("\n4. Testing unbalanced brackets...")
    unbalanced_brackets = """flowchart TD
    A["Unclosed quote]
    B["Valid"] --> C["Another"]"""

    result = diagram_generator.validate_mermaid_syntax(unbalanced_brackets)
    if result["valid"] or not any("Unbalanced" in e for e in result["errors"]):
        print(f"❌ FAIL: Should detect unbalanced brackets - {result}")
        return False
    print(f"✅ Unbalanced brackets detected")

    # Test 5: Invalid node IDs
    print("\n5. Testing invalid node IDs...")
    invalid_node_ids = """flowchart TD
    123Invalid["Start with number"] --> Valid_Node["Good"]
    Valid_Node --> 99["Another invalid"]"""

    result = diagram_generator.validate_mermaid_syntax(invalid_node_ids)
    if result["valid"] or len([e for e in result["errors"] if "Invalid" in e and "node ID" in e]) < 2:
        print(f"❌ FAIL: Should detect invalid node IDs - {result}")
        return False
    print(f"✅ Invalid node IDs detected")

    # Test 6: Invalid relationship syntax
    print("\n6. Testing invalid relationship syntax...")
    invalid_relationships = """flowchart TD
    A --> --> B
    C ->- D
    E --> """

    result = diagram_generator.validate_mermaid_syntax(invalid_relationships)
    if result["valid"] or len([e for e in result["errors"] if "relationship" in e.lower()]) == 0:
        print(f"❌ FAIL: Should detect invalid relationships - {result}")
        return False
    print(f"✅ Invalid relationship syntax detected")

    # Test 7: Invalid style definitions
    print("\n7. Testing invalid style definitions...")
    invalid_styles = """flowchart TD
    A["Node"] --> B["Node2"]
    style
    style A
    style 123Invalid fill:#color
    style A fill:notacolor"""

    result = diagram_generator.validate_mermaid_syntax(invalid_styles)
    if result["valid"] or len([e for e in result["errors"] if "style" in e.lower()]) < 2:
        print(f"❌ FAIL: Should detect invalid style definitions - {result}")
        return False
    print(f"✅ Invalid style definitions detected")

    # Test 8: Unbalanced quotes
    print("\n8. Testing unbalanced quotes...")
    unbalanced_quotes = """flowchart TD
    A["Unbalanced quote]
    C["Another unbalanced"
    D["Valid"] --> E["Also valid"]"""

    result = diagram_generator.validate_mermaid_syntax(unbalanced_quotes)
    if result["valid"] or len([e for e in result["errors"] if "quote" in e.lower()]) < 1:
        print(f"❌ FAIL: Should detect unbalanced quotes - {result}")
        return False
    print(f"✅ Unbalanced quotes detected")

    # Test 9: Wrong bracket types
    print("\n9. Testing wrong bracket types...")
    wrong_brackets = """flowchart TD
    A("Should be square") --> B{"Also wrong"}
    C[(Database shape)] --> D["Correct"]"""

    result = diagram_generator.validate_mermaid_syntax(wrong_brackets)
    error_warning_count = len([w for w in result["warnings"] if "bracket" in w.lower() or "node syntax" in w.lower()]) + len([e for e in result["errors"] if "node ID" in e])
    if error_warning_count < 1:
        print(f"❌ FAIL: Should detect wrong bracket types - {result}")
        return False
    print(f"✅ Wrong bracket types detected")

    # Test 10: Complex valid case
    print("\n10. Testing complex valid case...")
    complex_valid = """flowchart LR
    subgraph Title["Complex Diagram"]
    end
    PersonA["Dr. Jane Smith"] --> OrgB["Tech Corp"]
    PersonC["John Doe"] --> OrgB
    OrgB --> LocationD["San Francisco"]
    style PersonA fill:#FFE4B5
    style PersonC fill:#FFE4B5
    style OrgB fill:#B0E0E6
    style LocationD fill:#98FB98"""

    result = diagram_generator.validate_mermaid_syntax(complex_valid)
    if not result["valid"]:
        print(f"❌ FAIL: Complex valid case rejected - {result['errors']}")
        return False
    print(f"✅ Complex valid case accepted")

    print(f"\n🎯 ACCEPTANCE CRITERIA CHECK:")
    print(f"✅ Detect invalid syntax: 8 different error types detected")
    print(f"✅ Provide specific error messages: Detailed error descriptions provided")
    print(f"✅ Validate both valid and invalid samples: 10 test scenarios covered")

    return True

def main():
    try:
        success = test_enhanced_validation()
        if success:
            print(f"\n🎉 ALL TESTS PASSED: Enhanced validation system is functional")
            return 0
        else:
            print(f"\n❌ TESTS FAILED: Enhanced validation system has issues")
            return 1
    except Exception as e:
        print(f"\n💥 TEST CRASHED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())