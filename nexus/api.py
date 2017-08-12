import json
import re
import requests

class XmlReader():
  @staticmethod
  def read(content):
    return None # TODO

class JsonReader():
  @staticmethod
  def read(content):
    return json.loads(content)

class TextReader():
  @staticmethod
  def read(content):
    return content

_response_readers = dict(text=TextReader, xml=XmlReader, json=JsonReader)

class Api:
  def __init__(self, base_url):
    self.base_url = base_url
    self.sticky_data = {}

  def _do_request(self, endpoint, method, **kwargs):
    req_fn = getattr(requests, method)
    reader = _response_readers[kwargs.get("response_type", "text")]
    url = "{}/{}".format(self.base_url.strip("/"), "/".join(endpoint.names))
    data = {}
    data.update(self.sticky_data)
    data.update(endpoint.sticky_data)
    if "json" in kwargs:
      kwargs["json"].update(data)
    if "data" in kwargs:
      kwargs["data"].update(data)
    if "params" in kwargs:
      kwargs["params"].update(data)
    return reader.read(req_fn(url, json=kwargs.get("json"), data=kwargs.get("data"), params=kwargs.get("params")).content.decode())

  def get(self, endpoint, **kwargs):
    if "params" not in kwargs:
      kwargs["params"] = {}
    return self._do_request(endpoint, "get", **kwargs)

  def post(self, endpoint, **kwargs):
    if "json" not in kwargs and "data" not in kwargs:
      kwargs["data"] = {}
    return self._do_request(endpoint, "post", **kwargs)

  def __call__(self, **kwargs):
    cpy = Api(self.base_url)
    cpy.sticky_data = self.sticky_data.copy()
    cpy.sticky_data.update(kwargs)
    return cpy

  def __getattr__(self, name):
    return EndpointFactory(self, name)

class EndpointFactory:
  def __init__(self, api, name):
    self.names = [name]
    self.api = api
    self.sticky_data = {}

  def get(self, **kwargs):
    return self.api.get(self, **kwargs)

  def get_json(self, **kwargs):
    kwargs["response_type"] = "json"
    return self.api.get(self, **kwargs)

  def post(self, **kwargs):
    return self.api.post(self, **kwargs)

  def post_json(self, **kwargs):
    kwargs["response_type"] = "json"
    return self.api.post(self, **kwargs)

  def __getattr__(self, name):
    name = name.replace("_", ".")
    self.names.append(name)
    return self

  def __call__(self, **kwargs):
    self.sticky_data.update(kwargs)
    return self

  def __getitem__(self, key):
    self.names.append(str(key))
    return self

def load(url):
  return Api(url)