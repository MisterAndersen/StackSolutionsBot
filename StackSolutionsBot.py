import praw, yaml, re, requests, html
import logging
from string import Template
reddit = None

def load_session():
    with open("creds.yml", 'r') as stream:
        try:
            creds = yaml.load(stream)
            username = creds['username']
            password = creds['password']
            client_id = creds['client_id']
            client_secret = creds['client_secret']
            user_agent = creds['user_agent']

            global reddit
            reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password,
                                 user_agent=user_agent, username=username)
            logging.basicConfig( level=logging.INFO)

        except yaml.YAMLError as exc:
            logging.error(exc)

def main():
    load_session()
    for comment in reddit.subreddit('overflowbottesting').stream.comments():
        result = re.search('(?<=overflowbot search).*$', comment.body)
        if (result is not None):
            logging.info(Template('Received query: $query').substitute(query=result.group(0)))
            overflow_answer = overflow_search(result.group(0))
            if (overflow_answer is not None):
                try:
                    logging.info(Template('Posting comment $comment').substitute(comment=overflow_answer))
                    comment.reply(overflow_answer)
                except praw.exceptions.APIException as err:
                    logging.error(str(err))

def overflow_search(keywords):
    url = Template('https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&accepted=True&title=$title&site=stackoverflow&filter=!4y_5(4rHB9wzDjwGn35hUSguJO2n5y38KMQZ9P').substitute(title=keywords)
    response = requests.get(url)
    if (response.status_code == requests.codes.ok):
        response_json = response.json()
        if (len(response_json['items']) > 0):
            return html.unescape(response_json['items'][0]['answers'][0]['body_markdown'])
        else:
            logging.info(Template('Query $query had no valid answers').substitute(query=keywords))
    else:
        logging.error(Template('Received status code $code when attempting to query Stack Overflow. Response is as follows: $response').substitute(code = response.status_code, response=response.text))
    return None


if __name__ == '__main__':
    main()
