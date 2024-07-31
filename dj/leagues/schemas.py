SCHEMA_LEAGUE_LIST = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for League",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "number"
            },
            "basePrizePool": {
                "type": "number"
            },
            "tier": {
                "type": "number"
            },
            "startDateTime": {
                "type": "number"
            },
            "endDateTime": {
                "type": "number"
            },
            "tournamentUrl": {
                "type": "string"
            },
            "lastMatchDateTime": {
                "type": "number"
            },
            "prizePool": {
                "type": "number"
            },
            "displayName": {
                "type": "string"
            },
            "status": {
                "type": "number"
            },
            "description": {
                "type": "string"
            },
            "pro_circuit_points": {
                "type": "number"
            },
            "registration_period": {
                "type": "number"
            },
            "region": {
                "type": "number"
            },
            "isFollowed": {
                "type": "boolean"
            },
            "name": {
                "type": "string"
            },
            "private": {
                "type": "boolean"
            },
            "freeToSpectate": {
                "type": "boolean"
            },
            "hasLiveMatches": {
                "type": "boolean"
            },
            "imageUri": {
                "type": "string"
            },
            "city": {
                "type": "string"
            },
            "country": {
                "type": "string"
            },
            "venue": {
                "type": "string"
            }
        },
        "required": [
            "id",
            "tier",
            "startDateTime",
            "endDateTime",
            "lastMatchDateTime",
            "displayName",
        ]
    }
}
SCHEMA_LEAGUE_MATCH_LIST = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "number"
            },
            "didRadiantWin": {
                "type": "boolean"
            },
            "durationSeconds": {
                "type": "number"
            },
            "startDateTime": {
                "type": "number"
            },
            "clusterId": {
                "type": "number"
            },
            "firstBloodTime": {
                "type": "number"
            },
            "lobbyType": {
                "type": "number"
            },
            "numHumanPlayers": {
                "type": "number"
            },
            "gameMode": {
                "type": "number"
            },
            "isStats": {
                "type": "boolean"
            },
            "avgImp": {
                "type": "number"
            },
            "parsedDateTime": {
                "type": "number"
            },
            "statsDateTime": {
                "type": "number"
            },
            "leagueId": {
                "type": "number"
            },
            "radiantTeamId": {
                "type": "number"
            },
            "direTeamId": {
                "type": "number"
            },
            "seriesId": {
                "type": "number"
            },
            "gameVersionId": {
                "type": "number"
            },
            "regionId": {
                "type": "number"
            },
            "sequenceNum": {
                "type": "number"
            },
            "rank": {
                "type": "number"
            },
            "bracket": {
                "type": "number"
            },
            "endDateTime": {
                "type": "number"
            },
            "pickBans": {
                "type": "array",
            },
            "players": {
                "type": "array",
            },
            "analysisOutcome": {
                "type": "number"
            },
            "predictedOutcomeWeight": {
                "type": "number"
            },
            "bottomLaneOutcome": {
                "type": "number"
            },
            "midLaneOutcome": {
                "type": "number"
            },
            "topLaneOutcome": {
                "type": "number"
            },
            "radiantNetworthLead": {
                "type": "array",
            },
            "radiantExperienceLead": {
                "type": "array",
            },
            "radiantKills": {
                "type": "array",
            },
            "direKills": {
                "type": "array",
            },
            "towerStatus": {
                "type": "array",
            },
            "laneReport": {
                "type": "object",
                "properties": {
                    "radiant": {
                        "type": "array",
                    },
                    "dire": {
                        "type": "array",
                    }
                },
            },
            "winRates": {
                "type": "array",
            },
            "predictedWinRates": {
                "type": "array",
            },
            "towerDeaths": {
                "type": "array",
            },
            "chatEvents": {
                "type": "array",
            },
            "didRequestDownload": {
                "type": "boolean"
            }
        },
        "required": [
            "id",
            "didRequestDownload"
        ]
    }
}

SCHEMA_LEAGUE_SERIES_LIST = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "number"
            },
            "type": {
                "type": "number"
            },
            "teamOneId": {
                "type": "number"
            },
            "teamTwoId": {
                "type": "number"
            },
            "leagueId": {
                "type": "number"
            },
            "teamOneWinCount": {
                "type": "number"
            },
            "teamTwoWinCount": {
                "type": "number"
            },
            "winningTeamId": {
                "type": "number"
            },
            "matches": {
                "type": "array",
            },
            "lastMatchDate": {
                "type": "number"
            }
        },
        "required": [
            "id",
            "leagueId",
            "lastMatchDate"
        ]
    }
}
