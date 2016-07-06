import pathlib
import json


def main():
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


if __name__ == '__main__':
    main()
