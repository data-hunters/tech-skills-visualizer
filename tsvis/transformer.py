from typing import Dict, List, Tuple

import pandas as pd
from pandas import DataFrame

from tsvis.util import get_unique_elements


def preprocess_nodes(edges: List[Dict], tech_id_field: str = 'name', user_id_field: str = 'user_id') -> Tuple:
    """Split edges into two unique lists representing tags/technologies and users"""
    uniq_techs = get_unique_elements(edges, tech_id_field)
    uniq_users = get_unique_elements(edges, user_id_field)
    return uniq_techs, uniq_users


def build_base_nodes(technologies: List[Dict], users: List[Dict]) -> List[Dict]:
    nodes = [{'id': t['name'], 'label': t['name']} for t in technologies]
    nodes += [{'id': u['user_id'], 'label': u['user_name']} for u in users]
    return nodes


def build_node_colors(technologies: List[Dict], users: List[Dict],
                      tech_color: int = 0xFF000000, user_color: int = 0x0000FF00) -> List[int]:
    node_colors = [tech_color for i in range(0, len(technologies))]
    node_colors += [user_color for i in range(0, len(users))]
    return node_colors


def build_final_nodes(nodes: List[int], node_colors: List[int],
                      id_field: str = 'id', label_field: str = 'label') -> DataFrame:
    return pd.DataFrame.from_dict({
        'id': [str(n[id_field]) for n in nodes],
        'label': [n[label_field] for n in nodes],
        'color': node_colors
    })


def build_final_edges(edges: List[Dict], edges_id_field: str = 'name',
                      user_id_field: str = 'user_id', tags_count_field: str = 'count') -> DataFrame:
    return pd.DataFrame.from_dict({
        'tag_id': [e[edges_id_field] for e in edges],
        'user_id': [str(e[user_id_field]) for e in edges],
        'tags_count': [e[tags_count_field] for e in edges]
    })


def build_graph(edges: List[Dict], tech_color: int = 0xFF000000, user_color: int = 0x0000FF00) -> Tuple:
    technologies, users = preprocess_nodes(edges)
    nodes = build_base_nodes(technologies, users)
    node_colors = build_node_colors(technologies, users, tech_color, user_color)
    nodes_df = build_final_nodes(nodes, node_colors)
    edges_df = build_final_edges(edges)
    return nodes_df, edges_df
