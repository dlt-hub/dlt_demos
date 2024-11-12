# Use `dlt` with Cloud Secrets Vaults

## Google Cloud Secret Manager 
To retrieve secrets from Google Cloud Secret Manager using Python, and convert them into a dictionary format, you'll need to follow these steps. First, ensure that you have the necessary permissions to access the secrets on Google Cloud, and have the `google-cloud-secret-manager` library installed. If not, you can install it using pip:

```bash
pip install google-cloud-secret-manager
```
[Google Docs](https://cloud.google.com/secret-manager/docs/reference/libraries)

Here's how you can retrieve secrets and convert them into a dictionary:

1. **Set up the Secret Manager client**: Create a client that will interact with the Secret Manager API.
2. **Access the secret**: Use the client to access the secret's latest version.
3. **Convert to a dictionary**: If the secret is stored in a structured format (like JSON), parse it into a Python dictionary.

Assume we store secrets in JSON format:
```json
{"api_token": "ghp_Kskdgf98dugjf98ghd...."}
```

In the script `dlt_with_google_secrets_pipeline.py` you can find an example how to use Google Secrets in `dlt` pipelines.

### Points to Note:

- **Permissions**: Ensure the service account or user credentials you are using have the necessary permissions to access the Secret Manager and the specific secrets.
- **Secret Format**: This example assumes that the secret is stored in a JSON string format. If your secret is in a different format, you will need to adjust the parsing method accordingly.
- **Google Cloud Authentication**: Make sure your environment is authenticated with Google Cloud. This can typically be done by setting credentials in `.dlt/secrets.toml` or setting the `GOOGLE_SECRETS__CREDENTIALS` environment variable to the path of your service account key file or the dict of credentials as a string.

With this setup, you can effectively retrieve secrets stored in Google Cloud Secret Manager and use them in your `dlt` pipelines as dictionaries.