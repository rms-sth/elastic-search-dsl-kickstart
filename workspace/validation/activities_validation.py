import json
from datetime import datetime

from cerberus import Validator


data_path = './data/activities_data.json'

with open(data_path) as json_file:
    data = json.load(json_file)

activities_schema = {
    "workspace": {
        "type": "dict",
        "schema": {
            "id": {
                "type": "string"
            },
            "name": {
                "type": "string"
            }
        }
    },
    "user": {
        "type": "dict",
        "schema": {
            "id": {
                "type": "string"
            },
            "name": {
                "type": "string"
            }
        }
    },
    "message": {
        "type": "string"
    },
    "action": {
        "type": "string"
    },
    "source": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                }
            }
        }
    },
    "tags": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "tag": {
                    "type": "string"
                },
                "type": {
                    "type": "string"
                },
                "weight": {
                    "type": "string"
                }
            }
        }
    },
    "created_at": {
        "type": "datetime",
        'coerce': datetime.fromisoformat
    },
    "updated_at": {
        "type": "datetime",
        'coerce': datetime.fromisoformat
    },
    "created_by": {
        "type": "dict",
        "schema": {
            "id": {
                "type": "string"
            },
            "name": {
                "type": "string"
            }
        }
    },
    "references": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "vault": {
                    "type": "dict",
                    "schema": {
                        "name": {
                            "type": "string"
                        }
                    }
                },
                "app": {
                    "type": "dict",
                    "schema": {
                        "id": {
                            "type": "string"
                        },
                        "type": {
                            "type": "string"
                        }
                    }
                },
                "object": {
                    "type": "dict",
                    "schema": {
                        "id": {
                            "type": "string"
                        },
                        "type": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}


v = Validator(activities_schema)
print(v.validate(data))
