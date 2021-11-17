from itertools import islice
from stackapi import StackAPI


def chunk(it, size):
    """ Nice chunking method from: https://stackoverflow.com/a/22045226 """
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


# Crawling questions by tag:
# https://api.stackexchange.com/docs/questions#order=desc&sort=votes&tagged=spark&filter=default&site=stackoverflow&run=true
# Crawling answers for questions:
# https://api.stackexchange.com/docs/answers-on-questions#order=desc&sort=activity&ids=31610971&filter=default&site=stackoverflow&run=true
# Crawling tags of users:
# https://api.stackexchange.com/docs/tags-on-users#order=desc&sort=popular&ids=3324741%3B3324743&filter=default&site=stackoverflow&run=true

def run(tags):
    """ Tags will be joined by AND operator, not OR"""
    site = StackAPI('stackoverflow')
    questions = site.fetch('questions', tagged=tags, sort='votes', order='desc')
    question_ids = [str(q['question_id']) for q in questions['items']]
    chunked_question_ids = chunk(question_ids, 100)
    tags = []
    for q_chunk in chunked_question_ids:
        answers = SITE.fetch(f'questions/{";".join(q_chunk)}/answers', sort='votes', order='desc')
        user_ids = [{'id': a['owner']['user_id'], 'name': a['owner']['display_name']} for a in answers['items']]
        users_map = {}
        for u in user_ids:
            users_map[u['id']] = u['name']
        chunked_user_ids = chunk(user_ids, 100)
        for u_chunk in chunked_user_ids:
            ids = [str(u['id']) for u in u_chunk]
            users_tags = SITE.fetch(f'users/{";".join(ids)}/tags', sort='popular', order='desc')
            users_tags = [{'name': t['name'], 'count': t['count'], 'user_id': t['user_id'], 'user_name': users_map[t['user_id']]} for t in users_tags['items']]
            tags.extend(users_tags)


if __name__ == '__main__':
    run('spark')
