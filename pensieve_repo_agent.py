import collections
import functools
import json
import pathlib
import subprocess
import sys


class PensieveError(Exception):
    """A general pensieve exception."""
    code = 1


class RepositoryExistsError(PensieveError):
    """A repository already exists with that name."""
    code = 2

    def __init__(self, name):
        self.name = name

    def __str__(self):
        s = 'A repository already exists with the name "{}".'.format(self.name)
        return s


class InvalidCommandError(PensieveError):
    """The command is not valid."""
    code = 3

    def __init__(self, command):
        self.command = command

    def __str__(self):
        s = 'The request includes an invalid command: "{}".'
        return s.format(self.command)


class InvalidInputError(PensieveError):
    """The input is not valid."""
    code = 4


# SERIALIZATION ###############################################################


def dispatch_request(request, pensieve_path, commands):
    """Translate the request into a function call."""
    try:
        cmd = commands[request['command']]
    except KeyError:
        raise InvalidCommandError(request['command'])

    return cmd(pensieve_path, **request['data'])


def deserialize_json_request(fileobj):
    try:
        request = json.load(fileobj)
    except json.JSONDecodeError:
        raise InvalidInputError('Invalid input given.')

    required = ['command', 'data']
    for field in required:
        if field not in request:
            raise InvalidInputError('Input missing field: "{}".'.format(field))

    return request


# COMMANDS ####################################################################


def cmd_list(pensieve_path):
    """List the names of the repositories in the pensieve."""
    names = []
    for entry in pensieve_path.iterdir():
        if entry.is_dir():
            names.append(entry.name)

    return names


def cmd_new(pensieve_path, name):
    repo_path = pensieve_path / name

    try:
        repo_path.mkdir()
    except FileExistsError:
        raise RepositoryExistsError(name)

    command = ['git', 'init', '--bare', 'repo.git']
    subprocess.run(command, cwd=str(repo_path))


# MAIN ########################################################################


COMMANDS = {
    'list': cmd_list,
    'new': cmd_new
    }


def main(cwd=None, receive=None, send=None, dispatch=None, commands=None):
    """Read and process the request and present the result."""

    if cwd is None:
        cwd = pathlib.Path.cwd()

    if receive is None:
        receive = functools.partial(deserialize_json_request, sys.stdin)

    if send is None:
        send = functools.partial(json.dump, fp=sys.stdout)

    if dispatch is None:
        dispatch = dispatch_request

    if commands is None:
        commands = COMMANDS

    try:
        request = receive()
        result = dispatch(request, cwd, commands)
    except PensieveError as exc:
        error = {'code': exc.code, 'msg': str(exc)}
        result = None
    else:
        error = {'code': 0, 'msg': 'All good!'}

    response = {'error': error, 'data': result}
    send(response)


if __name__ == '__main__':
    main()
