from datetime import datetime
import os
from typing import Dict, Tuple
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand


class QueryBuilder:
    async def __format_params(self, key, value):
        if key in ["subject", "content", "receivers", "attachments_keyword"]:
            return f"%{value}%"
        elif isinstance(value, datetime):
            return value.isoformat()
        return value

    async def build_query(
        self, command: FilterEmailCommand
    ) -> Tuple[str, Dict[str, str]]:
        try:
            conditions = {
                "email_id": "email_id = @email_id",
                "is_sent": "is_sent = @is_sent",
                "request_time_start": "request_time >= @request_time_start",
                "request_time_end": "request_time <= @request_time_end",
                "sent_time_start": "sent_time >= @sent_time_start",
                "sent_time_end": "sent_time <= @sent_time_end",
                "receivers": "receivers LIKE @receivers",
                "subject": "subject LIKE @subject",
                "content": "content LIKE @content",
                "attachments_keyword": "attachments LIKE @attachments_keyword",
            }
            query_conditions = [
                conditions[key]
                for key in conditions
                if getattr(command, key, None) is not None
            ]
            view = os.getenv("GCP_BIG_QUERY_VIEW")
            query = f"SELECT * FROM `{view}`"
            if query_conditions:
                query += " WHERE " + " AND ".join(query_conditions)

            params = {
                key: await self.__format_params(key, getattr(command, key))
                for key in conditions
                if getattr(command, key, None) is not None
            }
            return query, params
        except Exception as error:
            raise FailedToBuildQuery(error)


class FailedToBuildQuery(Exception):
    def __init__(self, error):
        self.error = error
        self.message = f"Failed to build query. Error: {error}"
        super().__init__(self.message)
