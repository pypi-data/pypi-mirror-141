import os
import s3fs
import networkx as nx
import pandas as pd

from typing import Sequence


class CTNASApiError(BaseException):
    pass


class CTNASApi(object):
    def __init__(self, access_key: str = None, secret_key: str = None, endpoint: str = None, path_cache: str = "~/.cache/ctnas/"):
        path_cache = os.path.expanduser(path_cache)
        if not os.path.exists(path_cache):
            os.makedirs(path_cache)
        self._path_cache = path_cache

        self._s3_access_key = access_key if access_key is not None else "ctnas-public-acc"
        self._s3_secret_key = secret_key if secret_key is not None else "ctnas-public-sec"
        self._s3_endpoint = endpoint if endpoint is not None else "https://share.pads.fim.uni-passau.de"
        self._s3_base = "/homes/stier/ctnas/"

        self._pd_graph_props = None
        self._pd_computations = None

        self._initialize_s3fs()

    def _initialize_s3fs(self):
        self._s3fs = s3fs.S3FileSystem(
            key=self._s3_access_key,
            secret=self._s3_secret_key,
            use_ssl=True,
            client_kwargs={
              "endpoint_url": self._s3_endpoint,
            }
        )

    def _ensure_pd_graph_props(self):
        if self._pd_graph_props is None:
            self._load_pd_graph_props()

    def _load_pd_graph_props(self):
        path_cache_propfile = os.path.join(self._path_cache, "graph-properties.csv")
        path_s3_propfile = os.path.join(self._s3_base, "graph-properties.csv")
        if not os.path.exists(path_cache_propfile):
            self._s3fs.download(path_s3_propfile, path_cache_propfile)

        self._pd_graph_props = pd.read_csv(path_cache_propfile)

    def _ensure_pd_computations(self):
        if self._pd_computations is None:
            self._load_pd_computations()

    def _load_pd_computations(self):
        path_cache_compfile = os.path.join(self._path_cache, "ctnas-computations.csv")
        path_s3_compfile = os.path.join(self._s3_base, "ctnas-computations.csv")
        if not os.path.exists(path_cache_compfile):
            self._s3fs.download(path_s3_compfile, path_cache_compfile)

        self._pd_computations = pd.read_csv(path_cache_compfile)

    def get_computations(self) -> pd.DataFrame:
        self._ensure_pd_computations()
        return self._pd_computations

    def get_graph_properties(self) -> pd.DataFrame:
        self._ensure_pd_graph_props()
        return self._pd_graph_props

    def get_graph(self, uuid: str) -> nx.Graph:
        path_cache_graph = os.path.join(self._path_cache, "graphs", uuid + ".adjlist")
        path_s3_graph = os.path.join(self._s3_base, "graphs", uuid + ".adjlist")
        if not os.path.exists(path_cache_graph):
            try:
                self._s3fs.download(path_s3_graph, path_cache_graph)
            except FileNotFoundError as e:
                raise CTNASApiError("Could not find graph with that UUID=%s" % uuid, e)

        return nx.read_adjlist(path_cache_graph)

    def get_graphs(self) -> Sequence[nx.Graph]:
        for uuid in self.get_graph_uuids():
            yield self.get_graph(uuid)

    def get_graph_uuids(self) -> Sequence[str]:
        self._ensure_pd_graph_props()
        return list(pd.unique(self._pd_graph_props["graph_uuid"]))

    def get_datasets(self) -> Sequence[str]:
        self._ensure_pd_computations()
        return list(pd.unique(self._pd_computations["dataset"]))
