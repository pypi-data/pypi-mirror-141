import taodata as td

import json

if __name__ == '__main__':
    api = td.get_api('123456', 30)

    api_name = 'wb_blog'

    bodyHelper = td.BodyHelper()
    bodyHelper.match_phrase(td.WbBlog.blog_raw_text, '普京')
    body = bodyHelper.to_json()

    fields = [td.WbBlog.blog_id, td.WbBlog.blog_raw_text]
    data = api.query(api_name=api_name, fields=fields, body=body)
    print(json.dumps(data))
    print(data['info'])
    print(data['fields'])
    print(data['alias_fields'])
    print(data['items'])

