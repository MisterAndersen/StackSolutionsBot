import html
import logging
from string import Template


class Response:
    template_response = '**$asker asked: $question**\n\n' \
                        '$body\n\n' \
                        '*****\n' \
                        '**$replier answered**:\n\n $answer\n\n' \
                        '*****\n' \
                        '[Source]($link) (I\'m a bot, *bleep bloop*)'

    error_response = 'I couldn\'t find any results for that query.\n\n' \
                     'Sorry ¯\\\\\_(ツ)\_/¯\n\n' \
                     '^(I\'m a bot, *bleep bloop*)'

    def construct_response(self, result):
        if result is not None:
            accepted_answer = self.find_accepted_answer(result)
            if accepted_answer is not None:
                return Template(self.template_response).substitute(asker=result['owner']['display_name'],
                                                                   question=result['title'],
                                                                   body=html.unescape(result['body_markdown']),
                                                                   replier=html.unescape(accepted_answer['owner']['display_name']),
                                                                   answer=html.unescape(accepted_answer['body_markdown']),
                                                                   link=result['link'])
        else:
            logging.warning('Couldn\'t find an answer for the query')
            return self.error_response

    def find_accepted_answer(self, result):
        for answer in result['answers']:
            if answer['is_accepted']:
                return answer
        logging.error('Could not find the accepted answer.')
