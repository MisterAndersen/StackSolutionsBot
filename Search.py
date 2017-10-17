import requests, logging
from urllib.parse import quote
from string import Template
class Search:
    
    filter_string = '!t)HaoRoKRKSp-SLzkTBrhMYHH9UUFwE'
    template_url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q=$keywords&accepted=True&site=$site&filter=$filter'

    def search(self, keywords, site='stackoverflow'):
        url = Template(self.template_url).substitute(keywords=quote(keywords, safe=''), site=site, filter=self.filter_string)
        response = requests.get(url)
        if (response.status_code == requests.codes.ok):
            response_json = response.json()
            if (len(response_json['items']) > 0):
                return response_json['items'][0]
            else:
                logging.info(Template('Query $query had no valid answers').substitute(query=keywords))
        else:
            logging.error(Template(
                'Received status code $code when attempting to query Stack Exchange. Response is as follows: $response').substitute(
                code=response.status_code, response=response.text))
        return None