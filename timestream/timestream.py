from switchbot.config import AppConfig
from query_client import QueryClient
from write_client import WriteClient


# Sample app:
# https://github.com/awslabs/amazon-timestream-tools/tree/mainline/sample_apps/python
#
# Service endpoints:
# https://docs.aws.amazon.com/general/latest/gr/timestream.html
def test_timestream_connection():
    app_config = AppConfig()

    aws_config = app_config.config['aws']

    write_client = WriteClient(region="us-east-1", aws_config=aws_config)

    write_client.describe_database(database_name='grumpletest')

    query_client = QueryClient(region="us-east-1", aws_config=aws_config)

    query_client.run_query(query_string="select * from grumpletest.sometestdata")



if __name__ == '__main__':

    print('Connecting to timestream')

    test_timestream_connection()

