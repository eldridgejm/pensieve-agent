pensieve-agent
==============
An interface to a standardized collection of git repositories.

Background
----------
*pensieve* is a command-line tool for managing your git repositories. It allows
one to create and query repositories hosted on GitHub, as well as on a remote
private SSH server.

*pensieve-agent* is the script that runs on the remote private server and
responds to requests made by the *pensieve* CLI. The agent does the actual work
of creating and managing repositories.

Directory Structure
-------------------

This script assumes that git repositories are organized in a particular
structure. This structure is best illustrated with an example:

```
root/
    foo/
        repo.git/
        meta.yaml
    bar/
        repo.git/
        meta.yaml
    baz/
        repo.git/
        meta.yaml
```

This demonstrates a collection of three repositories, named *foo*, *bar*, and
*baz*. Each repository has a corresponding directory under the root. The git
repository itself is stored in `repo.git`, and should be a bare repository.
Metadata about the repository is stored in `meta.yaml`, and should have the
following structure:

```
description: A short description about the repository.
topics:
    - topic1
    - topic2
```

Usage
-----

This script is not meant to be invoked by the user directly -- instead, it is
meant to be invoked by the `pensieve` CLI over SSH. 

Start the script in the directory containing the repositories.
The script reads its instructions via stdin. The input should be formatted as
JSON with two fields: the "name" of the command, and the "data" needed to
execute the command. See the source for the available commands and the data they
require.

For instance, to create a new repository named "foo", pass the following JSON:
```
{
    "command": "new",
    "data": {
        "name": "foo"
    }
}
```

The script returns its output as JSON as well. There are two fields: "code",
which contains the return code, and "msg" which contains a short description of
the result. A non-zero error code signals a problem. See the exceptions defined
at the top of the source file to learn about the different error codes.
