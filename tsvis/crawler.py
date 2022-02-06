from typing import Dict, List
from stackapi import StackAPI
from tsvis.util import chunk, get_unique_elements


class StackOverflowCrawler:
    U_NOT_EXIST = 'does_not_exist'
    QUESTIONS_ENDPOINT = 'questions'
    ANSWERS_ENDPOINT = 'answers'
    USERS_ENDPOINT = 'users'
    TAGS_ENDPOINT = 'tags'

    def __init__(self, key=None, max_pages: int = 100, api: str = 'stackoverflow'):
        self.client = StackAPI(api, max_pages=max_pages, key=key)

    def crawl_user_tag_relations(self, tags: List[str],
                                 sort_field: str = 'votes',
                                 order: str = 'desc') -> List[Dict]:
        """
        Tags will be joined by AND operator, not OR
        Crawling questions by tag:
        https://api.stackexchange.com/docs/questions#order=desc&sort=votes&tagged=spark&filter=default&site=stackoverflow&run=true
        Crawling answers for questions:
        https://api.stackexchange.com/docs/answers-on-questions#order=desc&sort=activity&ids=31610971&filter=default&site=stackoverflow&run=true
        Crawling tags of users:
        https://api.stackexchange.com/docs/tags-on-users#order=desc&sort=popular&ids=3324741%3B3324743&filter=default&site=stackoverflow&run=true
        """

        print('Crawling questions...')
        questions = self.client.fetch(self.QUESTIONS_ENDPOINT, tagged=tags, sort=sort_field, order=order)
        question_ids = [str(q['question_id']) for q in questions['items']]
        chunked_question_ids = chunk(question_ids, 100)
        all_users = []
        users_map = {}
        print('Crawling answers...')
        for q_ids_chunk in chunked_question_ids:
            answers = self.client.fetch(f'{self.QUESTIONS_ENDPOINT}/{";".join(q_ids_chunk)}/{self.ANSWERS_ENDPOINT}',
                                        sort=sort_field, order=order)
            user_ids = []
            for a in answers['items']:
                if a['owner']['user_type'] != self.U_NOT_EXIST:
                    uid = a['owner']['user_id']
                    uname = a['owner']['display_name']
                    user_ids.append({'id': uid, 'name': uname})
                    users_map[uid] = uname
            all_users = all_users + user_ids
        all_users = [u['id'] for u in get_unique_elements(all_users)]
        return self.crawl_user_tags(all_users, users_map)

    def crawl_user_tags(self, user_ids: List[int],
                        users_map: dict,
                        sort_field: str = 'popular',
                        order: str = 'desc') -> List[Dict]:
        """ Crawl user tags based on provided list of user's IDs """
        user_ids = [str(id) for id in user_ids]
        chunked_user_ids = chunk(user_ids, 100)

        tags = []
        print('Crawling users...')
        for u_ids_chunk in chunked_user_ids:
            fetched_users_tags = self.client.fetch(
                f'{self.USERS_ENDPOINT}/{";".join(u_ids_chunk)}/{self.TAGS_ENDPOINT}', sort=sort_field, order=order)
            for t in fetched_users_tags['items']:
                tags.append({'name': t['name'], 'count': t['count'], 'user_id': t['user_id'],
                             'user_name': users_map[t['user_id']]})
        return tags
