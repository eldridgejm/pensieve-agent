Feature: Listing the repositories

    Scenario: A non-empty pensieve.
        Given the pensieve has repos "foo", "bar", "baz".
        When the agent receives
            """
            {"command": "list", "data": {}}
            """
        Then the agent responds with JSON equal to
            """
            {
                "error": {"code": 0, "msg": "All good!"},
                "data": ["bar", "baz", "foo"]
            }
            """
