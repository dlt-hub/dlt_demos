# from restack_ai.function import function, log
import dlt
from dlt.destinations import weaviate
from openai import Completion


# Step 4: Perform RAG Query
def rag_query(client, prompt):
    # Step 4.1: Query Weaviate for relevant documents
    response = client.query.get("AnimeDataNew_Anime", ["title", "synopsis"]).with_near_text({
        "concepts": [prompt]
    }).with_limit(3).do()

    if "data" in response and "Get" in response["data"]:
        docs = response["data"]["Get"]["AnimeDataNew_Anime"]
        print("Retrieved documents:")
        for doc in docs:
            print(f"- {doc['title']}: {doc['synopsis']}\n")
    else:
        print("No results found.")
        return None

    # Step 4.2: Combine retrieved documents
    context = " ".join([doc["synopsis"] for doc in docs])

    # Step 4.3: Use OpenAI to generate a response
    import openai
    openai.api_key = dlt.secrets["openai.api_key"]  # Replace with your OpenAI API key

    completion = Completion.create(
        engine="text-davinci-003",  # Replace with the desired engine
        prompt=f"{context}\n\nQuestion: {prompt}\nAnswer:",
        max_tokens=150
    )

    print("Generated Answer:")
    print(completion.choices[0].text.strip())


if __name__ == "__main__":

    pipeline = dlt.pipeline(
        pipeline_name="anime_pipeline",
        destination="weaviate",
        dataset_name="anime_data_new",
        progress="log",
        dev_mode=False,
    )
    with pipeline.destination_client() as client:
        # print(client.db_client.query.get("AnimeDataNew_Anime", ["synopsis"]).do())
        # result = client.db_client.query.get("AnimeDataNew_Anime", ["synopsis", "title"]).with_near_text({
        #     "concepts": ["cowboy"]
        # }).do()
        #
        # print(result)
        question = "What is the story about Ye Bufan and his medical skills?"
        rag_query(client.db_client, question)