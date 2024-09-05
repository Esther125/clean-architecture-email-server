
CREATE OR REPLACE VIEW `tw-rd-de-milecoolab-dev.firestore_export.email_data_view` AS
SELECT 
  JSON_EXTRACT_SCALAR(data, '$.email_id') AS email_id,
  JSON_EXTRACT_SCALAR(data, '$.is_sent') AS is_sent,
  FORMAT_TIMESTAMP('%F %T', TIMESTAMP_SECONDS(CAST(JSON_EXTRACT_SCALAR(data, '$.request_time._seconds') AS INT64)), 'Asia/Hong_Kong') AS request_time,
  FORMAT_TIMESTAMP('%F %T', TIMESTAMP_SECONDS(CAST(JSON_EXTRACT_SCALAR(data, '$.sent_time._seconds') AS INT64)), 'Asia/Hong_Kong') AS sent_time,
  ARRAY(
    SELECT JSON_EXTRACT_SCALAR(x) 
    FROM UNNEST(JSON_EXTRACT_ARRAY(data, '$.receivers')) x
  ) AS receivers,
  JSON_EXTRACT_SCALAR(data, '$.subject') AS subject,
  JSON_EXTRACT_SCALAR(data, '$.content') AS content,
  STRUCT(
    JSON_EXTRACT_SCALAR(data, '$.attachments.blobname') AS blobname,
    JSON_EXTRACT_SCALAR(data, '$.attachments.filename') AS filename,
    JSON_EXTRACT_SCALAR(data, '$.attachments.filetype') AS filetype
  ) AS attachments,
FROM `tw-rd-de-milecoolab-dev.firestore_export.email_raw_latest`;
