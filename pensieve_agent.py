"""An interface to a standardized collection of git repositories."""
import functools
import json
import pathlib
import subprocess
import sys


META_FILE_NAME = 'meta.json'


class PensieveAgentError(Exception):
    """General pensieve_repo_agent error."""
    code = 1


class InvalidCommandError(PensieveAgentError):
    code = 2

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '"{}" is not a valid command.'.format(self.name)


class InvalidDataError(PensieveAgentError):
    code = 3
    
    def __init__(self, command, data):
        self.command = command
        self.data = data

    def __str__(self):
        s = 'Invalid data "{}" for command "{}".'
        return s.format(self.data, self.command)


class MalformedMessageError(PensieveAgentError):
    code = 4

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'The message "{}" is malformed.'.format(self.message)


class DuplicateNameError(PensieveAgentError):
    code = 5

    def __init__(self, name):
        self.name = name

    def __str__(self):
        s = 'The pensieve already contains a repository with name "{}".'
        return s.format(self.name)


class InvalidNameError(PensieveAgentError):
    code = 6

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return (
            'The name "{}" could not be created. It may contain invalid '
            'characters.'
            ).format(self.name)


def _initialize_git_repository(path):
    cmd = ['git', 'init', '--bare', 'repo.git']
    subprocess.run(cmd, cwd=str(path), stdout=subprocess.PIPE)


class Commands(object):

    def __init__(self, path):
        self.path = path

    def list(self):
        """Return metadata about the repositories."""
        meta = {}
        for subdir in self.path.iterdir():
            with (subdir / META_FILE_NAME).open() as fileobj:
                meta[subdir.name] = json.load(fileobj)
        return meta

    def new(self, name, description=None, topics=None):
        repo_path = self.path / name
        try:
            repo_path.mkdir()
        except FileExistsError:
            raise DuplicateNameError(name)
        except PermissionError:
            raise InvalidNameError(name)

        meta = {
            'description': description,
            'topics': [] if topics is None else topics
        }

        with (repo_path / META_FILE_NAME).open('w') as fileobj:
            json.dump(meta, fileobj)

        _initialize_git_repository(repo_path)


def _invoke(commands, name, data):
    try:
        command = getattr(commands, name)
    except AttributeError:
        raise InvalidCommandError(name)

    try:
        return command(**data)
    except TypeError:
        raise InvalidDataError(name, data)


def _unpack(message):
    try:
        return message['command'], message['data']
    except (TypeError, KeyError):
        raise MalformedMessageError(message)


def route(receive, send, commands):
    """Route messages to the proper command and send the response."""

    try:
        message = receive()
        command, data = _unpack(message)
        result = _invoke(commands, command, data)
    except PensieveAgentError as exc:
        error = {'code': exc.code, 'msg': str(exc)}
        result = None
    else:
        error = {'code': 0, 'msg': 'All good!'}

    send({
        'error': error,
        'data': result
    })


def main():
    """Wire together the interface."""
    receive_json_from_stdin = functools.partial(json.load, sys.stdin)
    send_json_to_stdout = functools.partial(json.dump, fp=sys.stdout) 

    commands = Commands(pathlib.Path.cwd())

    route(receive_json_from_stdin, send_json_to_stdout, commands)

if __name__ == '__main__':
    main()
