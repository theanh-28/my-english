import unittest, tempfile, pathlib, json, threading, urllib.request, urllib.error
import server

class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(dir=server.ROOT)
        cls.original = server.DB
        server.DB = pathlib.Path(cls.temp.name) / 'test.sqlite3'
        server.init()
        cls.http = server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        cls.thread = threading.Thread(target=cls.http.serve_forever,daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:'+str(cls.http.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown(); cls.http.server_close(); cls.thread.join()
        server.DB=cls.original; cls.temp.cleanup()
    def request(self,path,data=None):
        req=urllib.request.Request(self.url+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as r: return json.load(r)
    def test_answer_saved_and_normalized(self):
        s=self.request('/api/state'); lid=next(l['id'] for l in s['lessons'] if l['title']=='A little space to focus')
        result=self.request('/api/answer',{'lesson':lid,'index':1,'answer':'  NOTEBOOK! '})
        self.assertTrue(result['correct'])
        self.assertEqual(self.request('/api/state')['attempts'][0]['answer'],'  NOTEBOOK! ')
    def test_review_is_persisted(self):
        word=self.request('/api/state')['reviews'][0]
        self.request('/api/review',{'id':word['id'],'remember':True})
        with server.connect() as db:
            row=db.execute('SELECT * FROM reviews WHERE id=?',(word['id'],)).fetchone()
            self.assertEqual(row['streak'],1)
            self.assertGreater(row['due'],str(server.today()))
    def test_bad_import_is_atomic(self):
        before=len(self.request('/api/state')['lessons'])
        with self.assertRaises(ValueError):
            with server.connect() as db: server.save_lesson(db,{'title':'bad','words':[],'questions':[]})
        self.assertEqual(len(self.request('/api/state')['lessons']),before)
    def test_import_and_time_and_note(self):
        lesson=json.loads((server.ROOT/'sample.json').read_text(encoding='utf-8'))
        with server.connect() as db: key=server.save_lesson(db,lesson)
        self.request('/api/time',{'seconds':20})
        self.request('/api/note',{'body':'Hôm nay học notebook.'})
        s=self.request('/api/state')
        self.assertTrue(any(l['id']==key for l in s['lessons']))
        self.assertEqual(s['sessions'][0]['seconds'],20)
        self.assertEqual(s['notes'][0]['body'],'Hôm nay học notebook.')
    def test_web_cannot_import_lessons(self):
        with self.assertRaises(urllib.error.HTTPError) as error: self.request('/api/import',{})
        self.assertEqual(error.exception.code,404)
    def test_static(self):
        with urllib.request.urlopen(self.url+'/') as r: self.assertIn(b'English Garden',r.read())

if __name__=='__main__': unittest.main()
