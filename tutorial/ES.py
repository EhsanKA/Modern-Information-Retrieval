import json
from elasticsearch import Elasticsearch
import elasticsearch
import urllib3
import networkx as nx

id_strid = {}
strid_id = {}

lenght = 2000


def save_information(host='localhost', port=9200, address='papers.json'):
    es = Elasticsearch([{'host': host, 'port': port}])
    ic = elasticsearch.client.IndicesClient(es)

    ic.create("paper_index")
    f = open(address, "r+")
    papers = json.load(f)
    lenght = len(papers)
    for i in range(lenght):
        id_strid[i] = papers[i]['id']
        strid_id[papers[i]['id']] = i
        es.create("paper_index", doc_type="paper", id=i, body=papers[i])

    with open("strid_id.json", 'w') as outfile:
        json.dump(strid_id, outfile)
    with open("id_strid.json", 'w') as outfile:
        json.dump(id_strid, outfile)


def load_information():

    with open('strid_id.json') as infile:
            strid_id = json.load(infile)
    with open('id_strid.json') as infile:
            id_strid = json.load(infile)
    return strid_id, id_strid


def delete_information(host='localhost', port=9200, address="paper_index"):
    es = Elasticsearch([{'host': host, 'port': port}])
    ic = elasticsearch.client.IndicesClient(es)

    ic.delete("paper_index")


def pagerank(host='localhost', port=9200, address="paper_index", a=0.85):
    strid_id, id_strid = load_information()
    es = Elasticsearch([{'host': host, 'port': port}])
    ic = elasticsearch.client.IndicesClient(es)
    G = nx.DiGraph()
    for i in range(lenght):
        # print(es.get_source("paper_index", doc_type="paper", id=i))
        node = es.get_source("paper_index", doc_type="paper", id=i)
        # u = int(strid_id[node['id']])     #node['id']
        u = i
        # print(u)
        G.add_node(u)
        to = node['references']
        # print(type(to[0]))
        for j in range(len(to)):
            # print(to[j])
            # print(strid_id[to[j]])
            if to[j] in strid_id:
                v = int(strid_id[to[j]])             #to[j]
                G.add_node(v)
                G.add_edge(u, v)

    return nx.pagerank(G,a)

def add_pagerank_field(host='localhost', port=9200, address='papers.json'):
        es = Elasticsearch([{'host': host, 'port': port}])

        docs = []
        for i in range(lenght):
            res = es.get(index="paper_index", doc_type="paper", id=i)
            docs.append(res)

        pr = pagerank()
        delete_information()
        ic = elasticsearch.client.IndicesClient(es)
        ic.create("paper_index")

        for i in range(lenght):
            res = docs[i]
            res['_source']['page_rank']= pr[i]
            id_strid[i] = res['_source']['id']
            strid_id[res['_source']['id']] = i
            es.create("paper_index", doc_type="paper", id=i, body=res['_source'])



        # for i in range(lenght):
        #     # id_strid[i] = papers[i]['id']
        #     # strid_id[papers[i]['id']] =
        #     res = es.get(index="paper_index", doc_type="paper", id=i)
        #     res["_source"]["pagerank"]=0
        #     # es.delete(index="paper_index", doc_type="paper", id=i)
        #     # print(res["_source"])
        #     # es.index(index="paper_index", doc_type="paper", id=i,body=res["_source"])
        #     print(es.index(index="paper_index", doc_type="paper", id=i,body=res["_source"]))
        #     # es.update(index="paper_index", doc_type="paper", id=id_strid[i], body={"paper":{papers[i])


delete_information()
save_information()


# strid_id, id_strid = load_information()
# pr = pagerank()
# print(pr)
# print((len(pr)))

add_pagerank_field()