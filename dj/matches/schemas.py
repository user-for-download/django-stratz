SCHEMA_OPENDOTA_TEAM_LIST = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "command": {
            "type": "string"
        },
        "rowCount": {
            "type": "number"
        },
        "oid": {},
        "rows": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "team_id": {
                        "type": "number"
                    },
                    "name": {
                        "type": "string"
                    },
                    "tag": {
                        "type": "string"
                    },
                    "logo_url": {
                        "type": "string"
                    },
                    "rating": {
                        "type": "number"
                    },
                    "wins": {
                        "type": "number"
                    },
                    "losses": {
                        "type": "number"
                    },
                    "last_match_time": {
                        "type": "number"
                    },
                    "matches_ids": {
                        "type": "string"
                    }
                },
                "required": [
                    "team_id",
                    "name",
                ]
            }
        },
    },
    "required": [
        "rows",
    ]
}
