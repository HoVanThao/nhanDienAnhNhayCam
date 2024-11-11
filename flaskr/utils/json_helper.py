from json import JSONEncoder
import json
from flask.json.provider import JSONProvider
from json import JSONEncoder
import json
from flask.json.provider import JSONProvider
from datetime import datetime, date

class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()  # Sử dụng hàm tích hợp sẵn của Python
        else:
            return super().default(o)

class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=MongoJSONEncoder)

    def loads(self, s: str | bytes, **kwargs):
        return json.loads(s, **kwargs)