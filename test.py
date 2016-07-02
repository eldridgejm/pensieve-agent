import io
import json
import pathlib
from unittest.mock import Mock

import pytest

import pensieve_repo_agent


NAMES = ['foo', 'bar', 'baz']


@pytest.fixture
def pensieve(tmpdir):
    path = pathlib.Path(str(tmpdir))

    for repo in NAMES:
        (path / repo).mkdir()

    return path


# dispatch_request ############################################################


def test_distpatch_request_routes_correctly():
    request = {
        'command': 'foobar',
        'data': {}
        }

    pensieve_path = Mock()
    commands = {
        'foobar': Mock()
        }

    pensieve_repo_agent.dispatch_request(request, pensieve_path, commands)
    commands['foobar'].assert_called_once_with(pensieve_path)


def test_dispatch_request_raises_on_invalid_command():
    request = {
        'command': 'foo',
        'data': {}
        }

    pensieve_path = Mock()
    commands = {}

    with pytest.raises(pensieve_repo_agent.InvalidCommandError):
        pensieve_repo_agent.dispatch_request(request, pensieve_path, commands)


# deserialize_json_request ####################################################


def test_deserialize_json_request_raises_on_invalid_json():
    s = io.StringIO('[[')
    with pytest.raises(pensieve_repo_agent.InvalidInputError):
        pensieve_repo_agent.deserialize_json_request(s)


# cmd_list ####################################################################


def test_cmd_list_produces_names(pensieve):
    res = pensieve_repo_agent.cmd_list(pensieve)
    assert set(res) == set(NAMES)


# cmd_new #####################################################################


def test_cmd_new_creates_git_repository(pensieve):
    pensieve_repo_agent.cmd_new(pensieve, 'testing')
    assert (pensieve / 'testing' / 'repo.git').is_dir()


def test_cmd_new_duplicate_raises_repo_exists_error(pensieve):
    with pytest.raises(pensieve_repo_agent.RepositoryExistsError):
        pensieve_repo_agent.cmd_new(pensieve, 'foo')
