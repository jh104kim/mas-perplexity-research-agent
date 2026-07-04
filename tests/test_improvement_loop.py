from app.graph import run_research


def test_improvement_loop_stops_after_three_attempts(tmp_path):
    state = run_research(
        "Low Quality Topic",
        output_dir=tmp_path,
        force_low_quality=True,
        score_sequence=[40, 45, 50, 55],
    )

    assert state["improvement_count"] == 3
    assert len(state["raw_results"]) == 4
    assert state["evaluation_score"] == 55
    assert "개선 루프 최대 3회" in state["quick_summary_report"]

