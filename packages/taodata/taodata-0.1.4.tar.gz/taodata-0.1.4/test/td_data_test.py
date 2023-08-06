import taodata as td

if __name__ == '__main__':
    api = td.get_api('123456', 30)

    api_name = 'wb_blog'
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "blog.raw_text": "股票"
                        }
                    }
                ]
            }
        }
    }
    fields = ['blog.id', 'blog.raw_text']
    pd = api.query(api_name=api_name, fields=fields, body=body)
    print(pd)

