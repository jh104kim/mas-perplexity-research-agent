from app.nodes.evaluator import evaluate_parsed_result


def test_evaluator_passes_complete_result():
    parsed = {
        "executive_summary": "Good summary",
        "key_findings": ["A", "B", "C"],
        "sources": ["https://a.example", "https://b.example"],
    }

    report = evaluate_parsed_result(parsed)

    assert report["score"] >= 85
    assert report["passed"] is True


def test_evaluator_fails_weak_result():
    parsed = {
        "executive_summary": "",
        "key_findings": ["A"],
        "sources": [],
    }

    report = evaluate_parsed_result(parsed)

    assert report["score"] < 85
    assert report["passed"] is False
    assert "executive_summary" in report["missing"]

