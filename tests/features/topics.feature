Feature: Listing all of the topics

    Scenario: A pensieve has existing repositories with topics
        Given the pensieve has repos "foo", "bar", "baz" with topics
            """
            {
                "foo": ["one", "two"],
                "bar": ["two"],
                "baz": ["three", "four"]
            }
            """
        When the agent receives
            """
            {"command": "topics", "data": {}}
            """
        Then the agent responds with JSON equal to
            """
            {
                "error": {"code": 0, "msg": "All good!"},
                "data": {
                    "foo": ["one", "two"],
                    "bar": ["two"],
                    "baz": ["four", "three"]
                }
            }
            """
