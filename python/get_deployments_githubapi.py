import requests
import os
import json
from pathlib import Path
from pandas import DataFrame


def get(url: str):
    api_key = ''

    # Save to file to prevent API usage limit.
    file = Path(f'data/{url.split("/")[-2]}.json')
    if file.is_file():
        with file.open('r', encoding='utf-8') as f:
            j = json.load(f)
        return j

    headers = {'Authorization': f'Bearer {api_key}'} if api_key else None
    r = requests.get(url, params={'per_page': 100},
                     headers=headers, timeout=1000)

    if not r.ok:
        raise RuntimeError(
            f'Failed to {r.request.method} url {r.url}. Content: {r.content}')

    with file.open('w', encoding='utf-8') as f:
        json.dump(r.json(), f)

    return r.json()


def get_dataframe(owner: str, repo: str):
    d_url = f'https://api.github.com/repos/{owner}/{repo}/deployments'

    # Labels
    lbl_env = 'Environment'
    lbl_status = 'Status'
    lbl_success = 'Success'
    lbl_failed = 'Failed'

    sts = [{'url': x['statuses_url'],
            lbl_env: x['environment'],
            'id': x['id']}
           for x in get(d_url) if x['task'] == 'deploy']
    tt = len(sts)
    print(f'Found {tt} deployments. Getting details...')
    rs = []
    for i, u in enumerate(sts):
        pp = int((100*i/tt))
        print('▇'*pp + '.'*(100-pp) + f'{pp}%')
        
        rs.append({'id': u['id'],
                   lbl_env: u[lbl_env],
                   lbl_status: int('success' in ''.join([s['state'] for s in get(u['url'])]))})

    df: DataFrame = DataFrame.from_records(rs).sort_values(by=lbl_env)

    df[lbl_status] = df[lbl_status].replace({1: lbl_success, 0: lbl_failed})

    s = df.groupby(lbl_status).size().fillna(0)
    s['Success (%)'] = (s[lbl_success] /
                        (s[lbl_failed] + s[lbl_success])) * 100

    e = df.groupby([lbl_env, lbl_status]).size().unstack().fillna(0)
    e['Success (%)'] = (e[lbl_success] /
                        (e[lbl_failed] + e[lbl_success])) * 100

    print(s.to_string())
    print(e)


try:
    get_dataframe('AgroMart', 'api')
except RuntimeError as e:
    print(e)
