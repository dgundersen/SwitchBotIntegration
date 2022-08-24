import boto3
from botocore.config import Config
from query_client import QueryClient
from write_client import WriteClient
from switchbot.config import AppConfig


# Sample app:
# https://github.com/awslabs/amazon-timestream-tools/tree/mainline/sample_apps/python
#
# Service endpoints:
# https://docs.aws.amazon.com/general/latest/gr/timestream.html
def connect_timestream():

    app_config = AppConfig()

    config = app_config.get_config()

    aws_config = config['aws']

    session = boto3.Session()

    region = "us-east-1"
    ingest_url = "https://ingest-cell2.timestream.us-east-1.amazonaws.com"
    query_url = "https://query-cell2.timestream.us-east-1.amazonaws.com"

    # Recommended Timestream write client SDK configuration:
    #  - Set SDK retry count to 10.
    #  - Use SDK DEFAULT_BACKOFF_STRATEGY
    #  - Set RequestTimeout to 20 seconds .
    #  - Set max connections to 5000 or higher.
    ts_write_client = session.client(
        'timestream-write',
        region_name=region,
        endpoint_url=ingest_url,
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key'],
        config=Config(read_timeout=20, max_pool_connections=5000, retries={'max_attempts': 10})
    )

    ts_query_client = session.client(
        'timestream-query',
        region_name=region,
        endpoint_url=query_url,
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    write_client = WriteClient(client=ts_write_client)

    write_client.describe_database(database_name='grumpletest')

    query_client = QueryClient(client=ts_query_client)

    query_client.run_query(query_string="select * from grumpletest.sometestdata")



if __name__ == '__main__':

    print('Connecting to timestream')

    connect_timestream()

