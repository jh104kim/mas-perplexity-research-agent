from datetime import datetime

from app.output import make_dated_output_dir, slugify


def test_slugify_keeps_readable_topic():
    assert slugify("LangGraph MAS Workflow!") == "LangGraph-MAS-Workflow"


def test_make_dated_output_dir_creates_unique_folder(tmp_path):
    first = make_dated_output_dir(tmp_path, "Topic A", datetime(2026, 7, 4, 1, 2, 3))
    second = make_dated_output_dir(tmp_path, "Topic B", datetime(2026, 7, 4, 1, 2, 4))

    assert first.exists()
    assert second.exists()
    assert first != second
