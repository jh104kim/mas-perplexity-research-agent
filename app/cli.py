from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from app.graph import run_approved_state
from app.nodes.planner import planner_node
from app.output import make_dated_output_dir
from app.plan_gate import apply_plan_decision
from app.state import ExecutorMode, create_initial_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HITL Perplexity Research Agent MVP")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--mode", choices=["mock", "hitl"], default="mock", help="Execution mode")
    parser.add_argument("--result-file", help="Markdown result file for hitl mode")
    parser.add_argument("--output-dir", default=".", help="Directory for generated artifacts")
    parser.add_argument("--dated-output", action="store_true", help="Create a dated subfolder under output-dir")
    parser.add_argument("--auto-approve", action="store_true", help="Skip interactive plan gate")
    return parser.parse_args()


def prompt_for_decision() -> str:
    while True:
        decision = input("Plan decision [approve/revise/stop]: ").strip().lower()
        if decision in {"approve", "revise", "stop"}:
            return decision
        print("approve, revise, stop 중 하나를 입력하세요.")


def main() -> int:
    args = parse_args()
    output_dir = make_dated_output_dir(args.output_dir, args.topic) if args.dated_output else Path(args.output_dir)
    state = create_initial_state(
        args.topic,
        mode=args.mode,
        output_dir=output_dir,
        result_file=args.result_file,
    )

    while True:
        planner_node(state)
        print("\n# Research Plan")
        print(yaml.safe_dump(state["research_plan"], allow_unicode=True, sort_keys=False))
        decision = "approve" if args.auto_approve else prompt_for_decision()
        apply_plan_decision(state, decision)
        if state.get("plan_status") == "revise":
            continue
        break

    if state.get("plan_status") == "stop":
        print("Workflow stopped before research.")
        return 0

    result = run_approved_state(state)
    if result.get("awaiting_hitl"):
        print("HITL result markdown file is required. See research_prompt.md.")
        return 2

    print("문제 없음")
    print(f"Report: {Path(result.get('output_dir', '.')) / 'quick_summary_report.md'}")
    print(f"HTML: {Path(result.get('output_dir', '.')) / 'report.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
