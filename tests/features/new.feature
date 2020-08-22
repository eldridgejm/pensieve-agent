Feature: Creating a new repository

    Scenario: A repo with a unique name is created in a non-empty pensieve.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"tags": ["research"], "description": "This is foo."},
            "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
            "baz": {"tags": [], "description": 2}
            }
            """
        When the agent receives
            """
            {"command": "new", "data": {"name": "testing"}}
            """
        Then the pensieve has repo "testing" with metadata
            """
            {
                "description": null,
                "tags": []
            }
            """
        And the agent responds with JSON equal to
            """
            {
                "error": {"code": 0, "msg": "All good!"},
                "data": null
            }
            """

    Scenario: A repo is created with a duplicate name.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"tags": ["research"], "description": "This is foo."},
            "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
            "baz": {"tags": [], "description": 2}
            }
            """
        When the agent receives
            """
            {"command": "new", "data": {"name": "foo"}}
            """
        Then the agent responds with JSON equal to
            """
            {
                "error": {
                    "code": 5, 
                    "msg": "The pensieve already contains a repository with name \"foo\"."
                    },
                "data": null
            }
            """

    Scenario: A repo is created with an invalid filesystem name.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"tags": ["research"], "description": "This is foo."},
            "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
            "baz": {"tags": [], "description": 2}
            }
            """
        When the agent receives
            """
            {"command": "new", "data": {"name": "/test"}}
            """
        Then the agent responds with JSON equal to
            """
            {
                "error": {
                    "code": 6,
                    "msg": "The name \"/test\" could not be created. It may contain invalid characters."
                    },
                "data": null
            }
            """

    Scenario: A repo is created with a description.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"tags": ["research"], "description": "This is foo."},
            "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
            "baz": {"tags": [], "description": 2}
            }
            """
        When the agent receives
            """
            {"command": "new", "data": {"name": "test", "description": "This is a test"}}
            """
        Then the pensieve has repo "test" with metadata
            """
            {
                "description": "This is a test",
                "tags": []
            }
            """

    Scenario: A repo is created with tags.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"tags": ["research"], "description": "This is foo."},
            "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
            "baz": {"tags": [], "description": 2}
            }
            """
        When the agent receives
            """
            {"command": "new", "data": {"name": "test", "tags": ["one", "two", "three"]}}
            """
        Then the pensieve has repo "test" with metadata
            """
            {
                "description": null,
                "tags": ["one", "two", "three"]
            }
            """
