__author__ = 'Thamme Gowda N'

'''
This module offers solr client.

Created on November 20, 2015
'''
import json
import requests

class Solr(object):
    '''
    Solr client  for querying, posting and committing
    '''

    def __init__(self, solr_url,
                 commit_batch=100):
        self.update_url = solr_url + '/update/json'
        self.query_url = solr_url + '/select'
        self.headers = {"content-type": "application/json"}

    def post_items(self, items, commit=False, softCommit=False):
        ''' post a items to Solr;
         '''
        url = self.update_url
        # Check either to do soft commit or hard commit
        if commit == True:
            url = url + '?commit=true'
        elif softCommit or 'soft' == commit:
            url = url + '?softCommit=true'

        resp = requests.post(
                    url,
                    data=json.dumps(items).encode('utf-8', 'replace'),
                    headers=self.headers)


        if not resp or resp.status_code != 200:
            print('Solr posting failed')
            return False
        return True

    def commit(self):
        '''
        Commit index
        '''
        resp = requests.post(self.update_url + '?commit=true')
        if resp.status_code == 200:
            self.posted_items = 0
        return resp

    def query(self, query='*:*', start=0, rows=20, **kwargs):
        '''
        Queries solr and returns results as a dictionary
        returns None on failure, items on success
        '''
        payload = {
                   'q': query,
                    'wt': 'python',
                    'start': start,
                    'rows': rows
                   }

        if kwargs:
            for key in kwargs:
                payload[key] = kwargs.get(key)

        resp = requests.get(self.query_url, params=payload)
        if resp.status_code == 200:
            return eval(resp.text)
        else:
            print(resp.status_code)
            return None

    def query_raw(self, query='*:*', start=0, rows=20, **kwargs):
        '''
        Queries solr server and returns raw Solr resonse
        '''
        payload = {
                   'q': query,
                    'wt': 'python',
                    'start': start,
                    'rows': rows
                   }

        if kwargs:
            for key in kwargs:
                payload[key] = kwargs.get(key)

        return requests.get(self.query_url, params=payload)

    def query_iterator(self, query='*:*', start=0, rows=20, **kwargs):
        '''
        Queries solr server and returns Solr response  as dictionary
        returns None on failure, iterator of results on success
        '''
        payload = {
                   'q': query,
                    'wt': 'python',
                    'rows': rows
                   }

        if kwargs:
            for key in kwargs:
                payload[key] = kwargs.get(key)

        total = start + 1
        while start < total:
            payload['start'] = start
            print('start = %s, total= %s' % (start, total))
            resp = requests.get(self.query_url, params=payload)
            if not resp:
                print('no response from solr server!')
                break

            if resp.status_code == 200:
                resp = eval(resp.text)
                total = resp['response']['numFound']
                for doc in resp['response']['docs']:
                    start += 1
                    yield doc
            else:
                print(resp)
                print('Oops! Some thing went wrong while querying solr')
                print('Solr query params = %s', payload)
                break

    def __del__(self):
        ''' commit pending docs before close '''
        print('SolrPipeline: commit pending docs before close ...')
        print('SolrPipeline: status = ', self.commit())


if __name__ == '__main__':
    solr = Solr("http://localhost:8983/solr")
    docs = solr.query_iterator(fl="id")
    for doc in docs:
        print(doc)
    print('Done')

