from app.graph import run_research


def test_report_builder_writes_markdown_and_html(tmp_path):
    state = run_research("Report Topic", output_dir=tmp_path)

    assert state["evaluation_score"] >= 85
    assert (tmp_path / "quick_summary_report.md").exists()
    assert (tmp_path / "report.html").exists()
    report = (tmp_path / "quick_summary_report.md").read_text(encoding="utf-8")
    assert "Quick Summary Report" in report
    assert "## Source Summary" in report
    assert "## Next Questions" in report
    assert "<html" in (tmp_path / "report.html").read_text(encoding="utf-8")
