import argparse
import os
import sys
import textwrap
from dataclasses import dataclass

from tsvis.crawler import StackOverflowCrawler
from tsvis.transformer import build_graph
from tsvis.visualizer import GraphistryVisualizer


@dataclass(frozen=True)
class InputConfig:
    g_user: str
    g_password: str
    stack_api_key: str
    tags: str
    max_pages: int


class ArgsHandler:
    GRAPHISTRY_USER_K = 'GRAPHISTRY_USER'
    GRAPHISTRY_PASSWD_K = 'GRAPHISTRY_PASSWD'
    STACK_API_KEY_K = 'STACK_API_KEY'
    NAME = 'TSVis'
    DESC = f'''
    TSVis - crawling StackOverflow posts and drawing user -> tag relations on Graph.
    
    In addition to arguments, you also need to provide environment variables:
    {GRAPHISTRY_USER_K} - username of Graphistry account.
    {GRAPHISTRY_PASSWD_K} - password of Graphistry account.
    {STACK_API_KEY_K} - optional. StackExchange API does not require key but it will increase limits,
    if you use it.
    '''

    TAGS_DESC = 'List of tags separated by semi-colon. They will be joined with AND operator.'
    MAX_PAGES_DESC = 'Max number of pages to crawl. StackOverflow API has limits. \n' \
                     'If you are getting message like "too many requests [...]", decrease this value.'

    def __init__(self):
        parser = argparse.ArgumentParser(prog='TSVis', description=textwrap.dedent(self.DESC), add_help=True,
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-t', '--tags', metavar='tags', type=str, help=self.TAGS_DESC)
        parser.add_argument('-p', '--max-pages', metavar='max_pages', type=int, help=textwrap.dedent(self.MAX_PAGES_DESC), default=10)
        self._parser = parser

    def parse(self):
        args = self._parser.parse_args()
        max_pages = args.max_pages
        tags = args.tags
        user = os.environ.get(self.GRAPHISTRY_USER_K, None)
        password = os.environ.get(self.GRAPHISTRY_PASSWD_K, None)
        stack_api_key = os.environ.get(self.STACK_API_KEY_K, None)
        if None in [tags, user, password]:
            print('You have to provide all necessary arguments and environment variables!\n', file=sys.stderr)
            self._parser.print_help(file=sys.stderr)
        return InputConfig(user, password, stack_api_key, tags, max_pages)


if __name__ == '__main__':
    input_args = ArgsHandler().parse()
    print(f'Starting crawler for tags: {input_args.tags}')
    edges = StackOverflowCrawler(input_args.stack_api_key, input_args.max_pages).crawl_user_tag_relations(input_args.tags)
    nodes_df, edges_df = build_graph(edges)
    GraphistryVisualizer(input_args.g_user, input_args.g_password).plot(edges_df, nodes_df, 'user_id', 'tag_id',
                                              'id', 'tags_count', 'color', 'label')
