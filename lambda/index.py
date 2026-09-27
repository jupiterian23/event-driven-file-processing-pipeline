import json
import urllib.parse
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")

OUTPUT_BUCKET = "jupiterian23-event-pipeline-output"


def lambda_handler(event, context):
    print("Received S3 event:")
    print(json.dumps(event))

    for record in event.get("Records", []):
        input_bucket = record["s3"]["bucket"]["name"]
        object_key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        print(f"Processing file: s3://{input_bucket}/{object_key}")

        response = s3.get_object(
            Bucket=input_bucket,
            Key=object_key
        )

        file_content = response["Body"].read().decode("utf-8")
        file_size = response["ContentLength"]

        processed_at = datetime.now(timezone.utc).isoformat()

        processed_content = (
            "PROCESSED FILE\n"
            "===============\n\n"
            f"Original file: {object_key}\n"
            f"Original size: {file_size} bytes\n"
            f"Character count: {len(file_content)}\n"
            f"Word count: {len(file_content.split())}\n"
            f"Processed at: {processed_at}\n\n"
            "Original content:\n"
            f"{file_content}"
        )

        output_key = f"processed/{object_key}"

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=processed_content.encode("utf-8"),
            ContentType="text/plain"
        )

        print(
            f"Processed file created: "
            f"s3://{OUTPUT_BUCKET}/{output_key}"
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "File processed successfully."
        })
    }
