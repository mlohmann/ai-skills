import unittest,json,sys,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'skills/job-search-jev/scripts'))
from jobscout import rank,request,validate
class Tests(unittest.TestCase):
 def setUp(self):
  self.p=json.loads((root/'skills/job-search-jev/assets/profile.template.json').read_text())
  self.j={'company':'Example','requisition_id':'1','title':'Nurse','employer_url':'https://example.org/jobs/1','role_eligible':True,'seniority_eligible':True,'location_eligible':True,'work_model_eligible':True,'active':True,'employer_verified':True,'evaluation':{'provider':'jev','scores':{c['id']:80 for c in self.p['criteria']},'confidence':.9}}
 def runjob(self,j=None,h=None):return rank(self.p,[j or self.j],[] if h is None else h)
 def test_generic_profile(self):
  self.p['target_roles']=['Nurse'];self.p['salary']['currency']='EUR'
  self.assertEqual(len(self.runjob()['shortlist']),1)
  payload=request(self.p,self.j);self.assertEqual(payload['questions']['skills_fit']['type'],'score');self.assertEqual(len(payload['questions']['skills_fit']['criteria']),5)
 def test_salary_boundaries(self):
  self.p['salary']['minimum']=160000;self.j['salary']={'min':150000,'max':180000,'currency':'USD','period':'year','employer_reported':True}
  self.assertEqual(len(self.runjob()['excluded']),1)
  self.p['salary']['gate']='upper_bound';self.assertEqual(len(self.runjob()['shortlist']),1)
  self.j['salary']['employer_reported']=False;self.assertEqual(len(self.runjob()['review']),1)
 def test_missing_salary(self):
  self.p['salary']['minimum']=100;self.assertEqual(len(self.runjob()['review']),1)
 def test_history_requisition_scope(self):
  self.assertEqual(len(self.runjob(h=[{'company':'EXAMPLE','requisition_id':'1','status':'applied'}])['excluded']),1)
  self.assertEqual(len(self.runjob(h=[{'company':'EXAMPLE','requisition_id':'2','status':'applied'}])['shortlist']),1)
  self.assertEqual(len(rank(self.p,[self.j])['review']),1)
 def test_unknown_and_low_confidence(self):
  self.j['location_eligible']=None;self.assertEqual(len(self.runjob()['review']),1)
  self.j['location_eligible']=True;self.j['evaluation']['confidence']=.5;self.assertEqual(len(self.runjob()['review']),1)
 def test_jev_unavailable(self):
  self.j.pop('evaluation');self.assertIn('jev_required',self.runjob()['review'][0]['reasons'])
 def test_invalid_scores(self):
  for bad in (float('nan'),True,101,None):
   self.j['evaluation']['scores']['role_fit']=bad;self.assertEqual(len(self.runjob()['review']),1)
 def test_duplicate_conflicts(self):
  other=copy.deepcopy(self.j);other['active']=False
  out=rank(self.p,[self.j,other],[]);self.assertEqual(out['duplicate_count'],1);self.assertEqual(len(out['shortlist']),0);self.assertEqual(len(out['review']),1)
 def test_exclusions_and_weight(self):
  self.p['excluded_companies']=['EXAMPLE'];self.assertEqual(len(self.runjob()['excluded']),1)
  self.p['excluded_companies']=[];self.j['evaluation']['scores']['role_fit']=100;self.assertEqual(self.runjob()['shortlist'][0]['score'],88.57)
 def test_validation(self):
  self.p['criteria'][0]['weight']=-1
  with self.assertRaises(ValueError):validate(self.p)
if __name__=='__main__':unittest.main()
