Feature: Creating a new repository

    Scenario: A repo with a unique name is created in a non-empty pensieve.
        Given the pensieve has repos "foo", "bar", "baz" with topics
            """
            {
                "foo": [],
                "bar": [],
                "baz": []
            }
            """
        When the agent receives
            """
            {"command": "new", "data": {"name": "testing"}}
            """
        Then the pensieve has repo "testing".
        And the agent responds with JSON equal to
            """
            {
                "error": {"code": 0, "msg": "All good!"},
                "data": null
            }
            """

    Scenario: A repo is created with a duplicate name.
        Given the pensieve has repos "foo", "bar", "baz" with topics
            """
            {
                "foo": [],
                "bar": [],
                "baz": []
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
        Given the pensieve has repos "foo", "bar", "baz" with topics
            """
            {
                "foo": [],
                "bar": [],
                "baz": []
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
