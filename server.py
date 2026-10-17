import json, sqlite3, datetime, pathlib, uuid, os
from contextlib import contextmanager
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = pathlib.Path(__file__).resolve().parent
DB = pathlib.Path(os.environ.get('DATABASE_PATH', str(ROOT / 'data' / 'learning.sqlite3')))

@contextmanager
def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()

def today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).date()

def init():
    DB.parent.mkdir(parents=True,exist_ok=True)
    with connect() as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS lessons(id TEXT PRIMARY KEY, title TEXT, payload TEXT, created TEXT);
        CREATE TABLE IF NOT EXISTS reviews(id TEXT PRIMARY KEY, word TEXT, meaning TEXT, example TEXT, due TEXT, streak INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, day TEXT, lesson TEXT, question TEXT, answer TEXT, correct INTEGER, explanation TEXT);
        CREATE TABLE IF NOT EXISTS sessions(day TEXT PRIMARY KEY, seconds INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY, day TEXT, body TEXT);''')
        if not db.execute('SELECT 1 FROM lessons').fetchone():
            save_lesson(db, json.loads((ROOT / 'sample.json').read_text(encoding='utf-8')))
            from add_topics import pack, IT, IT_PHRASES, DAILY, DAILY_PHRASES
            for lesson in [pack('Tiếng Anh IT','IT · Lập trình & làm việc cùng đội nhóm',IT,IT_PHRASES), pack('Giao tiếp đời thường','Daily English · Những cuộc trò chuyện mỗi ngày',DAILY,DAILY_PHRASES)]:
                save_lesson(db,lesson)

def save_lesson(db, lesson):
    from grammar_catalog import apply
    if not isinstance(lesson, dict) or not isinstance(lesson.get('title'), str) or not lesson['title'].strip():
        raise ValueError('Bài học cần title.')
    words, questions = lesson.get('words'), lesson.get('questions')
    if not isinstance(words, list) or not words or not isinstance(questions, list) or not questions:
        raise ValueError('Bài học cần danh sách words và questions không rỗng.')
    for w in words:
        if not isinstance(w, dict) or not all(isinstance(w.get(k), str) and w[k].strip() for k in ['word','meaning','example']):
            raise ValueError('Mỗi từ cần word, meaning, example.')
    for q in questions:
        if not isinstance(q, dict) or q.get('type') not in ['choice','write','listen'] or not all(isinstance(q.get(k), str) and q[k].strip() for k in ['prompt','answer','explanation']):
            raise ValueError('Câu hỏi cần type (choice/write/listen), prompt, answer, explanation.')
        if q['type'] == 'choice' and (not isinstance(q.get('options'), list) or q['answer'] not in q['options']):
            raise ValueError('Đáp án phải nằm trong options.')
        if q['type'] == 'listen' and not isinstance(q.get('audio'),str):
            raise ValueError('Bài nghe cần audio là câu tiếng Anh để đọc.')
    grammar = lesson.get('grammar', {})
    if not isinstance(grammar,dict) or not all(isinstance(grammar.get(k,''),str) for k in ['title','body']):
        raise ValueError('grammar cần title và body dạng chữ.')
    lesson = apply(lesson)
    key = uuid.uuid4().hex
    db.execute('INSERT INTO lessons VALUES(?,?,?,?)',(key,lesson['title'],json.dumps(lesson,ensure_ascii=False),str(today())))
    for w in words:
        db.execute('INSERT INTO reviews VALUES(?,?,?,?,?,0)',(uuid.uuid4().hex,w['word'],w['meaning'],w['example'],str(today())))
    return key

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT / 'web'),**kw)
    def reply(self, value, status=200):
        data=json.dumps(value,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path == '/api/state':
            with connect() as db:
                result={ 'today':str(today()), 'lessons':[dict(r) for r in db.execute('SELECT * FROM lessons ORDER BY rowid DESC')], 'reviews':[dict(r) for r in db.execute('SELECT * FROM reviews ORDER BY due')], 'attempts':[dict(r) for r in db.execute('SELECT * FROM attempts ORDER BY id DESC')], 'sessions':[dict(r) for r in db.execute('SELECT * FROM sessions ORDER BY day DESC')], 'notes':[dict(r) for r in db.execute('SELECT * FROM notes ORDER BY id DESC')] }
                for l in result['lessons']: l['payload']=json.loads(l['payload'])
                return self.reply(result)
        if self.path.startswith('/api/'): return self.reply({'error':'Không tìm thấy'},404)
        super().do_GET()
    def do_POST(self):
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size > 2_000_000: raise ValueError('Dữ liệu vượt quá 2 MB.')
            data=json.loads(self.rfile.read(size))
            with connect() as db:
                if self.path == '/api/answer':
                    row=db.execute('SELECT payload FROM lessons WHERE id=?',(data['lesson'],)).fetchone()
                    if not row: raise ValueError('Không tìm thấy bài học.')
                    q=json.loads(row[0])['questions'][int(data['index'])]
                    normalize=lambda s:' '.join(str(s).strip().casefold().rstrip('.!?').split())
                    correct=normalize(data['answer']) in [normalize(x) for x in [q['answer']]+q.get('accepted',[])]
                    db.execute('INSERT INTO attempts(day,lesson,question,answer,correct,explanation) VALUES(?,?,?,?,?,?)',(str(today()),data['lesson'],q['prompt'],str(data['answer']),int(correct),q['explanation']))
                    result={'correct':correct,'answer':q['answer'],'explanation':q['explanation']}
                elif self.path == '/api/review':
                    row=db.execute('SELECT * FROM reviews WHERE id=?',(data['id'],)).fetchone()
                    if not row: raise ValueError('Không tìm thấy từ.')
                    streak=min(row['streak']+1,6) if data['remember'] else 0
                    days=[0,1,3,7,14,30,60][streak]
                    db.execute('UPDATE reviews SET streak=?,due=? WHERE id=?',(streak,str(today()+datetime.timedelta(days=days)),data['id']))
                    result={'ok':True}
                elif self.path == '/api/time':
                    seconds=max(0,min(90,int(data['seconds'])))
                    db.execute('INSERT INTO sessions VALUES(?,?) ON CONFLICT(day) DO UPDATE SET seconds=seconds+excluded.seconds',(str(today()),seconds)); result={'ok':True}
                elif self.path == '/api/note':
                    body=str(data['body']).strip()
                    if not body or len(body)>20000: raise ValueError('Ghi chú cần từ 1 đến 20.000 ký tự.')
                    db.execute('INSERT INTO notes(day,body) VALUES(?,?)',(str(today()),body)); result={'ok':True}
                else: return self.reply({'error':'Không tìm thấy'},404)
            self.reply(result)
        except (ValueError,KeyError,TypeError,IndexError) as e: self.reply({'error':str(e)},400)

if __name__ == '__main__':
    init()
    host=os.environ.get('HOST','127.0.0.1')
    port=int(os.environ.get('PORT','8765'))
    print(f'English Garden: http://{host}:{port}',flush=True)
    ThreadingHTTPServer((host,port),Handler).serve_forever()
