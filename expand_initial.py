"""Extend the initial lesson without replacing any learning history."""
import json, uuid
import server

ADDITIONS = [
    ('chair','/tʃer/','ghế','I sit on a chair when I study.'),
    ('keyboard','/ˈkiːbɔːrd/','bàn phím','I type on my keyboard.'),
    ('screen','/skriːn/','màn hình','I read the question on the screen.'),
    ('pencil','/ˈpensəl/','bút chì','I draw with a pencil.'),
    ('dictionary','/ˈdɪkʃəneri/','từ điển','I use a dictionary to check new words.'),
    ('lesson','/ˈlesən/','bài học','This lesson has twenty new words.'),
    ('question','/ˈkwestʃən/','câu hỏi','I ask a question when I need help.'),
    ('answer','/ˈænsər/','câu trả lời','I write my answer in the notebook.'),
    ('remember','/rɪˈmembər/','nhớ, ghi nhớ','I remember this word.'),
    ('review','/rɪˈvjuː/','ôn lại','I review new words every morning.'),
    ('listen','/ˈlɪsən/','lắng nghe','I listen to English every day.'),
    ('repeat','/rɪˈpiːt/','lặp lại, nhắc lại','I repeat the sentence three times.'),
]

def expand(lesson):
    existing={w['word'] for w in lesson['words']}
    for word,ipa,meaning,example in ADDITIONS:
        if word not in existing:
            lesson['words'].append(dict(word=word,ipa=ipa,meaning=meaning,example=example))
    lesson['description']='Ngày 01 · 20 từ về góc học tập và thói quen học tiếng Anh'
    # Append questions only: earlier question indexes and recorded answers stay valid.
    prompts={q['prompt'] for q in lesson['questions']}
    for i,w in enumerate(lesson['words']):
        prompt=f'Từ nào có nghĩa là “{w["meaning"]}”?' if i%2==0 else f'Viết từ tiếng Anh: {w["meaning"]}.'
        if prompt in prompts: continue
        q=dict(type='choice' if i%2==0 else 'write',prompt=prompt,answer=w['word'],explanation=f'{w["word"]}: {w["meaning"]}. Ví dụ: {w["example"]}')
        if q['type']=='choice':
            choices=[w['word']]+[x['word'] for x in lesson['words'] if x['word']!=w['word']][:3]
            offset=i%4
            q['options']=choices[offset:]+choices[:offset]
        lesson['questions'].append(q)
    return lesson

if __name__=='__main__':
    source=server.ROOT/'sample.json'
    sample=expand(json.loads(source.read_text(encoding='utf-8')))
    source.write_text(json.dumps(sample,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    server.init()
    with server.connect() as db:
        rows=db.execute('SELECT id,payload FROM lessons').fetchall()
        for row in rows:
            lesson=json.loads(row['payload'])
            if lesson['title']!='A little space to focus': continue
            previous={w['word'] for w in lesson['words']}
            expand(lesson)
            db.execute('UPDATE lessons SET payload=? WHERE id=?',(json.dumps(lesson,ensure_ascii=False),row['id']))
            for w in lesson['words']:
                if w['word'] not in previous:
                    db.execute('INSERT INTO reviews VALUES(?,?,?,?,?,0)',(uuid.uuid4().hex,w['word'],w['meaning'],w['example'],str(server.today())))
            print(f'Đã lưu: {len(lesson["words"])} từ, {len(lesson["questions"])} câu luyện tập; giữ nguyên lịch sử.')
