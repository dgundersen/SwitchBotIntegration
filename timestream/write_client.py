import boto3
from botocore.config import Config

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

