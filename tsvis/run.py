import os
import sys
from tsvis.crawler import StackOverflowCrawler
from tsvis.transformer import build_graph
from tsvis.visualizer import GraphistryVisualizer

if __name__ == '__main__':
    user = os.environ['GRAPHISTRY_USER']
    password = os.environ['GRAPHISTRY_PASSWD']
    tags = sys.argv[1]
    max_pages = 50
    if len(sys.argv) > 2:
        max_pages = int(sys.argv[2])
    edges = StackOverflowCrawler(max_pages).crawl_user_tag_relations(tags)
    nodes_df, edges_df = build_graph(edges)
    GraphistryVisualizer(user, password).plot(edges_df, nodes_df, 'user_id', 'tag_id',
                                              'id', 'tags_count', 'color', 'label')
