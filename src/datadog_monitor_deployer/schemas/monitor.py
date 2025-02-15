"""
JSON Schema for monitor configuration validation.
"""

MONITOR_SCHEMA = {
    "type": "object",
    "required": ["monitors"],
    "properties": {
        "monitors": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "type", "query", "message"],
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "type": {
                        "type": "string",
                        "enum": [
                            "metric alert",
                            "service check",
                            "event alert",
                            "query alert",
                            "composite",
                            "log alert",
                            "process alert",
                            "trace-analytics alert",
                            "slo alert",
                            "event-v2 alert",
                            "audit alert",
                            "rum alert",
                            "ci-pipelines alert",
                            "error-tracking alert",
                        ],
                    },
                    "query": {"type": "string", "minLength": 1},
                    "message": {"type": "string", "minLength": 1},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "priority": {"type": "integer", "minimum": 1, "maximum": 5},
                    "restricted_roles": {"type": "array", "items": {"type": "string"}},
                    "options": {
                        "type": "object",
                        "properties": {
                            "notify_no_data": {"type": "boolean"},
                            "no_data_timeframe": {"type": "integer"},
                            "notify_audit": {"type": "boolean"},
                            "timeout_h": {"type": "integer"},
                            "evaluation_delay": {"type": "integer"},
                            "new_host_delay": {"type": "integer"},
                            "include_tags": {"type": "boolean"},
                            "require_full_window": {"type": "boolean"},
                            "renotify_interval": {"type": "integer"},
                            "escalation_message": {"type": "string"},
                            "thresholds": {
                                "type": "object",
                                "properties": {
                                    "critical": {"type": "number"},
                                    "warning": {"type": "number"},
                                    "ok": {"type": "number"},
                                },
                            },
                            "threshold_windows": {
                                "type": "object",
                                "properties": {
                                    "trigger_window": {"type": "string"},
                                    "recovery_window": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
        }
    },
}
