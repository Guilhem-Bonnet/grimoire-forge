"""Test A2 — token-budget.py vendorisé et branché dans guardrail-policy.py.

Écart couvert : B2 (audit-ecarts-reference-agentique-20260908.md, action A2
du plan-execution-ecarts-20260908.md). Avant correction :
  - .github/hooks/lib/token-budget.py n'existait pas -> assess_token_budget()
    était un no-op silencieux (renvoyait toujours {}).
  - enforcementRecommended (calculé par assess_token_budget) n'était lu par
    personne : le hook Stop ne produisait jamais de systemMessage.

Exécuter avec le python du venv (celui que les scripts .sh utilisent) :
  .venv/bin/python -m pytest .github/hooks/tests/test_token_budget_wired.py -v

Note d'implémentation : guardrail-policy.py déclare des dataclasses
frozen+slots dont la résolution de type au moment de la définition de
classe consulte sys.modules[cls.__module__]. Un module chargé par
importlib.util sans être enregistré dans sys.modules AVANT exec_module()
lève ``AttributeError: 'NoneType' object has no attribute '__dict__'``
sous Python >= 3.12/3.14. _load_guardrail_policy() applique le correctif
(enregistrement dans sys.modules avant exécution).
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import importlib.util
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parents[1]
LIB_DIR = HOOKS_DIR / "lib"
PROJECT_ROOT = HOOKS_DIR.parents[1]
MODULE_NAME = "grimoire_guardrail_policy_under_test"


def _load_guardrail_policy():
    spec = importlib.util.spec_from_file_location(MODULE_NAME, LIB_DIR / "guardrail-policy.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module  # requis avant exec_module, cf. docstring
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def policy():
    return _load_guardrail_policy()


def test_token_budget_file_is_vendored():
    """Sans ce fichier, assess_token_budget() redevient un no-op silencieux."""
    vendored = LIB_DIR / "token-budget.py"
    assert vendored.exists(), (
        "token-budget.py absent de .github/hooks/lib/ — assess_token_budget() "
        "redeviendra un no-op silencieux (ecart B2)."
    )
    assert "TokenBudgetEnforcer" in vendored.read_text(encoding="utf-8")


def test_assess_token_budget_returns_non_empty_status(policy):
    status = policy.assess_token_budget(PROJECT_ROOT, force=True)
    assert status, "assess_token_budget() a renvoye un statut vide alors que force=True"
    assert "level" in status
    assert "usagePct" in status
    assert "enforcementRecommended" in status
    assert isinstance(status["enforcementRecommended"], bool)


def test_assess_token_budget_is_noop_without_vendored_file(policy, tmp_path, monkeypatch):
    """Reproduit le comportement d'origine (ecart B2) si le fichier disparait."""
    empty_lib = tmp_path / "lib"
    empty_lib.mkdir()
    monkeypatch.setattr(policy, "tool_dir", lambda: empty_lib)
    policy._TOOL_MODULE_CACHE.clear()
    try:
        status = policy.assess_token_budget(PROJECT_ROOT, force=True)
        assert status == {}, "assess_token_budget() aurait du etre un no-op sans token-budget.py"
    finally:
        policy._TOOL_MODULE_CACHE.clear()


def test_format_token_budget_enforcement_message_empty_when_not_recommended(policy):
    assert policy.format_token_budget_enforcement_message({}) == ""
    assert (
        policy.format_token_budget_enforcement_message({"enforcementRecommended": False, "level": "ok"}) == ""
    )


def test_format_token_budget_enforcement_message_names_overrun(policy):
    token_budget = {
        "level": "critical",
        "usagePct": 0.82,
        "enforcementRecommended": True,
        "recommendations": ["résumer le contexte P2/P3"],
    }
    message = policy.format_token_budget_enforcement_message(token_budget)
    assert message, "enforcementRecommended=True doit produire un message nommant le depassement"
    assert "82%" in message
    assert "critical" in message


def test_command_stop_closure_emits_system_message_when_enforcement_recommended(policy, tmp_path, monkeypatch, capsys):
    """Bout-en-bout : le hook Stop (stop-closure) doit émettre systemMessage
    quand enforcementRecommended est vrai — c'est le seul canal qu'aucun
    hôte ne filtre sur un évènement Stop (voir hosts/runtime.py côté
    produit : ``# No host reads additionalContext on a stop event``)."""
    forced_budget = {
        "level": "critical",
        "usagePct": 0.91,
        "usedTokens": 91000,
        "windowTokens": 100000,
        "recommendations": ["résumer"],
        "enforcementRecommended": True,
    }
    monkeypatch.setattr(policy, "assess_token_budget", lambda *a, **k: dict(forced_budget))
    monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))

    project_root = tmp_path / "project"
    project_root.mkdir()
    prompt_state_file = tmp_path / "prompt-state.json"
    prompt_state_file.write_text("{}", encoding="utf-8")
    task_latest_file = tmp_path / "task-latest.json"
    task_latest_file.write_text("{}", encoding="utf-8")
    subagent_latest_file = tmp_path / "subagent-latest.json"
    subagent_latest_file.write_text("{}", encoding="utf-8")
    latest_file = tmp_path / "stop-latest.json"

    args = argparse.Namespace(
        project_root=project_root,
        prompt_state_file=prompt_state_file,
        task_latest_file=task_latest_file,
        subagent_latest_file=subagent_latest_file,
        latest_file=latest_file,
    )

    rc = policy.command_stop_closure(args)
    assert rc == 0
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert "systemMessage" in payload, (
        f"systemMessage absent alors qu'enforcementRecommended=True — sortie: {out}"
    )
    assert "91%" in payload["systemMessage"] or "critical" in payload["systemMessage"]


def test_command_stop_closure_no_system_message_when_not_recommended(policy, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        policy,
        "assess_token_budget",
        lambda *a, **k: {"level": "ok", "usagePct": 0.1, "enforcementRecommended": False},
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))

    project_root = tmp_path / "project"
    project_root.mkdir()
    prompt_state_file = tmp_path / "prompt-state.json"
    prompt_state_file.write_text("{}", encoding="utf-8")
    task_latest_file = tmp_path / "task-latest.json"
    task_latest_file.write_text("{}", encoding="utf-8")
    subagent_latest_file = tmp_path / "subagent-latest.json"
    subagent_latest_file.write_text("{}", encoding="utf-8")
    latest_file = tmp_path / "stop-latest.json"

    args = argparse.Namespace(
        project_root=project_root,
        prompt_state_file=prompt_state_file,
        task_latest_file=task_latest_file,
        subagent_latest_file=subagent_latest_file,
        latest_file=latest_file,
    )

    rc = policy.command_stop_closure(args)
    assert rc == 0
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert "systemMessage" not in payload
