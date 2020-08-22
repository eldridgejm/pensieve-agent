import json
import pathlib
import subprocess
import tempfile


def process_name_list(names):
    """Process a string like "foo, bar, baz" into a list of strings."""
    return [n.strip().strip('"') for n in names.split(",")]


@given("the store has repos {repos} with metadata")
def step_impl(context, repos):
    meta = json.loads(context.text.strip())
    context.tempdir = tempfile.TemporaryDirectory()
    context.path = pathlib.Path(context.tempdir.name)
    for name in process_name_list(repos):
        path = context.path / name
        path.mkdir()
        with (path / "meta.json").open("w") as fileobj:
            json.dump(meta[name], fileobj)


@when("the agent receives")
def step_impl(context):
    context.proc = subprocess.run(
        ["_pensieve-agent"],
        input=context.text.encode(),
        cwd=context.tempdir.name,
        stdout=subprocess.PIPE,
    )


@then("the agent responds with JSON equal to")
def step_impl(context):
    result = json.loads(context.proc.stdout.decode())
    expected = json.loads(context.text)
    assert result == expected, (str(result), str(expected))


@then('the pensieve has repo "{name}".')
def step_impl(context, name):
    assert (context.path / name).is_dir()


@then('the pensieve has repo "{name}" with metadata')
def step_impl(context, name):
    assert (context.path / name).is_dir(), f"{context.path / name} does not exist."
    with (context.path / name / "meta.json").open() as fileobj:
        actual_meta = json.load(fileobj)
    expected_meta = json.loads(context.text)
    assert actual_meta == expected_meta, (str(actual_meta), str(expected_meta))
