import boto3
from botocore.config import Config
import time

class WriteClient:

    INGEST_URL = "https://ingest-cell2.timestream.us-east-1.amazonaws.com"

    def __init__(self, region, aws_config):

        self.region_name = region

        session = boto3.Session()

        # Recommended Timestream write client SDK configuration:
        #  - Set SDK retry count to 10.
        #  - Use SDK DEFAULT_BACKOFF_STRATEGY
        #  - Set RequestTimeout to 20 seconds .
        #  - Set max connections to 5000 or higher.
        self.client = session.client(
            'timestream-write',
            region_name=self.region_name,
            endpoint_url=self.INGEST_URL,
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key'],
            config=Config(read_timeout=20, max_pool_connections=5000, retries={'max_attempts': 10})
        )

    def describe_database(self, database_name):
        print("Describing database")

        result = self.client.describe_database(DatabaseName=database_name)

        try:
            # result = self.client.describe_database(DatabaseName=database_name)
            print("Database [%s] has id [%s]" % (database_name, result['Database']['Arn']))
        except self.client.exceptions.ResourceNotFoundException:
            print("Database doesn't exist")
        except Exception as err:
            print("Describe database failed:", err)

    def write_records(self, database_name, table_name, records):
        print("Writing records")

        try:
            result = self.client.write_records(
                DatabaseName=database_name,
                TableName=table_name,
                Records=records,
                CommonAttributes={}
            )
            print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
        except self.client.exceptions.RejectedRecordsException as err:
            self._print_rejected_records_exceptions(err)
        except Exception as err:
            print("Error:", err)

    @staticmethod
    def current_milli_time():
        return str(int(round(time.time() * 1000)))

    @staticmethod
    def _print_rejected_records_exceptions(err):
        print("RejectedRecords: ", err)
        for rr in err.response["RejectedRecords"]:
            print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
            if "ExistingVersion" in rr:
                print("Rejected record existing version: ", rr["ExistingVersion"])


