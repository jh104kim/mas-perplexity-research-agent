from app.nodes.parser import parse_markdown_result


def test_parser_extracts_summary_findings_and_sources():
    markdown = """# Research Result

## Executive Summary
This is the summary.

## Key Findings
- Finding A
- Finding B

## Sources
- https://example.com/a
- https://example.com/b
"""

    parsed = parse_markdown_result(markdown)

    assert parsed["executive_summary"] == "This is the summary."
    assert parsed["key_findings"] == ["Finding A", "Finding B"]
    assert parsed["sources"] == ["https://example.com/a", "https://example.com/b"]

