import json
import pathlib
import subprocess
import tempfile


@given('the pensieve has repos {repos}.')
def step_impl(context, repos):
    context.repo_names = [name.strip() for name in repos.split(',')]
    context.tempdir = tempfile.TemporaryDirectory()

    root = pathlib.Path(context.tempdir.name)
    for name in context.repo_names:
        (root / name).mkdir()


@when('the agent receives')
def step_impl(context):
    context.proc = subprocess.run(
        ['pensieve-repo-agent'], input=context.text.encode(), 
        cwd=context.tempdir.name, stdout=subprocess.PIPE)


@then('the agent responds with JSON equal to')
def step_impl(context):
    result = json.loads(context.proc.stdout.decode())
    expected = json.loads(context.text)
    assert result == expected, (str(result), str(expected))