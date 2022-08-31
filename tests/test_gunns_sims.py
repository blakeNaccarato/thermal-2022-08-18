"""Tests for gunns_sims."""

import datadict

from gunns_sims.contextdict import ContextDict


@datadict.dataclass
class Node:
    label: str = ""
    pos: tuple[float, float] = (0, 0)


test = Node(label="well", pos=(0, 0))


def test_thing():

    context_dict = ContextDict(
        hello=Node("well", (0, 0)),
        world=Node("quell", (1, 1)),
    )
    with context_dict.context("label"):
        context_dict["hello"] = "test"

    context_dict["hello"] = Node()
