import pandas as pd

from tsvis.util import get_unique_elements


def preprocess_nodes(edges, tech_id_field='name', user_id_field='user_id'):
    uniq_techs = get_unique_elements(edges, tech_id_field)
    uniq_users = get_unique_elements(edges, user_id_field)
    return uniq_techs, uniq_users


def build_base_nodes(technologies, users):
    nodes = [{'id': t['name'], 'label': t['name']} for t in technologies]
    nodes += [{'id': u['user_id'], 'label': u['user_name']} for u in users]
    return nodes


def build_node_colors(technologies, users, tech_color=0xFF000000, user_color=0x0000FF00):
    node_colors = [tech_color for i in range(0, len(technologies))]
    node_colors += [user_color for i in range(0, len(users))]
    return node_colors


def build_final_nodes(nodes, node_colors, id_field='id', label_field='label'):
    return pd.DataFrame.from_dict({
        'id': [str(n[id_field]) for n in nodes],
        'label': [n[label_field] for n in nodes],
        'color': node_colors
    })


def build_final_edges(edges, edges_id_field='name', user_id_field='user_id', tags_count_field='count'):
    return pd.DataFrame.from_dict({
        'tag_id': [e[edges_id_field] for e in edges],
        'user_id': [str(e[user_id_field]) for e in edges],
        'tags_count': [e[tags_count_field] for e in edges]
    })


def build_graph(edges, tech_color=0xFF000000, user_color=0x0000FF00):
    technologies, users = preprocess_nodes(edges)
    nodes = build_base_nodes(technologies, users)
    node_colors = build_node_colors(technologies, users, tech_color, user_color)
    nodes_df = build_final_nodes(nodes, node_colors)
    edges_df = build_final_edges(edges)
    return nodes_df, edges_df
