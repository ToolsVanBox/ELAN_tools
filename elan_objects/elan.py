import os
import requests
from urllib.parse import urljoin
from urllib.parse import urlencode
from elan_objects.project import Project
from elan_objects.experiment import Experiment
from elan_objects.study import Study
TIMEOUT=20

class Elan(object):

    def __init__(self, baseuri, key):

        self.baseuri = baseuri.rstrip('/') + '/'
        self.version = 'v1'
        self.cache = dict()
        self.key = key
        self.request_session = requests.Session()

        self.adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.request_session.mount('http://', self.adapter)

    def patch(self, uri, params=dict()):

        try:
            r = self.request_session.patch(uri, json=params,
                headers={
                    'Content-Type' : 'application/json',
                    'Authorization' : self.key
                },
                timeout=TIMEOUT
            )
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        #else:
        #    return

    def put(self, uri, params=dict()):

        try:
            r = self.request_session.put(uri, json=params,
                headers={
                    'Content-Type' : 'application/json',
                    'Accept' : 'application/json',
                    'Authorization' : self.key
                },
                timeout=TIMEOUT
            )
            r.raise_for_status()
            #print( r.status_code()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return r.status_code

    def get(self, uri, params=dict()):

        try:
            r = self.request_session.get(uri, params=params,
                headers={
                    'Accept' : 'application/json',
                    'X-Requested-With' : 'Swagger',
                    'Authorization' : self.key
                },
                timeout=TIMEOUT
            )
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return r.json()


    def get_projects(self, project_workdir):
        parts = ['api', self.version, 'projects']
        url = urljoin(self.baseuri, '/'.join(parts))
        r = self.get(url)
        projects = []
        for p in r['data']:
            projects.append(Project(p, project_workdir))
        return projects

    def get_studies(self, project_dir,project_id=None, study_id=None):
        parts = ['api', self.version, 'studies']
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        if project_id:
            params['projectID'] = project_id
        if study_id:
            params['studyID'] = study_id

        r = self.get(url, params)
        studies = []
        for s in r['data']:
            studies.append(Study(s, project_dir))
        return studies

    def get_sampleTypeID(self, sample_type_name=None):
        parts = ['api', self.version, 'sampleTypes']
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        if sample_type_name:
            params['name'] = sample_type_name
        r = self.get(url, params)
        sampleTypeID = r['data'][0]['sampleTypeID']
        return sampleTypeID
        # for s in r['data']:
        #     print(s)
    def get_samples_for_names(self, samplenames=None):
        parts = ['api', self.version, 'samples', 'forNames']
        url = urljoin(self.baseuri, '/'.join(parts))
        params = { '$expand': 'meta' }
        samples = []
        for name in samplenames:
            if name:
                params['names'] = name
            r = self.get(url, params)
            for s in r['data']:
                samples.append(s)
        return( samples )

    def get_samples_by_sample_type_id(self, sample_type_id=None):
        parts = ['api', self.version, 'samples']
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        if sample_type_id:
            params['sampleTypeID'] = sample_type_id
        r = self.get(url, params)
        samples = []
        for s in r['data']:
            samples.append(s)
        return( samples )

    def get_samples_by_study_name(self, study_name=None):
        parts = ['api', self.version, 'samples']
        url = urljoin(self.baseuri, '/'.join(parts))
        params = { '$expand': 'meta', 'search': study_name}
        r = self.get(url, params)
        samples = []
        for s in r['data']:
            for m in s['meta']:
                if m['key'] == 'Study Name' and m['value'] == study_name:
                    samples.append(s)
        return( samples )

    def get_meta_field_from_sample_type_by_key( self, sample_type_id=None, key=None):
        parts = ['api', self.version, 'sampleTypes',str(sample_type_id),"meta"]
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        r = self.get(url, params)
        meta_fields = []
        for m in r['data']:
            if m['key'] == key:
                meta_fields.append(m)
        return( meta_fields )

    def get_sample_meta_fields_by_key( self, sample_id=None, key=None ):
        parts = ['api', self.version, 'samples',str(sample_id),"meta"]
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        r = self.get(url, params)
        sample_meta_fields = []
        for m in r['data']:
            if m['key'] == key:
                sample_meta_fields.append(m)
        return( sample_meta_fields )

    def put_meta(self, sample_id=None, params=None):
        parts = ['api', self.version, 'samples', str(sample_id), "meta"]
        url = urljoin(self.baseuri, '/'.join(parts))
        r = self.put(url, params)
        return r

    def patch_sample(self, sample_id=None):
        parts = ['api', self.version, 'samples', str(sample_id)]
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        self.patch(url, params)

    def get_experiments(self, project_id=None, study_id=None):
        parts = ['api', self.version, 'experiments']
        url = urljoin(self.baseuri, '/'.join(parts))
        params = {}
        if project_id:
            params['projectID'] = project_id
        if study_id:
            params['studyID'] = study_id
        r = self.get(url, params)
        experiments = []
        for e in r['data']:
            experiments.append(Experiment(e))
        return experiments
    # response = request_session.get(elan_uri + '/api/v1/projects',
