import pathlib
from unittest.mock import Mock

import pytest
from pytest import fixture

import pensieve_repo_agent


_NAMES = [
    ['foo', 'bar', 'baz'],
    []
]


@fixture(params=_NAMES)
def names(request):
    return request.param


@fixture
def pensieve(tmpdir, names):
    path = pathlib.Path(str(tmpdir))
    for name in names:
        (path / name).mkdir()
    return path


# test route ##################################################################


MESSAGE = {
    'command': 'foo',
    'data': {
        'key': 'value'
        }
    }

def test_route_invokes_command_with_data():
    receive = Mock(return_value=MESSAGE)
    send = Mock()
    commands = Mock()

    pensieve_repo_agent.route(receive, send, commands)
    commands.foo.assert_called_once_with(**MESSAGE['data'])


def test_route_sends_message_with_error_data():
    receive = Mock(return_value=MESSAGE)
    send = Mock()
    commands = Mock()
    commands.foo.return_value = 'hello'

    pensieve_repo_agent.route(receive, send, commands)
    send.assert_called_once_with({
        'error': {
            'code': 0,
            'msg': 'All good!'
            },
        'data': 'hello'
    })


def test_route_sends_correct_error_when_command_raises():
    receive = Mock(return_value=MESSAGE)
    send = Mock()
    commands = Mock()
    commands.foo.side_effect = pensieve_repo_agent.PensieveAgentError('test')

    pensieve_repo_agent.route(receive, send, commands)
    send.assert_called_once_with({
        'error': {
            'code': 1,
            'msg': 'test'
            },
        'data': None
    })


def test_route_sends_error_when_invalid_command_given():
    receive = Mock(return_value=MESSAGE)
    send = Mock()
    commands = object()

    pensieve_repo_agent.route(receive, send, commands)
    exc = pensieve_repo_agent.InvalidCommandError('foo')
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


def test_route_sends_error_when_invalid_data_given():
    receive = Mock(return_value=MESSAGE)
    send = Mock()

    class Commands(object):

        def foo(self, only_argument):
            pass

    commands = Commands()

    pensieve_repo_agent.route(receive, send, commands)
    exc = pensieve_repo_agent.InvalidDataError('foo', MESSAGE['data'])
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


def test_route_sends_error_when_receive_raises():
    exc = pensieve_repo_agent.PensieveAgentError('test')
    receive = Mock(side_effect=exc)
    send = Mock()
    commands = Mock()

    pensieve_repo_agent.route(receive, send, commands)
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


def test_route_sends_error_when_message_is_malformed():
    receive = Mock(return_value=42)
    send = Mock()
    commands = Mock()

    pensieve_repo_agent.route(receive, send, commands)
    exc = pensieve_repo_agent.MalformedMessageError(42)
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


def test_route_sends_error_when_message_has_no_command():
    msg = MESSAGE.copy()
    del msg['command']

    receive = Mock(return_value=msg)
    send = Mock()
    commands = Mock()

    pensieve_repo_agent.route(receive, send, commands)
    exc = pensieve_repo_agent.MalformedMessageError(msg)
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


def test_route_sends_error_when_message_has_no_data():
    msg = MESSAGE.copy()
    del msg['data']

    receive = Mock(return_value=msg)
    send = Mock()
    commands = Mock()

    pensieve_repo_agent.route(receive, send, commands)
    exc = pensieve_repo_agent.MalformedMessageError(msg)
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


# test list command ###########################################################


def test_list_command_sorts_alphabetically(pensieve, names):
    commands = pensieve_repo_agent.Commands(pensieve)
    result = commands.list()
    assert result == sorted(names)
