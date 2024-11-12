import json

import dlt
import requests
from dlt.common.configuration.inject import with_config
from dlt.common.configuration.specs import GcpServiceAccountCredentials
from google.cloud import secretmanager


@with_config(sections=("google_secrets",))
def get_secret_dict(
    secret_id, credentials: GcpServiceAccountCredentials = dlt.secrets.value
):
    """
    Retrieve a secret from Google Cloud Secret Manager and convert to a dictionary.

    Args:
        secret_id (str): ID of the secret to retrieve.
        credentials (GcpServiceAccountCredentials): Credentials for accessing the secret manager.

    Returns:
        dict: The secret data as a dictionary.
    """
    # Create the Secret Manager client with provided credentials
    client = secretmanager.SecretManagerServiceClient(
        credentials=credentials.to_native_credentials()
    )
    # Build the resource name of the secret version
    name = f"projects/{credentials.project_id}/secrets/{secret_id}/versions/latest"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})
    # Decode the payload to a string and convert it to a dictionary
    secret_string = response.payload.data.decode("UTF-8")
    secret_dict = json.loads(secret_string)

    return secret_dict


@dlt.resource()
def get_repositories(
    api_token: str = dlt.secrets.value, organization: str = dlt.secrets.value
):
    """
    Retrieve repositories of a specified organization from GitHub.

    Args:
        api_token (str): GitHub API token for authentication.
        organization (str): The GitHub organization from which to retrieve repositories.

    Yields:
        list: A list of repositories for the specified organization.
    """
    BASE_URL = "https://api.github.com"
    url = f"{BASE_URL}/orgs/{organization}/repos"
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure that a HTTP error is raised for bad responses
    yield response.json()


if __name__ == "__main__":
    secret_data = get_secret_dict("temp-secret")
    data = get_repositories(api_token=secret_data["api_token"], organization="dlt-hub")

    pipeline = dlt.pipeline(
        pipeline_name="quick_start", destination="duckdb", dataset_name="mydata"
    )
    load_info = pipeline.run(data, table_name="repos")

    print(load_info)
