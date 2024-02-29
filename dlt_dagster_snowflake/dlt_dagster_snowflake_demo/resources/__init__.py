from dagster import ConfigurableResource 
import dlt
import os


# Define a Dagster resource for managing dlt pipelines
class DltPipeline(ConfigurableResource):
    # Initialize resource with pipeline details
    pipeline_name: str
    dataset_name: str
    destination: str

    def create_pipeline(self, resource_data, table_name):
        """
        Creates and runs a dlt pipeline with specified data and table name.
        
        Args:
            resource_data: The data to be processed by the pipeline.
            table_name: The name of the table where data will be loaded.
        
        Returns:
            The result of the pipeline execution.
        """

        # Configure the dlt pipeline with your destination details
        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination=self.destination,
            dataset_name=self.dataset_name
        )

        # Run the pipeline with your parameters
        load_info = pipeline.run(resource_data, table_name=table_name)
        return load_info


# Define a Dagster resource for managing local file storage
class LocalFileStorage(ConfigurableResource):
    dir: str

    def setup_for_execution(self, context) -> None:
        """
        Prepares the local directory for file storage, creating it if it doesn't exist.
        
        Args:
            context: The Dagster execution context (not used here).
        """

        # Ensure the storage directory exists
        os.makedirs(self.dir, exist_ok=True)

    def write(self, filename, data):
        """
        Writes data to a file within the local storage directory.
        
        Args:
            filename: The name of the file to write to.
            data: The data to be written to the file.
        """

        # Create the directory path for the file if it does not exist
        dir_path = f"{self.dir}/{os.path.dirname(filename)}"
        os.makedirs(dir_path, exist_ok=True)

        # Write data to the file in binary mode
        with open(f"{self.dir}/{filename}", "wb") as f:
            f.write(data.read())
