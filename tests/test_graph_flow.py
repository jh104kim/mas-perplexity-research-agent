from pathlib import Path

from app.graph import run_research


def test_mock_mode_full_workflow_creates_artifacts(tmp_path):
    state = run_research("LangGraph MAS Workflow", mode="mock", output_dir=tmp_path)

    assert state["status"] == "completed"
    assert state["evaluation_score"] >= 85
    assert (tmp_path / "research_plan.yaml").exists()
    assert (tmp_path / "approved_plan.yaml").exists()
    assert (tmp_path / "research_prompt.md").exists()
    assert (tmp_path / "raw_result_01.md").exists()
    assert (tmp_path / "parsed_result.json").exists()
    assert (tmp_path / "evaluation_report.yaml").exists()
    assert (tmp_path / "quick_summary_report.md").exists()
    assert (tmp_path / "report.html").exists()
    assert (tmp_path / "run_log.json").exists()


def test_hitl_mode_reads_user_result_markdown(tmp_path):
    fixture = Path("tests/fixtures/hitl_result.md").resolve()
    state = run_research("HITL Topic", mode="hitl", output_dir=tmp_path, result_file=str(fixture))

    assert state["status"] == "completed"
    assert state["evaluation_score"] >= 85
    assert state["parsed_result"]["key_findings"]
    assert (tmp_path / "research_prompt.md").exists()
    assert (tmp_path / "raw_result_01.md").exists()


def test_hitl_mode_without_result_file_waits_for_user_file(tmp_path):
    state = run_research("HITL Missing", mode="hitl", output_dir=tmp_path)

    assert state["awaiting_hitl"] is True
    assert state["status"] == "awaiting_hitl_result"
    assert state["errors"]
    assert (tmp_path / "research_prompt.md").exists()
    assert (tmp_path / "run_log.json").exists()

