import requests
from pandas import DataFrame


def get(url: str):
    api_key = ''

    headers = {'Authorization': f'Bearer {api_key}'} if api_key else None
    r = requests.get(url, params={'per_page': 100},
                     headers=headers, timeout=1000)

    if not r.ok:
        raise RuntimeError(
            f'Failed to {r.request.method} url {r.url}. Content: {r.content}')
    return r.json()


def get_dataframe():
    owner, repo = 'AgroMart', 'api'
    d_url = f'https://api.github.com/repos/{owner}/{repo}/deployments'

    sts = [{'url': x['statuses_url'],
            'Environment': x['environment'],
            'id': x['id']}
           for x in get(d_url) if x['task'] == 'deploy']
    tt = len(sts)
    print(f'Found {tt} deployments. Getting details...')
    rs = [{'id': u['id'],
           'Environment': u['Environment'],
           'Status': int('success' in ''.join([s['state']
                                               for s in get(u['url'])]))}
          for u in sts]

    df: DataFrame = DataFrame.from_records(rs).sort_values(by='Environment')

    df['Status'] = df['Status'].replace({1: 'Success', 0: 'Failed'})

    s = df.groupby('Status').size().fillna(0)
    s['Success (%)'] = (s['Success'] /
                        (s['Failed'] + s['Success'])) * 100

    e = df.groupby(['Environment', 'Status']).size().unstack().fillna(0)
    e['Success (%)'] = (e['Success'] /
                        (e['Failed'] + e['Success'])) * 100

    print(s.to_csv())
    print(e.to_csv())


try:
    get_dataframe()
except RuntimeError as e:
    print(e)
