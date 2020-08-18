import pathlib
from unittest.mock import Mock

import pytest
from pytest import fixture

import pensieve_agent


_NAMES = [
    ['foo', 'bar', 'baz'],
    []
]

_TOPICS = {
    "foo": {"a", "b"},
    "bar": {"b", "c"},
    "baz": {"d"}
}


@fixture(params=_NAMES)
def names(request):
    return request.param


@fixture
def pensieve(tmpdir, names):
    path = pathlib.Path(str(tmpdir))
    for name in names:
        (path / name).mkdir()
        with (path / name / 'topics').open('w') as fileobj:
            for tag in _TOPICS[name]:
                fileobj.write(tag + '\n')
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

    pensieve_agent.route(receive, send, commands)
    commands.foo.assert_called_once_with(**MESSAGE['data'])


def test_route_sends_message_with_error_data():
    receive = Mock(return_value=MESSAGE)
    send = Mock()
    commands = Mock()
    commands.foo.return_value = 'hello'

    pensieve_agent.route(receive, send, commands)
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
    commands.foo.side_effect = pensieve_agent.PensieveAgentError('test')

    pensieve_agent.route(receive, send, commands)
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

    pensieve_agent.route(receive, send, commands)
    exc = pensieve_agent.InvalidCommandError('foo')
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

    pensieve_agent.route(receive, send, commands)
    exc = pensieve_agent.InvalidDataError('foo', MESSAGE['data'])
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


def test_route_sends_error_when_receive_raises():
    exc = pensieve_agent.PensieveAgentError('test')
    receive = Mock(side_effect=exc)
    send = Mock()
    commands = Mock()

    pensieve_agent.route(receive, send, commands)
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

    pensieve_agent.route(receive, send, commands)
    exc = pensieve_agent.MalformedMessageError(42)
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

    pensieve_agent.route(receive, send, commands)
    exc = pensieve_agent.MalformedMessageError(msg)
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

    pensieve_agent.route(receive, send, commands)
    exc = pensieve_agent.MalformedMessageError(msg)
    send.assert_called_once_with({
        'error': {
            'code': exc.code,
            'msg': str(exc)
            },
        'data': None
    })


# test list command ###########################################################


def test_list_command_sorts_alphabetically(pensieve, names):
    commands = pensieve_agent.Commands(pensieve)
    result = commands.list()
    assert result == sorted(names)


# test new command ############################################################


def test_new_command_creates_repository(pensieve):
    commands = pensieve_agent.Commands(pensieve)
    commands.new('steve')
    assert (pensieve / 'steve' / 'repo.git').is_dir()


def test_new_command_raises_when_duplicate_name_is_given(pensieve, names):
    if not names:
        return

    commands = pensieve_agent.Commands(pensieve)
    with pytest.raises(pensieve_agent.DuplicateNameError):
        commands.new(names[0])


def test_new_command_raises_when_invalid_character_in_name(pensieve):
    commands = pensieve_agent.Commands(pensieve)
    with pytest.raises(pensieve_agent.InvalidNameError):
        commands.new("/test")


# test topics command #########################################################


def test_topics_command_returns_dictionary_of_topics(pensieve, names):
    commands = pensieve_agent.Commands(pensieve)
    result = commands.topics()
    expected = {name:sorted(_TOPICS[name]) for name in names}
    assert result == expected
