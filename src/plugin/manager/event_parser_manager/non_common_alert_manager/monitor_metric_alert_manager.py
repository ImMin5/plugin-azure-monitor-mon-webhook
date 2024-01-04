import json
from typing import List
from plugin.manager.event_parser_manager.base_manager import EventParserManager


class MonitorMetricAlertManager(EventParserManager):
    schema_id = "AzureMonitorMetricAlert"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:
        context = data.get("context")

        response = {
            "event_key": context.get('id'),
            "event_type": self.get_event_status(data.get("status")),
            "title": context.get("name"),
            "description": self.make_description(context.get("description"),
                                                 context.get("condition", {}).get("allOf", [])),
            "severity": self.get_severity(context.get("severity", "")),
            "resource": self.get_resource_info(context),
            "rule": context.get("name"),
            "image_url": context.get("portalLink", ""),
            "occurred_at": context.get("timestamp"),
            "additional_info": data.get("properties", {}),
        }
        return [response]

    @staticmethod
    def make_description(description:str, all_of: List[dict]) -> str:
        tmp_description = json.dumps(all_of, indent=2)

        return f"Description: {description}\n{tmp_description}"

    @staticmethod
    def get_event_status(status: str) -> str:
        """

        Args:
            status:
            - Deactivated
            - Activated
        Returns:
            - ALERT
            - RECOVERY
        """
        if status == "Deactivated":
            return "RECOVERY"
        else:
            return "ALERT"

    @staticmethod
    def get_resource_info(context: dict) -> dict:
        resource_info = {}

        if resource_id := context.get("resourceId"):
            resource_info["resource_id"] = resource_id

        if resource_name := context.get("resourceName"):
            resource_info["name"] = resource_name

        if resource_type := context.get("resourceType"):
            resource_info["resource_type"] = resource_type

        return resource_info

    @staticmethod
    def _get_resource_type_from_resource_id(resource_id: str) -> str:
        return resource_id.split("/")[5]

    @staticmethod
    def get_severity(origin_severity: str) -> str:
        if origin_severity.lower() == "0":
            return "CRITICAL"
        elif origin_severity.lower() == "1":
            return "ERROR"
        elif origin_severity.lower() == "2":
            return "WARNING"
        elif origin_severity.lower() == "3":
            return "INFO"
        elif origin_severity.lower() == "4":
            return "NONE"
        else:
            return "UNKNOWN"
