import boto3
from botocore.config import Config
from query_client import QueryClient



# Sample app:
# https://github.com/awslabs/amazon-timestream-tools/tree/mainline/sample_apps/python
def connect_timestream():

    session = boto3.Session()

    # Recommended Timestream write client SDK configuration:
    #  - Set SDK retry count to 10.
    #  - Use SDK DEFAULT_BACKOFF_STRATEGY
    #  - Set RequestTimeout to 20 seconds .
    #  - Set max connections to 5000 or higher.
    write_client = session.client('timestream-write', config=Config(read_timeout=20, max_pool_connections=5000, retries={'max_attempts': 10}))

    query_client = QueryClient(client=session.client('timestream-query', config=Config()))

    # TODO: update this and get from config
    """
    ts_client = session.client(
        'timestream-query',
        region_name="us-east-1",
        endpoint_url="https://query.timestream.us-east-1.amazonaws.com",
        aws_access_key_id="???",
        aws_secret_access_key="???"
    )
    """

    query_client.run_query(query_string="select * from grumpletest.sometestdata")



if __name__ == '__main__':

    print('Connecting to timestream')

    connect_timestream()

