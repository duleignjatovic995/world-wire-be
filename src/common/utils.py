from json import JSONEncoder
from uuid import UUID


class FlexibleJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return JSONEncoder.default(self, obj)
