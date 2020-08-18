import json
import pathlib
import subprocess
import tempfile


@given('the pensieve has repos {repos} with topics')
def step_impl(context, repos):
    context.repo_names = [name.strip() for name in repos.split(',')]
    context.tempdir = tempfile.TemporaryDirectory()
    context.all_topics = json.loads(context.text)

    context.path = pathlib.Path(context.tempdir.name)
    for name in context.repo_names:
        path = context.path / name.strip('"')
        path.mkdir()
        with (path / 'topics').open('w') as fileobj:
            for tag in context.all_topics[name.strip('"')]:
                fileobj.write(tag.strip('"') + '\n')


@when('the agent receives')
def step_impl(context):
    context.proc = subprocess.run(
        ['_pensieve-agent'], input=context.text.encode(), 
        cwd=context.tempdir.name, stdout=subprocess.PIPE)


@then('the agent responds with JSON equal to')
def step_impl(context):
    result = json.loads(context.proc.stdout.decode())
    expected = json.loads(context.text)
    assert result == expected, (str(result), str(expected))


@then('the pensieve has repo "{name}".')
def step_impl(context, name):
    assert (context.path / name).is_dir()
