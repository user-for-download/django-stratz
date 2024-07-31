SCHEMA_PLAYER = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "isFollowed": {
            "type": "boolean"
        },
        "steamAccount": {
            "type": "object",
            "properties": {
                "avatar": {
                    "type": "string"
                },
                "countryCode": {
                    "type": "string"
                },
                "dotaAccountLevel": {
                    "type": "number"
                },
                "dotaPlusOriginalStartDate": {
                    "type": "number"
                },
                "id": {
                    "type": "number"
                },
                "isAnonymous": {
                    "type": "boolean"
                },
                "isDotaPlusSubscriber": {
                    "type": "boolean"
                },
                "isStratzPublic": {
                    "type": "boolean"
                },
                "name": {
                    "type": "string"
                },
                "profileUri": {
                    "type": "string"
                },
                "proSteamAccount": {
                    "type": "object",
                },
                "rankShift": {
                    "type": "number"
                },
                "realName": {
                    "type": "string"
                },
                "seasonLeaderboardDivisionId": {
                    "type": "number"
                },
                "seasonLeaderboardRank": {
                    "type": "number"
                },
                "seasonRank": {
                    "type": "number"
                },
                "smurfCheckDate": {
                    "type": "number"
                },
                "smurfFlag": {
                    "type": "number"
                },
                "stateCode": {
                    "type": "string"
                }
            },
            "required": [
                "id",
            ]
        },
        "steamAccountId": {
            "type": "number"
        }
    },
    "required": [
        "steamAccount",
        "steamAccountId"
    ]
}


SCHEMA_PLAYERS = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "steamAccount": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number"
                },
                "lastActiveTime": {
                    "type": "string"
                },
                "profileUri": {
                    "type": "string"
                },
                "realName": {
                    "type": "string"
                },
                "timeCreated": {
                    "type": "number"
                },
                "countryCode": {
                    "type": "string"
                },
                "cityId": {
                    "type": "number"
                },
                "communityVisibleState": {
                    "type": "number"
                },
                "name": {
                    "type": "string"
                },
                "avatar": {
                    "type": "string"
                },
                "primaryClanId": {
                    "type": "number"
                },
                "isDotaPlusSubscriber": {
                    "type": "boolean"
                },
                "dotaPlusOriginalStartDate": {
                    "type": "number"
                },
                "isAnonymous": {
                    "type": "boolean"
                },
                "isStratzPublic": {
                    "type": "boolean"
                },
                "seasonRank": {
                    "type": "number"
                },
                "seasonLeaderboardRank": {
                    "type": "number"
                },
                "seasonLeaderboardDivisionId": {
                    "type": "number"
                },
                "proSteamAccount": {
                    "type": "object",
                    "properties": {
                        "steamAccountId": {
                            "type": "number"
                        },
                        "name": {
                            "type": "string"
                        },
                        "realName": {
                            "type": "string"
                        },
                        "fantasyRole": {
                            "type": "number"
                        },
                        "teamId": {
                            "type": "number"
                        },
                        "sponsor": {
                            "type": "string"
                        },
                        "isLocked": {
                            "type": "boolean"
                        },
                        "isPro": {
                            "type": "boolean"
                        },
                        "totalEarnings": {
                            "type": "number"
                        },
                        "romanizedRealName": {
                            "type": "string"
                        },
                        "roles": {
                            "type": "number"
                        },
                        "statuses": {
                            "type": "number"
                        },
                        "twitchLink": {
                            "type": "string"
                        },
                        "instagramLink": {
                            "type": "string"
                        },
                        "vkLink": {
                            "type": "string"
                        },
                        "signatureheroes": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "countries": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "tiWins": {
                            "type": "number"
                        },
                        "istiwinner": {
                            "type": "boolean"
                        },
                        "position": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "steamAccountId",
                        "name"
                    ],
                },
                "smurfFlag": {
                    "type": "number"
                },
                "smurfCheckDate": {
                    "type": "number"
                },
                "lastMatchDateTime": {
                    "type": "number"
                },
                "lastMatchRegionId": {
                    "type": "number"
                },
                "dotaAccountLevel": {
                    "type": "number"
                }
            },
            "required": [
                "id"
            ]
        },
        "battlePass": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "eventId": {
                        "type": "number"
                    },
                    "level": {
                        "type": "number"
                    },
                    "bracket": {
                        "type": "number"
                    },
                    "isAnonymous": {
                        "type": "boolean"
                    }
                },
            }
        },
        "date": {
            "type": "number"
        },
        "badges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "steamId": {
                        "type": "number"
                    },
                    "badgeId": {
                        "type": "number"
                    },
                    "createdDateTime": {
                        "type": "string"
                    }
                },
            }
        },
        "lastRegionId": {
            "type": "number"
        },
        "ranks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "seasonRankId": {
                        "type": "number"
                    },
                    "asOfDateTime": {
                        "type": "string"
                    },
                    "isCore": {
                        "type": "boolean"
                    },
                    "rank": {
                        "type": "number"
                    }
                },
            }
        },
        "languageCode": {
            "type": "array",
            "items": {}
        },
        "firstMatchDate": {
            "type": "number"
        },
        "matchCount": {
            "type": "number"
        },
        "winCount": {
            "type": "number"
        },
        "names": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "lastseendatetime": {
                        "type": "number"
                    }
                },
                "required": [
                    "name",
                ]
            }
        },
        "team": {
            "type": "object",
            "properties": {
                "teamId": {
                    "type": "number"
                },
                "firstMatchId": {
                    "type": "number"
                },
                "firstMatchDateTime": {
                    "type": "string"
                },
                "lastMatchId": {
                    "type": "number"
                },
                "lastMatchDateTime": {
                    "type": "string"
                },
                "team": {
                    "type": "object",
                    "properties": {
                        "members": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "teamId": {
                                        "type": "number"
                                    },
                                    "firstMatchId": {
                                        "type": "number"
                                    },
                                    "firstMatchDateTime": {
                                        "type": "string"
                                    },
                                    "lastMatchId": {
                                        "type": "number"
                                    },
                                    "lastMatchDateTime": {
                                        "type": "string"
                                    },
                                    "steamAccount": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "type": "number"
                                            },
                                            "profileUri": {
                                                "type": "string"
                                            },
                                            "realName": {
                                                "type": "string"
                                            },
                                            "countryCode": {
                                                "type": "string"
                                            },
                                            "stateCode": {
                                                "type": "string"
                                            },
                                            "name": {
                                                "type": "string"
                                            },
                                            "avatar": {
                                                "type": "string"
                                            },
                                            "isDotaPlusSubscriber": {
                                                "type": "boolean"
                                            },
                                            "dotaPlusOriginalStartDate": {
                                                "type": "number"
                                            },
                                            "isAnonymous": {
                                                "type": "boolean"
                                            },
                                            "isStratzPublic": {
                                                "type": "boolean"
                                            },
                                            "seasonRank": {
                                                "type": "number"
                                            },
                                            "seasonLeaderboardRank": {
                                                "type": "number"
                                            },
                                            "seasonLeaderboardDivisionId": {
                                                "type": "number"
                                            },
                                            "proSteamAccount": {
                                                "type": "object",
                                                "properties": {
                                                    "steamAccountId": {
                                                        "type": "number"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "realName": {
                                                        "type": "string"
                                                    },
                                                    "fantasyRole": {
                                                        "type": "number"
                                                    },
                                                    "teamId": {
                                                        "type": "number"
                                                    },
                                                    "sponsor": {
                                                        "type": "string"
                                                    },
                                                    "isLocked": {
                                                        "type": "boolean"
                                                    },
                                                    "isPro": {
                                                        "type": "boolean"
                                                    },
                                                    "totalEarnings": {
                                                        "type": "number"
                                                    },
                                                    "romanizedRealName": {
                                                        "type": "string"
                                                    },
                                                    "roles": {
                                                        "type": "number"
                                                    },
                                                    "aliases": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "string"
                                                        }
                                                    },
                                                    "statuses": {
                                                        "type": "number"
                                                    },
                                                    "twitchLink": {
                                                        "type": "string"
                                                    },
                                                    "vkLink": {
                                                        "type": "string"
                                                    },
                                                    "signatureheroes": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "string"
                                                        }
                                                    },
                                                    "countries": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "string"
                                                        }
                                                    },
                                                    "tiWins": {
                                                        "type": "number"
                                                    },
                                                    "istiwinner": {
                                                        "type": "boolean"
                                                    },
                                                    "position": {
                                                        "type": "number"
                                                    },
                                                    "instagramLink": {
                                                        "type": "string"
                                                    },
                                                    "twitterLink": {
                                                        "type": "string"
                                                    },
                                                    "youTubeLink": {
                                                        "type": "string"
                                                    }
                                                },
                                            },
                                            "smurfFlag": {
                                                "type": "number"
                                            },
                                            "smurfCheckDate": {
                                                "type": "number"
                                            },
                                            "dotaAccountLevel": {
                                                "type": "number"
                                            },
                                            "lastActiveTime": {
                                                "type": "string"
                                            },
                                            "timeCreated": {
                                                "type": "number"
                                            },
                                            "cityId": {
                                                "type": "number"
                                            },
                                            "communityVisibleState": {
                                                "type": "number"
                                            },
                                            "primaryClanId": {
                                                "type": "number"
                                            },
                                            "soloRank": {
                                                "type": "number"
                                            },
                                            "partyRank": {
                                                "type": "number"
                                            },
                                            "lastMatchDateTime": {
                                                "type": "number"
                                            },
                                            "lastMatchRegionId": {
                                                "type": "number"
                                            },
                                            "rankShift": {
                                                "type": "number"
                                            }
                                        },
                                    }
                                },
                            }
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
                }
            }
        },
        "behaviorScore": {
            "type": "number"
        },
        "steamAccountId": {
            "type": "number"
        },
        "isFollowed": {
            "type": "boolean"
        }
    },
    "required": [
        "steamAccountId",
    ]
}
