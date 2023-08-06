import re
from jinja2.ext import Extension
import requests
import requests_cache

requests_cache.install_cache(cache_name='orcid_cache', backend='sqlite',
                             expire_after=180, use_temp=True)


def is_orcid(orcid: str):
    pattern = re.compile(r'^https://orcid.org/\d{4}-\d{4}-\d{4}-\d{4}$')
    return True if pattern.match(orcid) else False


def get_orcid_record(orcid: str):
    if not is_orcid(orcid):
        raise ValueError("{orcid} is not a valid ORCID".format(orcid=orcid))

    r = requests.get(orcid, headers={'Accept': 'application/json'})
    if r.status_code == 200:
        record = r.json()
        rd = {
            'family_name': record['person']['name']['family-name']['value'],
            'given_names': record['person']['name']['given-names']['value']
            }
        if record['person']['name']['credit-name']:
            rd['name'] = record['person']['name']['credit-name']['value']
        else:
            rd['name'] = rd['given_names'] + ' ' + rd['family_name']
    else:
        m = 'HTTP request to orcid.org returned with status code {code}'
        raise Exception(m.format(code=r.status_code))
    return rd


def orcid_full_credit(orcid: str):
    name = get_orcid_record(orcid)['name']
    label = '{name} ({orcid})'.format(name=name, orcid=orcid)
    return label


def orcid_family_name(orcid: str):
    return get_orcid_record(orcid)['family_name']


def orcid_given_names(orcid: str):
    return get_orcid_record(orcid)['given_names']


class OrcidExtension(Extension):

    def __init__(self, environment):
        super(OrcidExtension, self).__init__(environment)
        environment.filters['orcid_full_credit'] = orcid_full_credit
        environment.filters['orcid_family_name'] = orcid_family_name
        environment.filters['orcid_given_names'] = orcid_given_names
