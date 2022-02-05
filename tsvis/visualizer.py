from typing import Tuple

import graphistry
import pyarrow as pa
from pandas import DataFrame


class GraphistryVisualizer:
    """ Helper class for ploting network graps in Graphistry """

    def __init__(self, user: str, password: str, protocol: str = 'https', server: str = 'hub.graphistry.com',
                 edge_opacity: float = 0.4, edge_size: int = 25, max_poi: int = 100) -> None:
        self.edge_opacity = edge_opacity
        self.edge_size = edge_size
        self.max_poi = max_poi
        self._register_graphistry(user, password, protocol, server)

    @staticmethod
    def _register_graphistry(user: str, password: str, protocol: str, server: str) -> None:
        graphistry.register(api=3,
                            protocol=protocol,
                            server=server,
                            username=user,
                            password=password)

    @staticmethod
    def _convert_to_arrow(edges_df: DataFrame, nodes_df: DataFrame) -> Tuple:
        """ Convert edges and nodes of the graph from Pandas DataFrames to Arrow format """
        edges_arr = pa.Table.from_pandas(edges_df)
        nodes_arr = pa.Table.from_pandas(nodes_df)
        print('Edges schema:')
        print(edges_arr.schema)
        print()
        print('Nodes schema:')
        print(nodes_arr.schema)
        return edges_arr, nodes_arr

    def plot(self, edges_df: DataFrame, nodes_df: DataFrame, source_col: str, dest_col: str,
                        node_id_col: str, edge_weight_col: str, node_color_col: str, node_label_col: str) -> str:
        """ Draw graph and returns URL to Graphistry view"""
        edges_arr, nodes_arr = self._convert_to_arrow(edges_df, nodes_df)
        url = graphistry.edges(edges_arr, source_col, dest_col) \
            .nodes(nodes_arr) \
            .bind(source=source_col,
                  destination=dest_col,
                  node=node_id_col,
                  point_color=node_color_col,
                  point_title=node_label_col,
                  edge_weight=edge_weight_col) \
            .settings(url_params={
                'edgeOpacity': self.edge_opacity,
                'edgeSize': self.edge_size,
                'pointsOfInterestMax': self.max_poi
            }).plot(render=False)
        print(url)
        return url
