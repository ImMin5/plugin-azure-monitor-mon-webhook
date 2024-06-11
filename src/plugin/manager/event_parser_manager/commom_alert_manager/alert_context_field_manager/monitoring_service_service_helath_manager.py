from plugin.manager.event_parser_manager.commom_alert_manager.monitor_alert_schema_manager import (
    MonitorAlertSchemaManager,
)


class ServiceHealthManager(MonitorAlertSchemaManager):
    monitoring_service = "ServiceHealth"

    def event_parse(self, options: dict, data: dict) -> list:
        essentials: dict = data.get("essentials")
        alert_context: dict = data.get("alertContext")
        response = {
            "event_key": essentials.get("alertId"),
            "event_type": self.get_event_status(essentials.get("monitorCondition")),
            "title": alert_context.get("properties").get("title"),
            "description": essentials.get("description"),
            "severity": self.get_severity(essentials.get("severity", "")),
            "resource": self.get_resource_info(essentials),
            "rule": essentials.get("alertRule"),
            "occurred_at": essentials.get("firedDateTime"),
            "additional_info": alert_context,
        }

        return [response]
