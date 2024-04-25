from dagster import asset, get_dagster_logger, AssetExecutionContext, MetadataValue
from dagster_snowflake import SnowflakeResource
from ..dlt import hacker_news, comments, google_trends, hacker_news_full
from ..resources import LocalFileStorage, DltPipeline
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


orchestration_tools = ("Kestra", "Dagster", "Airflow", "Luigi", "MageAi", "Keboola")


def run_dlt_pipeline_and_generate_md(pipeline: DltPipeline, resource_data, table_name: str):
    """
    Executes a dlt pipeline and generates a Markdown report.

    Args:
        pipeline: A DltResource object representing the dlt pipeline to be executed.
        resource_data: The data that will be used by the pipeline.
        table_name: The name of the table to be updated by the pipeline.

    Returns:
        A string containing the Markdown formatted summary of the schema updates performed by the pipeline.
    """

    logger = get_dagster_logger()

    # Create the pipeline and log the resulting load information
    load_info = pipeline.create_pipeline(
        resource_data = resource_data,
        table_name = table_name
    )
    logger.info(load_info)

    md_content = ""
    # Iterate through the load packages to update the Markdown content
    for package in load_info.load_packages:
        for table_name, table in package.schema_update.items():
            for column_name, column in table["columns"].items():
                md_content += f"\tTable updated: {table_name}: Column changed: {column_name}: {column['data_type']}\n"
    
    return md_content


@asset(group_name = "google_trends_data")
def google_trends_asset(context: AssetExecutionContext, pipeline: DltPipeline) -> None:
    """
    A Dagster asset that loads Google Trends data from the "google_trends" dlt resource to Snowflake using a dlt pipeline and documents the updates.
    """ 

    dlt_resource = google_trends(orchestration_tools)
    md_content = run_dlt_pipeline_and_generate_md(pipeline, resource_data = dlt_resource, table_name = "google_trends_asset")

    context.add_output_metadata(metadata = {"Updates": MetadataValue.md(md_content)})


@asset(group_name = "google_trends_data", deps = [google_trends_asset])
def google_trends_chart(snowflake: SnowflakeResource, image_storage: LocalFileStorage) -> None:
    """
    A Dagster asset that generates a line chart visualizing Google Trends data over time and saves it to the local storage.
    """
    
    with snowflake.get_connection() as conn:
        google_trends = conn.cursor().execute(
                f"SELECT * FROM {google_trends_asset.name}"
            ).fetch_pandas_all()
        
        # Plot the data
        google_trends["DATE"] = pd.to_datetime(google_trends['DATE'])
        pivot_df = google_trends.pivot(index='DATE', columns='TOOL', values='HITS')
        plt.figure(figsize=(10, 6))
        pivot_df.plot(kind='line', ax=plt.gca(), linewidth=2)
        plt.title('Google Trends Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Hits')
        plt.legend(title='Tool')
        plt.grid(True)
        plt.xticks(rotation = 45)
        plt.ylim(-50, 200)  # Setting y-axis range from -50 to 200 for better visbility 

        # Save the chart as an image to local storage
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0) 
        plt.close()
        filename = "google_trends_over_time.png"
        image_storage.write(filename, buffer)


@asset(group_name = "hacker_news_data")
def hacker_news_full_asset(context: AssetExecutionContext, pipeline: DltPipeline) -> None:
    """
    A Dagster asset that loads Hackernews data from the "hacker_news_full" dlt source to Snowflake using a dlt pipeline and documents the updates.
    """ 

    dlt_source = hacker_news_full(orchestration_tools)
    md_content = run_dlt_pipeline_and_generate_md(pipeline, resource_data = dlt_source, table_name = "hacke_news_full_asset")

    context.add_output_metadata(metadata={"Updates": MetadataValue.md(md_content)})


@asset(group_name = "hacker_news_data", deps = [hacker_news_full_asset])
def hacker_news_chart(snowflake: SnowflakeResource, image_storage: LocalFileStorage) -> None:
    """
    A Dagster asset that generates a line chart visualizing the sentiment of comments for each tool and saves it to the local storage.
    """

    with snowflake.get_connection() as conn:
        data = conn.cursor().execute(
            f"SELECT TOOL_NAME, SENTIMENT, COUNT(*) AS COUNT FROM HACKER_NEWS_FULL_ASSET WHERE SENTIMENT IN ('Neutral', 'Positive', 'Negative') GROUP BY TOOL_NAME, SENTIMENT"
        ).fetch_pandas_all()

        # Plot the data
        pivot_df = data.pivot(index='TOOL_NAME', columns='SENTIMENT', values='COUNT').fillna(0)
        plt.figure(figsize=(10, 6)) 
        pivot_df.plot(kind='bar', width=0.8)
        plt.title('Sentiment Counts for Each Tool on Hacker News')
        plt.xlabel('Tool Name')
        plt.ylabel('Count')
        plt.legend(title='Sentiment')
        plt.xticks(rotation=45)

        # Save the chart as an image to local storage
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)  
        plt.close()  
        filename = "hacker_news_sentiment_counts.png"
        image_storage.write(filename, buffer)


'''
@asset(group_name = "hacker_news_data")
def hacker_news_asset(context: AssetExecutionContext, pipeline: DltResource) -> None:
    """
    A Dagster asset that separately loads Hackernews stories from the "hacker_news" dlt resource to Snowflake using a dlt pipeline and documents the updates.
    """ 

    dlt_resource = hacker_news(orchestration_tools)
    md_content = run_dlt_pipeline_and_generate_md(pipeline, resource_data = dlt_resource, table_name = "hacker_news_asset")
   
    context.add_output_metadata(metadata={"Updates": MetadataValue.md(md_content)})
'''