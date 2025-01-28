## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

## Run Weaviate

```shell
docker run -p 8080:8080 -p 50051:50051  -e ENABLE_MODULES=text2vec-openai,generative-openai cr.weaviate.io/semitechnologies/weaviate:1.28.4 
```
