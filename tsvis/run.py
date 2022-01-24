import os
import graphistry
import pandas as pd

from tsvis.processor import build_graph
from tsvis.visualizer import GraphistryVisualizer


def write_skills(skills, path):
    import json
    edges_str = json.dumps(edges)
    with open(path, "w") as text_file:
        text_file.write(edges_str)


def load_skills(path):
    import json
    d = None
    with open(path) as f:
        d = json.load(f)
    return d



if __name__ == '__main__':
    user = os.environ['GRAPHISTRY_USER']
    password = os.environ['GRAPHISTRY_PASSWD']
    edges = [
        {'name': 'apache-kafka', 'count': 2524, 'user_id': 2308683, 'user_name': 'OneCricketeer'},
        {'name': 'apache-kafka', 'count': 2524, 'user_id': 2308683, 'user_name': 'OneCricketeer'},
        {'name': 'apache-kafka', 'count': 2524, 'user_id': 2308684, 'user_name': 'Lol'},
        {'name': 'apache-kafka', 'count': 2524, 'user_id': 2308685, 'user_name': 'ROTFL'}
    ]
    # edges = run('bigdata')
    edges = load_skills('skills_bigdata.json')
    # write_skills(edges, 'skills_bigdata.json')
    # net = Network()
    # uniq_techs = get_unique_elements(edges, 'name')
    # uniq_users = get_unique_elements(edges, 'user_id')
    # nodes = [{'id': t['name'], 'label': t['name']} for t in uniq_techs]
    # nodes += [{'id': u['user_id'], 'label': u['user_name']} for u in uniq_users]
    # node_colors = [0xFF000000 for i in range(0, len(uniq_techs))]
    # node_colors += [0x0000FF00 for i in range(0, len(uniq_users))]
    # node_ids = [str(n['id']) for n in nodes]
    # node_labels = [n['label'] for n in nodes]
    # node_id_labels = {}
    # for i in range(0, len(node_labels)):
    #     node_id_labels[node_ids[i]] = node_labels[i]
    #
    # nodes_df = pd.DataFrame.from_dict({
    #     'id': node_ids,
    #     'label': node_labels,
    #     'color': node_colors
    # })
    # edges_df = pd.DataFrame.from_dict({
    #     'technology_id': [e['name'] for e in edges],
    #     'user_id': [str(e['user_id']) for e in edges],
    #     'tags_count': [e['count'] for e in edges]
    # })
    # register_graphistry()
    # draw_graphistry(edges_df, nodes_df, 'user_id', 'technology_id', 'id', 'tags_count', 'color', 'label')
    nodes_df, edges_df = build_graph(edges)
    GraphistryVisualizer(user, password).plot(edges_df, nodes_df, 'user_id', 'technology_id',
                                              'id', 'tags_count', 'color', 'label')
