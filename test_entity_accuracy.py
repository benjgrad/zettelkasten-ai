#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.entity_extraction import entity_service

# Test cases with known entities for validation
TEST_CASES = [
    {
        "text": "Apple Inc. CEO Tim Cook announced the new iPhone at the Apple Park headquarters in Cupertino, California.",
        "expected_entities": [
            ("Apple Inc.", "ORG"),
            ("Tim Cook", "PERSON"),
            ("Apple Park", "ORG"),
            ("Cupertino", "GPE"),
            ("California", "GPE")
        ]
    },
    {
        "text": "President Joe Biden met with Chancellor Angela Merkel in Berlin to discuss NATO policies.",
        "expected_entities": [
            ("Joe Biden", "PERSON"),
            ("Angela Merkel", "PERSON"),
            ("Berlin", "GPE"),
            ("NATO", "ORG")
        ]
    },
    {
        "text": "Microsoft Corporation reported record earnings. CEO Satya Nadella said the company's Azure cloud platform grew 50% in the Seattle-based tech giant.",
        "expected_entities": [
            ("Microsoft Corporation", "ORG"),
            ("Satya Nadella", "PERSON"),
            ("Azure", "ORG"),
            ("Seattle", "GPE")
        ]
    },
    {
        "text": "The European Union imposed sanctions on Russia following the invasion of Ukraine. Foreign Minister Sergey Lavrov criticized the decision.",
        "expected_entities": [
            ("European Union", "ORG"),
            ("Russia", "GPE"),
            ("Ukraine", "GPE"),
            ("Sergey Lavrov", "PERSON")
        ]
    },
    {
        "text": "Tesla's Elon Musk announced plans to build a new Gigafactory in Texas. The Austin facility will produce the Cybertruck.",
        "expected_entities": [
            ("Tesla", "ORG"),
            ("Elon Musk", "PERSON"),
            ("Texas", "GPE"),
            ("Austin", "GPE")
        ]
    },
    {
        "text": "The World Health Organization warned about a new COVID-19 variant. Dr. Tedros Adhanom Ghebreyesus urged countries to increase vaccination rates.",
        "expected_entities": [
            ("World Health Organization", "ORG"),
            ("Tedros Adhanom Ghebreyesus", "PERSON")
        ]
    },
    {
        "text": "Amazon Web Services launched new data centers in Singapore and Mumbai. CEO Andy Jassy said this expansion supports growth in Asia.",
        "expected_entities": [
            ("Amazon Web Services", "ORG"),
            ("Singapore", "GPE"),
            ("Mumbai", "GPE"),
            ("Andy Jassy", "PERSON"),
            ("Asia", "GPE")
        ]
    },
    {
        "text": "The Federal Reserve raised interest rates. Chairman Jerome Powell cited inflation concerns in his Washington D.C. announcement.",
        "expected_entities": [
            ("Federal Reserve", "ORG"),
            ("Jerome Powell", "PERSON"),
            ("Washington D.C.", "GPE")
        ]
    },
    {
        "text": "Google's parent company Alphabet reported strong quarterly results. CEO Sundar Pichai highlighted YouTube's performance.",
        "expected_entities": [
            ("Google", "ORG"),
            ("Alphabet", "ORG"),
            ("Sundar Pichai", "PERSON"),
            ("YouTube", "ORG")
        ]
    },
    {
        "text": "The United Nations Security Council met in New York to address the crisis in Syria. Secretary-General António Guterres called for immediate action.",
        "expected_entities": [
            ("United Nations Security Council", "ORG"),
            ("New York", "GPE"),
            ("Syria", "GPE"),
            ("António Guterres", "PERSON")
        ]
    }
]

def validate_accuracy():
    print("🧪 Running Entity Extraction Accuracy Validation")
    print("=" * 60)

    results = entity_service.validate_extraction_accuracy(TEST_CASES)

    print(f"\n📊 VALIDATION RESULTS:")
    print(f"Total test cases: {results['total_tests']}")
    print(f"Expected entities: {results['total_expected']}")
    print(f"Extracted entities: {results['total_extracted']}")
    print(f"Correct matches: {results['correct_entities']}")
    print(f"\n📈 ACCURACY METRICS:")
    print(f"Precision: {results['precision']:.2%}")
    print(f"Recall: {results['recall']:.2%}")
    print(f"F1 Score: {results['f1_score']:.2%}")

    # Detailed analysis
    print(f"\n🔍 DETAILED ANALYSIS:")
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\nTest Case {i}:")
        print(f"Text: {test_case['text'][:100]}...")

        extracted_entities = entity_service.extract_entities(test_case["text"])
        extracted_set = set((ent["text"], ent["label"]) for ent in extracted_entities)
        expected_set = set(test_case["expected_entities"])

        correct = expected_set.intersection(extracted_set)
        missed = expected_set - extracted_set
        extra = extracted_set - expected_set

        print(f"  ✅ Correct: {len(correct)}/{len(expected_set)} - {list(correct)}")
        if missed:
            print(f"  ❌ Missed: {list(missed)}")
        if extra:
            print(f"  ➕ Extra: {list(extra)}")

    # Acceptance criteria check
    print(f"\n🎯 ACCEPTANCE CRITERIA CHECK:")
    if results['f1_score'] >= 0.8:
        print(f"✅ PASS: F1 Score ({results['f1_score']:.2%}) >= 80% requirement")
        return True
    else:
        print(f"❌ FAIL: F1 Score ({results['f1_score']:.2%}) < 80% requirement")
        return False

if __name__ == "__main__":
    success = validate_accuracy()
    sys.exit(0 if success else 1)