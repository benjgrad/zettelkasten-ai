import spacy
import sqlite3
from typing import List, Dict, Any, Tuple
from src.models import db

class EntityExtractionService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.target_entities = ["PERSON", "ORG", "GPE"]

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        doc = self.nlp(text)
        entities = []
        processed_texts = set()

        for ent in doc.ents:
            if ent.label_ in self.target_entities:
                # Clean up entity text
                entity_text = ent.text.strip()

                # Handle common prefixes (remove "The " from organization names)
                if ent.label_ == "ORG" and entity_text.startswith("The "):
                    clean_text = entity_text[4:]  # Remove "The "
                    # Add both original and cleaned version to avoid duplicates
                    if clean_text not in processed_texts:
                        entities.append({
                            "text": clean_text,
                            "label": ent.label_,
                            "start": ent.start_char + 4,
                            "end": ent.end_char,
                            "confidence": float(ent._.get("score", 0.0)) if hasattr(ent._, "score") else 1.0
                        })
                        processed_texts.add(clean_text)

                # Add original entity if not already processed
                if entity_text not in processed_texts:
                    entities.append({
                        "text": entity_text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "confidence": float(ent._.get("score", 0.0)) if hasattr(ent._, "score") else 1.0
                    })
                    processed_texts.add(entity_text)

        return entities

    def process_article(self, article_id: int) -> Dict[str, Any]:
        with db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT id, title, content, summary FROM articles WHERE id = ?",
                (article_id,)
            )
            article = cursor.fetchone()

        if not article:
            return {"error": f"Article {article_id} not found"}

        text_to_process = article["content"] or article["summary"] or article["title"]

        entities = self.extract_entities(text_to_process)

        # Store entities in database
        entities_stored = 0
        for entity in entities:
            entity_id = db.add_entity(
                article_id=article_id,
                text=entity["text"],
                label=entity["label"],
                start_pos=entity["start"],
                end_pos=entity["end"],
                confidence=entity["confidence"]
            )
            if entity_id:
                entities_stored += 1

        return {
            "article_id": article_id,
            "article_title": article["title"],
            "text_processed": len(text_to_process),
            "entities_found": len(entities),
            "entities_stored": entities_stored,
            "entities": entities
        }

    def get_article_entities(self, article_id: int) -> Dict[str, Any]:
        entities = db.get_entities_by_article(article_id)
        return {
            "article_id": article_id,
            "entity_count": len(entities),
            "entities": entities
        }

    def validate_extraction_accuracy(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {
            "total_tests": len(test_cases),
            "correct_entities": 0,
            "total_expected": 0,
            "total_extracted": 0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "by_type": {}
        }

        for test_case in test_cases:
            text = test_case["text"]
            expected = set(test_case["expected_entities"])

            extracted_entities = self.extract_entities(text)
            extracted = set((ent["text"], ent["label"]) for ent in extracted_entities)

            correct = expected.intersection(extracted)
            results["correct_entities"] += len(correct)
            results["total_expected"] += len(expected)
            results["total_extracted"] += len(extracted)

        if results["total_extracted"] > 0:
            results["precision"] = results["correct_entities"] / results["total_extracted"]
        if results["total_expected"] > 0:
            results["recall"] = results["correct_entities"] / results["total_expected"]
        if results["precision"] + results["recall"] > 0:
            results["f1_score"] = 2 * (results["precision"] * results["recall"]) / (results["precision"] + results["recall"])

        return results

entity_service = EntityExtractionService()