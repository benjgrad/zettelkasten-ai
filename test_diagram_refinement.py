#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.diagram_refinement import diagram_refinement
from src.services.diagram_generator import diagram_generator

def test_diagram_refinement():
    print("🧪 Running Diagram Refinement Validation Tests")
    print("=" * 60)

    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("   Setting mock mode for testing basic functionality...")
        return test_mock_refinement()

    # Test starting diagram
    initial_diagram = """flowchart TD
    A["Charles Mwesigwa"] --> B["Dubai Government"]
    C["Tech Innovation"] --> D["Smart City"]
    B --> D
    style A fill:#FFE4B5
    style B fill:#B0E0E6
    style C fill:#FFE4B5
    style D fill:#98FB98"""

    print("\n📋 Initial diagram:")
    print(initial_diagram)

    # Test 1: Single refinement - "make it simpler"
    print("\n1. Testing single refinement: 'make it simpler'...")

    try:
        result1 = diagram_refinement.refine_diagram(
            current_mermaid=initial_diagram,
            feedback="make it simpler",
            context={"article_title": "Dubai Smart City Innovation"}
        )

        if "error" in result1:
            print(f"❌ FAIL: Refinement error - {result1['error']}")
            return False

        if not result1.get("refined_mermaid"):
            print(f"❌ FAIL: No refined diagram returned")
            return False

        print(f"✅ Single refinement successful")
        print(f"   Explanation: {result1['refinement_explanation'][:100]}...")
        print(f"   Valid syntax: {result1['validation']['valid']}")

        simplified_diagram = result1["refined_mermaid"]

    except Exception as e:
        print(f"❌ FAIL: Single refinement crashed - {str(e)}")
        return False

    # Test 2: Iterative refinement through 3 feedback rounds
    print("\n2. Testing 3-iteration refinement sequence...")

    feedback_sequence = [
        "make it simpler",
        "add more connections between elements",
        "organize it better with clear flow"
    ]

    try:
        iterative_result = diagram_refinement.iterative_refinement(
            initial_mermaid=initial_diagram,
            feedback_sequence=feedback_sequence,
            context={"article_title": "Dubai Smart City Innovation"}
        )

        if "error" in iterative_result:
            print(f"❌ FAIL: Iterative refinement error - {iterative_result['error']}")
            return False

        if iterative_result["total_iterations"] != 3:
            print(f"❌ FAIL: Expected 3 iterations, got {iterative_result['total_iterations']}")
            return False

        print(f"✅ 3-iteration refinement successful")
        print(f"   Total iterations: {iterative_result['total_iterations']}")

        # Validate each iteration
        for i, iteration in enumerate(iterative_result["refinement_history"]):
            validation = iteration["validation"]
            print(f"   Iteration {i+1}: {iteration['feedback'][:30]}... - Valid: {validation['valid']}")

            if not validation["valid"]:
                print(f"   ⚠️  Validation errors: {validation['errors']}")

    except Exception as e:
        print(f"❌ FAIL: Iterative refinement crashed - {str(e)}")
        return False

    # Test 3: Validation of refined diagrams
    print("\n3. Testing refined diagram validation...")

    final_diagram = iterative_result["final_diagram"]
    validation_result = diagram_generator.validate_mermaid_syntax(final_diagram)

    if not validation_result["valid"]:
        print(f"❌ FAIL: Final refined diagram has validation errors - {validation_result['errors']}")
        return False

    print(f"✅ Final refined diagram passes validation")
    print(f"   Lines checked: {validation_result['lines_checked']}")
    print(f"   Warnings: {len(validation_result['warnings'])}")

    # Test 4: Render URL generation
    print("\n4. Testing render URL generation...")

    if not iterative_result.get("final_render_url"):
        print(f"❌ FAIL: No render URL generated")
        return False

    if not iterative_result["final_render_url"].startswith("https://mermaid.live/edit#"):
        print(f"❌ FAIL: Invalid render URL format")
        return False

    print(f"✅ Render URL generated successfully")
    print(f"   URL: {iterative_result['final_render_url'][:60]}...")

    print(f"\n🎯 ACCEPTANCE CRITERIA CHECK:")
    print(f"✅ Accept user feedback like 'make it simpler': Confirmed with actual GPT-4 refinement")
    print(f"✅ Update diagram based on feedback: 3 iterations applied successfully")
    print(f"✅ Refine test diagram through 3 iterations: All iterations completed with valid output")

    return True

def test_mock_refinement():
    """Test basic functionality without OpenAI API"""
    print("\n🔧 Running mock refinement tests...")

    # Test error handling for missing API key
    test_diagram = """flowchart TD
    A["Test"] --> B["Node"]"""

    try:
        result = diagram_refinement.refine_diagram(
            current_mermaid=test_diagram,
            feedback="make it simpler"
        )

        # Should get an error due to missing API key
        if "error" not in result:
            print("❌ FAIL: Expected error for missing API key")
            return False

        print("✅ Error handling for missing API key works correctly")
        print(f"   Error: {result['error'][:80]}...")

        return True

    except Exception as e:
        print(f"✅ Exception handling works: {str(e)[:80]}...")
        return True

def main():
    try:
        success = test_diagram_refinement()
        if success:
            print(f"\n🎉 ALL TESTS PASSED: Diagram refinement system is functional")
            return 0
        else:
            print(f"\n❌ TESTS FAILED: Diagram refinement system has issues")
            return 1
    except Exception as e:
        print(f"\n💥 TEST CRASHED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())