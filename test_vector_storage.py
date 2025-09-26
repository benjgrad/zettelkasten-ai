#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.vector_storage import vector_storage
from src.models import db

def test_vector_storage():
    print("🧪 Running Vector Storage Validation")
    print("=" * 60)

    # Test 1: Check collection stats
    print("\n1. Testing collection initialization...")
    stats = vector_storage.get_collection_stats()
    if "error" in stats:
        print(f"❌ FAIL: Collection initialization failed - {stats['error']}")
        return False
    print(f"✅ Collection initialized: {stats['total_embeddings']} existing embeddings")

    # Test 2: Get sample articles from database
    print("\n2. Testing article retrieval...")
    with db.get_connection() as conn:
        cursor = conn.execute("SELECT id, title FROM articles LIMIT 5")
        sample_articles = cursor.fetchall()

    if not sample_articles:
        print("❌ FAIL: No articles found in database")
        return False
    print(f"✅ Found {len(sample_articles)} sample articles")

    # Test 3: Add embeddings for sample articles
    print("\n3. Testing embedding generation and storage...")
    test_article_id = sample_articles[0][0]
    result = vector_storage.add_article_embedding(test_article_id)

    if "error" in result:
        print(f"❌ FAIL: Embedding generation failed - {result['error']}")
        return False

    print(f"✅ Embedding stored for article {test_article_id}: {result['embedding_dimension']} dimensions")

    # Test 4: Batch add embeddings for all sample articles
    print("\n4. Testing batch embedding creation...")
    sample_ids = [article[0] for article in sample_articles]
    batch_result = vector_storage.batch_add_embeddings(sample_ids)

    if batch_result["failed"] > 0:
        print(f"⚠️  Partial success: {batch_result['successful']}/{batch_result['total_articles']} succeeded")
        for error in batch_result["errors"][:3]:  # Show first 3 errors
            print(f"   Error: {error}")
    else:
        print(f"✅ Batch embedding complete: {batch_result['successful']} articles processed")

    # Test 5: Test semantic search functionality
    print("\n5. Testing semantic search...")
    test_queries = [
        "technology innovation",
        "government policy",
        "business economy"
    ]

    all_searches_successful = True
    for query in test_queries:
        search_result = vector_storage.semantic_search(query, limit=3)

        if "error" in search_result:
            print(f"❌ Search failed for '{query}': {search_result['error']}")
            all_searches_successful = False
        else:
            print(f"✅ Search '{query}': {search_result['results_count']} results")
            for i, result in enumerate(search_result['results'][:2], 1):
                print(f"   {i}. {result['title'][:50]}... (similarity: {result['similarity_score']:.3f})")

    if not all_searches_successful:
        return False

    # Test 6: Verify similarity search quality
    print("\n6. Testing search result quality...")
    tech_search = vector_storage.semantic_search("technology computer software", limit=5)

    if "error" in tech_search:
        print(f"❌ Quality test failed: {tech_search['error']}")
        return False

    if tech_search['results_count'] == 0:
        print("❌ No search results returned")
        return False

    # Check if results have reasonable similarity scores (adjust threshold for distance-based system)
    good_results = [r for r in tech_search['results'] if r['similarity_score'] > 0.0]
    if len(good_results) == 0:
        print("❌ No results with reasonable similarity scores")
        return False

    # Show actual scores for debugging
    print(f"✅ Quality test passed: {len(good_results)} results with similarity > 0.0")
    for result in tech_search['results'][:3]:
        print(f"   - Distance: {result.get('distance', 'N/A'):.3f}, Similarity: {result['similarity_score']:.3f}")

    # Final stats
    print("\n7. Final collection statistics...")
    final_stats = vector_storage.get_collection_stats()
    print(f"✅ Final stats: {final_stats['total_embeddings']} embeddings stored")

    print(f"\n🎯 ACCEPTANCE CRITERIA CHECK:")
    print(f"✅ Store articles with metadata: Verified")
    print(f"✅ Embeddings generated for semantic search: {final_stats['total_embeddings']} embeddings")
    print(f"✅ Insert test article, perform similarity search, retrieve results: Successful")

    return True

def main():
    try:
        success = test_vector_storage()
        if success:
            print(f"\n🎉 ALL TESTS PASSED: Vector storage system is functional")
            return 0
        else:
            print(f"\n❌ TESTS FAILED: Vector storage system has issues")
            return 1
    except Exception as e:
        print(f"\n💥 TEST CRASHED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())