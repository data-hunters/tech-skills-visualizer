from stackapi import StackAPI
from tsvis.util import chunk, get_unique_elements


class StackOverflowCrawler:
    U_NOT_EXIST = 'does_not_exist'
    QUESTIONS_ENDPOINT = 'questions'
    ANSWERS_ENDPOINT = 'answers'
    USERS_ENDPOINT = 'users'
    TAGS_ENDPOINT = 'tags'

    def __init__(self, api='stackoverflow'):
        self.site = StackAPI(api)

    def crawl_user_tag_relations(self, tags, sort_field='votes', order='desc'):
        """
        Tags will be joined by AND operator, not OR
        Crawling questions by tag:
        https://api.stackexchange.com/docs/questions#order=desc&sort=votes&tagged=spark&filter=default&site=stackoverflow&run=true
        Crawling answers for questions:
        https://api.stackexchange.com/docs/answers-on-questions#order=desc&sort=activity&ids=31610971&filter=default&site=stackoverflow&run=true
        Crawling tags of users:
        https://api.stackexchange.com/docs/tags-on-users#order=desc&sort=popular&ids=3324741%3B3324743&filter=default&site=stackoverflow&run=true
        """

        questions = self.site.fetch(self.QUESTIONS_ENDPOINT, tagged=tags, sort='votes', order='desc')
        question_ids = [str(q['question_id']) for q in questions['items']]
        chunked_question_ids = chunk(question_ids, 100)
        all_users = []
        users_map = {}
        for q_ids_chunk in chunked_question_ids:
            answers = self.site.fetch(f'{self.QUESTIONS_ENDPOINT}/{";".join(q_ids_chunk)}/{self.ANSWERS_ENDPOINT}', sort=sort_field, order=order)
            user_ids = [{'id': a['owner']['user_id'], 'name': a['owner']['display_name']} for a in answers['items'] if a['owner']['user_type'] != self.U_NOT_EXIST]
            all_users = all_users + user_ids
            for u in user_ids:
                users_map[u['id']] = u['name']
        all_users = [u['id'] for u in get_unique_elements(all_users)]
        return self.crawl_user_tags(all_users, users_map)

    def crawl_user_tags(self, user_ids, users_map, sort_field='popular', order='desc'):
        """ Crawl user tags based on provided list of user's IDs """
        chunked_user_ids = chunk(user_ids, 100)
        tags = []
        for u_ids_chunk in chunked_user_ids:
            u_ids_chunk = [str(id) for id in u_ids_chunk]
            users_tags = self.site.fetch(f'{self.USERS_ENDPOINT}/{";".join(u_ids_chunk)}/{self.TAGS_ENDPOINT}', sort=sort_field, order=order)
            users_tags = [{'name': t['name'], 'count': t['count'], 'user_id': t['user_id'], 'user_name': users_map[t['user_id']]} for t in users_tags['items']]
            tags.extend(users_tags)
        return tags

