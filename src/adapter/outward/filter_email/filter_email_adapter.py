from asyncio import to_thread
import json
from dotenv import load_dotenv
from typing import List
from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob
from src.adapter.outward.filter_email.query_builder import QueryBuilder
from src.app.domain.entity.email import Attachment, Email
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand
from src.app.port.outward.filter_email.filter_email_port import FilterEmailPort


load_dotenv()


class FilterEmailAdapter(FilterEmailPort):
    def __init__(self):
        self.client = bigquery.Client()
        self.query_builder = QueryBuilder()

    async def __generate_result_emails(self, rows: List[dict]) -> List[Email]:
        result_emails = []
        for row in rows:
            receivers_list = json.loads(row["receivers"])
            attachments_list = json.loads(row["attachments"])
            result_emails.append(
                Email(
                    email_id=row["email_id"],
                    is_sent=row["is_sent"],
                    request_time=row["request_time"],
                    sent_time=row["sent_time"],
                    receivers=[receiver for receiver in receivers_list],
                    subject=row["subject"],
                    content=row["content"],
                    attachments=[
                        Attachment(
                            filename=attachment["filename"],
                            filetype=attachment["filetype"],
                            blobname=attachment["blobname"],
                        )
                        for attachment in attachments_list
                    ],
                )
            )
        return result_emails

    async def async_query(self, query, query_job_config) -> QueryJob:
        return await to_thread(self.client.query, query, job_config=query_job_config)

    async def filter_email(self, command: FilterEmailCommand) -> List[Email]:
        try:
            query, params = await self.query_builder.build_query(command)
            query_job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(key, "STRING", params[key])
                    for key in params
                ]
            )
            query_job = await self.async_query(query, query_job_config)
            rows = list(query_job.result())
            result_emails = await self.__generate_result_emails(rows)
            return result_emails
        except Exception as error:
            raise FailedToFilterEmailError(error)


class FailedToFilterEmailError(Exception):
    def __init__(self, error) -> None:
        self.error = error
        self.message = f"Failed to filter emails. Error: {error}"
        super().__init__(self.message)
