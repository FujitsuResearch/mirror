"""Small generic PUCT search utilities.

This module is model-agnostic. It does not contain prompts, target wrappers, or
API calls. Users provide the state transition and evaluation functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Callable, Generic, Hashable, Iterable, TypeVar

State = TypeVar("State", bound=Hashable)
Action = TypeVar("Action", bound=Hashable)


@dataclass
class ActionStats:
    prior: float
    visits: int = 0
    value_sum: float = 0.0

    @property
    def value(self) -> float:
        if self.visits == 0:
            return 0.0
        return self.value_sum / self.visits


@dataclass
class SearchNode(Generic[State, Action]):
    state: State
    actions: dict[Action, ActionStats] = field(default_factory=dict)
    children: dict[Action, "SearchNode[State, Action]"] = field(default_factory=dict)
    visits: int = 0


def select_puct(node: SearchNode[State, Action], c_puct: float) -> Action:
    if not node.actions:
        raise ValueError("node has no actions")
    parent_visits = max(1, node.visits)

    def score(item: tuple[Action, ActionStats]) -> float:
        _, stats = item
        exploration = c_puct * stats.prior * sqrt(parent_visits) / (1 + stats.visits)
        return stats.value + exploration

    return max(node.actions.items(), key=score)[0]


def normalize_priors(priors: dict[Action, float], actions: Iterable[Action]) -> dict[Action, float]:
    actions = list(actions)
    if not actions:
        raise ValueError("actions must not be empty")
    cleaned = {action: max(0.0, float(priors.get(action, 0.0))) for action in actions}
    total = sum(cleaned.values())
    if total == 0.0:
        return {action: 1.0 / len(actions) for action in actions}
    return {action: value / total for action, value in cleaned.items()}


def run_puct_search(
    root_state: State,
    actions_fn: Callable[[State], Iterable[Action]],
    transition_fn: Callable[[State, Action], State],
    evaluate_fn: Callable[[State], float],
    prior_fn: Callable[[State, Iterable[Action]], dict[Action, float]],
    simulations: int,
    c_puct: float = sqrt(2.0),
) -> SearchNode[State, Action]:
    """Run a shallow generic PUCT search and return the root node.

    The search expands one selected path per simulation until it reaches a new
    state, evaluates that state, and backs the reward up along the path.
    """

    if simulations <= 0:
        raise ValueError("simulations must be positive")

    nodes: dict[State, SearchNode[State, Action]] = {}

    def get_node(state: State) -> SearchNode[State, Action]:
        if state not in nodes:
            actions = list(actions_fn(state))
            priors = normalize_priors(prior_fn(state, actions), actions)
            nodes[state] = SearchNode(
                state=state,
                actions={action: ActionStats(prior=priors[action]) for action in actions},
            )
        return nodes[state]

    root = get_node(root_state)
    for _ in range(simulations):
        node = root
        path: list[tuple[SearchNode[State, Action], Action]] = []

        while node.actions:
            action = select_puct(node, c_puct)
            path.append((node, action))
            if action not in node.children:
                child_state = transition_fn(node.state, action)
                child = get_node(child_state)
                node.children[action] = child
                node = child
                break
            node = node.children[action]

        reward = float(evaluate_fn(node.state))
        if not 0.0 <= reward <= 1.0:
            raise ValueError("evaluate_fn must return a score in [0, 1]")

        node.visits += 1
        for parent, action in reversed(path):
            stats = parent.actions[action]
            stats.visits += 1
            stats.value_sum += reward
            parent.visits += 1

    return root
