import pytest
from backend.app.services.knowledge_retrieval import KnowledgeBaseService

def test_knowledge_base_loading():
    service = KnowledgeBaseService()
    success = service.load_knowledge_base()
    assert success is True
    assert service.loaded is True
    assert len(service.load_errors) == 0

    status = service.get_status()
    assert status["loaded"] is True
    assert status["total_files"] >= 44
    assert status["source_records"] == 37
    assert "Haryana" in status["target_regions"]
    assert "Punjab" in status["target_regions"]

def test_knowledge_schemes():
    service = KnowledgeBaseService()
    service.load_knowledge_base()

    schemes = service.get_all_schemes()
    assert len(schemes) >= 6
    ids = [s["id"] for s in schemes]
    assert "scheme-national-pmkisan-001" in ids
    assert "scheme-national-pmfby-001" in ids

    # Test scheme with sources
    pmkisan = service.get_scheme_by_id("scheme-national-pmkisan-001")
    assert pmkisan is not None
    assert len(pmkisan["sources"]) > 0

def test_knowledge_search():
    service = KnowledgeBaseService()
    service.load_knowledge_base()

    # Search for wheat sowing
    results = service.search_knowledge("गेहूं बुवाई")
    assert len(results) > 0
    top = results[0]
    assert "answer_simple" in top
    assert "hi" in top["answer_simple"]
    assert top["verification_status"] in ("verified", "pending_review")

def test_non_empty_files_tolerance():
    service = KnowledgeBaseService()
    service.load_knowledge_base()

    # Crops like apple, bajra now have detailed info
    assert "apple" in service.crops_data
    assert len(service.crops_data["apple"]) > 0
    # Must successfully retrieve guidance
    res = service.get_crop_guidance("apple")
    assert len(res) > 0

