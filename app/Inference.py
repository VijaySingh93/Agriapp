from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('roberta-base-nli-stsb-mean-tokens')


def callfunc(text):
    searchtext = text
    client = Elasticsearch(hosts=[{"host":'elasticsearch'}], timeout=400, max_retries=10, retry_on_timeout=True)

    query_vector = embedder.encode(searchtext)
    print(len(query_vector))

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index='agriapp',
        body={
            "size": 1,
            "query": script_query,
            "_source": {"includes": ["query_text","kcc_answer"]}
        }
    )

    res = response
    return res
