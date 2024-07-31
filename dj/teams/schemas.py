SCHEMA_TEAM = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "members": {
            "type": "array"
        },
        "id": {
            "type": "number"
        },
        "name": {
            "type": "string"
        },
        "tag": {
            "type": "string"
        },
        "isProfessional": {
            "type": "boolean"
        },
        "logo": {
            "type": "string"
        },
        "bannerLogo": {
            "type": "string"
        },
        "winCount": {
            "type": "number"
        },
        "lossCount": {
            "type": "number"
        },
        "lastMatchDateTime": {
            "type": "number"
        },
        "isFollowed": {
            "type": "boolean"
        },
        "countryName": {
            "type": "string"
        }
    },
    "required": [
        "id",
        "name"
    ]
}
