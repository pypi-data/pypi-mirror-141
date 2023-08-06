import pytest
import mock
from mlonmcu.setup.task import get_combs, TaskFactory, TaskType, TaskGraph
from mlonmcu.setup.setup import Setup

TestTaskFactory = TaskFactory()

def _validate_example_task1(context, params={}):
    print("_validate_example_task1", params)
    assert "foo" in params and "bar" in params and "special" in params
    if params["foo"] == 0 or params["bar"] == "B":
        return params["special"]
    return False

@TestTaskFactory.provides(["dep0"])
@TestTaskFactory.param("special", [True, False])
@TestTaskFactory.param("foo", [0, 1])
@TestTaskFactory.param("bar", ["A", "B"])
@TestTaskFactory.validate(_validate_example_task1)
@TestTaskFactory.register(category=TaskType.MISC)
def example_task1(context, params={}, rebuild=False):
    context.cache._vars["dep0"] = ""
    pass

@TestTaskFactory.needs(["dep0"])
@TestTaskFactory.provides(["dep1"])
@TestTaskFactory.register(category=TaskType.MISC)
def example_task2(context, params={}, rebuild=False):
    context.cache._vars["dep1"] = ""
    pass

def test_task_registry():
    assert len(TestTaskFactory.registry) == 2
    assert len(TestTaskFactory.validates) == 1
    assert len(TestTaskFactory.dependencies) == 1
    assert len(TestTaskFactory.providers) == 2
    assert len(TestTaskFactory.types) == 2
    assert len(TestTaskFactory.params) == 2
    assert len(TestTaskFactory.params["example_task1"]) == 3

def test_task_registry_reset_changes():
    TestTaskFactory.changed = ["dep0"]
    TestTaskFactory.reset_changes()
    assert len(TestTaskFactory.changed) == 0

@pytest.mark.parametrize("progress", [False, True])
@pytest.mark.parametrize("print_output", [False, True])
@pytest.mark.parametrize("rebuild", [False, True])  # TODO: actually test this
@pytest.mark.parametrize("write_cache", [False])  # TODO: True
def test_setup_install_dependencies(progress, print_output, rebuild, write_cache, fake_context):
    # example_task1_mock = mock.Mock(return_value=True)
    TestTaskFactory.registry["example_task1"] = mock.Mock(return_value=True)
    # example_task2_mock = mock.Mock(return_value=True)
    TestTaskFactory.registry["example_task2"] = mock.Mock(return_value=True)
    config = {"print_output": print_output}
    installer = Setup(config=config, context=fake_context, tasks_factory=TestTaskFactory)
    result = installer.install_dependencies(progress=progress, write_cache=write_cache, rebuild=rebuild)
    # assert example_task1_mock.call_count == 3
    assert TestTaskFactory.registry["example_task1"].call_count == 1  # Due to the mock, the actual wrapper is not executed anymore, params are not considered etc
    # assert example_task2_mock.call_count == 1
    assert TestTaskFactory.registry["example_task2"].call_count == 1

def test_task_get_combs():
    assert get_combs({}) == []
    assert get_combs({"foo": []}) == []  # TODO: invalid?
    assert get_combs({"foo": [0]}) == [{"foo": 0}]
    # assert set(get_combs({"foo": [0, 1, 2]})) == set([{"foo": 0}, {"foo": 1}, {"foo": 2}])
    assert get_combs({"foo": [0, 1, 2]}) == [{"foo": 0}, {"foo": 1}, {"foo": 2}]
    # assert set(get_combs({"foo": [0, 1], "bar": ["A", "B"]})) == set([{"foo": 0, "bar": "A"}, {"foo": 1, "bar": "A"}, {"foo": 0, "bar": "B"}, {"foo": 1, "bar": "B"}])  # order irrelevant
    assert len(get_combs({"foo": [0, 1], "bar": ["A", "B"]})) == 4
    assert len(get_combs({"foo": [0, 1], "bar": ["A", "B"]})[0].items()) == 2


def test_task_graph():
    names = ["NodeA", "NodeB", "NodeC"]
    dependencies = {"NodeA": [], "NodeB": ["foo", "bar"], "NodeC": ["foo"]}
    providers = {"foo": "NodeA", "bar": "NodeC"}
    task_graph = TaskGraph(names, dependencies, providers)
    nodes, edges = task_graph.get_graph()
    print("nodes", nodes)
    print("edges", edges)
    assert len(nodes) == len(names)
    assert len(edges) == sum([len(deps) for deps in dependencies.values()])
    order = task_graph.get_order()
    assert len(order) == len(nodes)
    assert order.index("NodeB") > order.index("NodeA") and order.index("NodeB") > order.index("NodeC")
    assert order.index("NodeC") > order.index("NodeA")

