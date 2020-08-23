Feature: Listing the repositories

    Scenario: A non-empty pensieve.
        Given the store has repos "foo", "bar", "baz" with metadata
            """
            {
            "foo": {"topics": ["research"], "description": "This is foo."},
            "bar": {"topics": ["teaching", "research"], "description": "This is bar."},
            "baz": {"topics": [], "description": null}
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
                    "foo": {"topics": ["research"], "description": "This is foo."},
                    "bar": {"topics": ["teaching", "research"], "description": "This is bar."},
                    "baz": {"topics": [], "description": null}
                    }
            }
            """
