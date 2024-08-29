import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple
from google.cloud import bigquery
from src.app.domain.entity.email import Email
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand
from src.app.port.outward.filter_email.filter_email_port import FilterEmailPort


load_dotenv()


class FilterEmailAdapter(FilterEmailPort):
    def __init__(self):
        self.client = bigquery.Client()

    async def build_query(
        self, command: FilterEmailCommand
    ) -> Tuple[str, Dict[str, str]]:
        conditions = {
            "email_id": "email_id = @email_id",
            "is_sent": "is_sent = @is_sent",
            "request_time_start": "request_time >= @request_time_start",
            "request_time_end": "request_time <= @request_time_end",
            "sent_time_start": "sent_time >= @sent_time_start",
            "sent_time_end": "sent_time <= @sent_time_end",
            "receivers": "receivers = @receivers",
            "subject": "subject LIKE @subject",
            "content": "content LIKE @content",
            "attachments_blobname": "attachments_blobname = @attachments_blobname",
        }

        query_conditions = [
            conditions[key]
            for key in conditions
            if getattr(command, key, None) is not None
        ]
        params = {
            key: f"%{getattr(command, key)}%"
            if key in ["subject", "content"]
            else getattr(command, key)
            for key in conditions
            if getattr(command, key, None) is not None
        }

        view = os.getenv("GCP_BIG_QUERY_VIEW")
        query = f"SELECT * FROM `{view}`"
        if query_conditions:
            query += " WHERE " + " AND ".join(query_conditions)

        return query, params

    async def filter_email(self, command: FilterEmailCommand) -> List[Email]:
        query, params = await self.build_query(command)
        # TODO: change hard-coded "STRING" type
        query_job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(key, "STRING", params[key])
                for key in params
            ]
        )
        query_job = self.client.query(query, job_config=query_job_config)
        rows = list(query_job.result())
        result_emails = [
            Email(
                email_id=row["email_id"],
                is_sent=row["is_sent"],
                request_time=row["request_time"],
                sent_time=row["sent_time"],
                receivers=[row["receivers"]],
                subject=row["subject"],
                content=row["content"],
                # TODO: handle attachment
            )
            for row in rows
        ]
        return result_emails


# test
# async def main():
#     command = FilterEmailCommand(
#         is_sent=True,
#     )
#     adapter = FilterEmailAdapter()
#     emails =  await adapter.filter_email(command)
#     count = 0
#     for email in emails:
#         print(email.is_sent)
#         count+=1
#     print("COUNT: ", count)

# if __name__ == "__main__":
#     asyncio.run(main())
