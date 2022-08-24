


class WriteClient:

    def __init__(self, client):
        self.client = client

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

