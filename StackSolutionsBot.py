import praw, yaml, re, time
import logging
from string import Template
from Search import Search
from Response import Response
from praw.models import Comment

reddit = None
username = None


def load_session():
    with open("creds.yml", 'r') as stream:
        try:
            creds = yaml.load(stream)
            global username
            username = creds['username']
            password = creds['password']
            client_id = creds['client_id']
            client_secret = creds['client_secret']
            user_agent = creds['user_agent']

            global reddit
            reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password,
                                 user_agent=user_agent, username=username)
            logging.basicConfig(level=logging.INFO)

        except yaml.YAMLError as exc:
            logging.error(exc)


def main():
    load_session()
    while True:
        for item in reddit.inbox.mentions():
            processed = []
            if isinstance(item, Comment) and item.new:
                parse_query(item)
                processed.append(item)
            reddit.inbox.mark_read(processed)
        time.sleep(5)

def parse_query(comment):
    result = re.search('(?<=/u/' + username + ' ).*$', comment.body, re.IGNORECASE)
    if result is not None:
        logging.info(Template('Received query: $query').substitute(query=result.group(0)))
        try:
            comment.reply(Response().construct_response(Search().search(result.group(0))))
            logging.info('Posted comment')
        except praw.exceptions.APIException as err:
            logging.error(str(err))

if __name__ == '__main__':
    main()
