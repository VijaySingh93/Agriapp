"""
Example script to create elasticsearch documents.
"""
import argparse
import json
import pickle
import joblib

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

def load_dataset(path):
    docs = []
    print("Loading CSV")
    df = pd.read_csv(path, index_col=0)
    df.reset_index(inplace=True)
    df.fillna(value='not available', inplace=True)
    print("CSV read")
    for row in df.iterrows():
        series = row[1]
        doc = {
            'query_text': series['QueryText_clean'],
            'kcc_answer': series['KCCAns']
        }
        docs.append(doc)
        if row[0]%1000 == 0:
            print('{} docs created'.format(row[0]))
    return docs



def index_batch(docs, index):
    file = open('sentence_embeddings.pkl', 'rb')
    # load information from file
    corpus_embeddings = joblib.load(file)
    # close the file
    file.close()
    print(len(docs))
    print(len(corpus_embeddings))   

    requests = []
    for i, doc in enumerate(docs):
        request = doc
        request["_op_type"] = "index"
        request["_index"] = 'agriapp'
        request["text_vector"] = corpus_embeddings[i+index]
        requests.append(request)
    bulk(client, requests)

def main(args):
    print("Loading docs")
    docs = load_dataset(args.data)
    i=0
    while i+15000 <= len(docs):
        index_batch(docs[i:i+15000], i)
        i = i+15000
        print('{} documents indexed'.format(i+15000))
    # sentences = pd.read_csv('sentences_new.csv')
    if i < len(docs):
        index_batch(docs[i:-1], i)
    print('Indexed all documents')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    client = Elasticsearch(hosts=[{"host":'elasticsearch'}], timeout=400, max_retries=10, retry_on_timeout=True)
    parser.add_argument('--data', help='data for creating documents.')
    # parser.add_argument('--save', default='documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='agriapp', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
