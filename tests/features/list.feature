Feature: Listing the repositories

    Scenario: A non-empty pensieve.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"tags": ["research"], "description": "This is foo."},
            "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
            "baz": {"tags": [], "description": null}
            }
            """
        When the agent receives
            """
            {"command": "list", "data": {}}
            """
        Then the agent responds with JSON equal to
            """
            {
                "error": {"code": 0, "msg": "All good!"},
                "data":
                    {
                    "foo": {"tags": ["research"], "description": "This is foo."},
                    "bar": {"tags": ["teaching", "research"], "description": "This is bar."},
                    "baz": {"tags": [], "description": null}
                    }
            }
            """
