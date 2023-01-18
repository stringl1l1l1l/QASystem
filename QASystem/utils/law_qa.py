# coding:utf-8

from elasticsearch import Elasticsearch

'''数据库查询'''


class ES(object):
    def __init__(self):
        self.index_law = "test_data"
        self.index_qa = "test_data"
        # 无用户名密码状态
        self.es = Elasticsearch('http://192.168.206.100:9200')
        self.doc_type = "qa"  # 相当于在指定数据库中创建的表名称

    # 法条查询
    def get_law(self, question):
        res = []
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "content": question
                            }
                        }
                    ],
                    "must_not": [],
                    "should": []
                }
            },
            "from": 0,
            "size": 20,
            "sort": [],
            "aggs": {}
        }
        res = self.es.search(index=self.index_law, body=body)["hits"]["hits"]

        answer_list = []
        for hit in res:
            # print(type(hit))
            # print(hit.keys())
            # for key in hit:
            #     print(key)
            #     print(hit.get(key))
            # exit()
            answer_dict = {}
            answer_dict['score'] = (float)(hit.get('_score') / 100)
            answer_dict['lawname'] = hit['_source']['lawname']
            answer_dict['num'] = hit['_source']['num']
            answer_dict['content'] = hit['_source']['content']

            answer_list.append(answer_dict)
        # print(type(answer_list[0]['score']))
        return sorted(answer_list, key=lambda x: x.get('score'), reverse=True)[0]

    # 问答查询
    def get_qa(self, question):
        res = []
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "content": question
                            }
                        }
                    ],
                    "must_not": [],
                    "should": []
                }
            },
            "from": 0,
            "size": 20,
            "sort": [],
            "aggs": {}
        }
        res = self.es.search(index=self.index_qa, body=body)["hits"]["hits"]

        answer_list = []
        for hit in res:
            answer_dict = {}
            answer_dict['score'] = (float)(hit.get('_score') / 100)
            answer_dict['lawname'] = hit['_source']['lawname']
            answer_dict['num'] = hit['_source']['num']
            answer_dict['content'] = hit['_source']['content']

            answer_list.append(answer_dict)
        # print(type(answer_list[0]['score']))
        return sorted(answer_list, key=lambda x: x.get('score'), reverse=True)[0]
