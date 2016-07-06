import functools
import pathlib
import json
import sys


def cmd_ls():
    names = []
    for path in pathlib.Path.cwd().iterdir():
        names.append(path.name)

    response = {
        'error': {
            'code': 0,
            'msg': 'All good!'
            },
        'data': sorted(names)
        }

    print(json.dumps(response))


class Commands(object):

    def __init__(self, path):
        self.path = path

    def list(self):
        """List the folder names under the path."""
        names = []
        for subdir in self.path.iterdir():
            names.append(subdir.name)
        return sorted(names)


def route(receive, send, commands):
    """Route messages to the proper command and send the response."""
    message = receive()
    command = getattr(commands, message['command'])
    response = command(**message['data'])
    send(response)


def main():
    """Wire together the interface."""
    receive_json_from_stdin = functools.partial(json.load, sys.stdin)
    send_json_to_stdout = functools.partial(json.dump, fp=sys.stdout) 

    commands = Commands(pathlib.Path.cwd())

    route(receive_json_from_stdin, send_json_to_stdout, commands)

if __name__ == '__main__':
    main()
