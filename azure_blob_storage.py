# References
# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli


from dotenv import load_dotenv
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()

KEY = os.getenv("KEY")
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def create_container():

    # BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    # Create a unique name for the container
    container_name = "reportscontainer"
    # Create the container
    container_client =  blob_service_client.create_container(container_name)


def main():

    create_container()

    # print(KEY, "\n\n", CONNECTION_STRING)


if __name__ == "__main__":
    main()

