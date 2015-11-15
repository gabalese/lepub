import inspect
import json


class JSONAble(object):
    def json(self):
        superclass = super(JSONAble, self).__self_class__
        members = inspect.getmembers(superclass, predicate=inspect.isdatadescriptor)
        properties = map(lambda x: x[0], filter(lambda x: x[0] != '__weakref__', members))
        return json.dumps(
            {
                prop: getattr(self, prop)
                for prop in properties
                if getattr(self, prop) is not None
            }, default=lambda o: o.as_json()
        )


