from app.nodes.planner import planner_node
from app.plan_gate import apply_plan_decision
from app.state import create_initial_state


def test_approve_before_executor_does_not_create_raw_results(tmp_path):
    state = create_initial_state("Plan Gate", output_dir=tmp_path)
    planner_node(state)
    apply_plan_decision(state, "approve")

    assert state["plan_status"] == "approve"
    assert state.get("raw_results") == []
    assert state.get("research_prompt") == ""
    assert (tmp_path / "approved_plan.yaml").exists()


def test_stop_exits_without_executor_call(tmp_path):
    state = create_initial_state("Plan Gate", output_dir=tmp_path)
    planner_node(state)
    apply_plan_decision(state, "stop")

    assert state["status"] == "stopped"
    assert state.get("raw_results") == []
    assert (tmp_path / "run_log.json").exists()


def test_revise_regenerates_plan(tmp_path):
    state = create_initial_state("Plan Gate", output_dir=tmp_path)
    planner_node(state)
    first_revision = state["research_plan"]["revision"]

    apply_plan_decision(state, "revise")

    assert state["plan_status"] == "revise"
    assert state["research_plan"]["revision"] == first_revision + 1

