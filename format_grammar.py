"""Structure the existing lesson without changing exercise history."""
import json
import server

sections = [
    {'title':'Khi nào dùng?', 'items':['Diễn tả thói quen hoặc việc lặp lại: học mỗi ngày, đọc sách mỗi tối.','Diễn tả sự thật hoặc điều thường đúng.'], 'hint':'Dấu hiệu thường gặp: every day, every morning, usually, often, always.'},
    {'title':'Công thức', 'columns':['Dạng câu','I / You / We / They','He / She / It'], 'rows':[
        ['Khẳng định','Chủ ngữ + V nguyên mẫu','Chủ ngữ + V-s / V-es'],
        ['Phủ định','Chủ ngữ + do not (don’t) + V','Chủ ngữ + does not (doesn’t) + V'],
        ['Câu hỏi','Do + chủ ngữ + V?','Does + chủ ngữ + V?']
    ], 'hint':'V = động từ nguyên mẫu. Bảng này áp dụng với động từ thường; động từ be có cách chia riêng: am / is / are.'},
    {'title':'Ví dụ dễ nhớ', 'examples':[
        {'en':'I study English every day.','vi':'Tôi học tiếng Anh mỗi ngày.'},
        {'en':'She studies English every day.','vi':'Cô ấy học tiếng Anh mỗi ngày.'},
        {'en':'She doesn’t study at night.','vi':'Cô ấy không học vào buổi tối.'},
        {'en':'Does she study every day?','vi':'Cô ấy có học mỗi ngày không?'}
    ]},
    {'title':'Lưu ý để tránh nhầm', 'items':['Sau do / does / don’t / doesn’t, luôn dùng động từ nguyên mẫu.','Với he / she / it: study → studies (phụ âm + y → ies); practice → practices (thêm s).'], 'contrast':{'wrong':'She doesn’t studies at night.','right':'She doesn’t study at night.'}}
]

def update(lesson):
    if lesson.get('grammar',{}).get('title','').startswith('Present simple'):
        lesson['grammar']['sections']=sections
    return lesson

if __name__=='__main__':
    path=server.ROOT/'sample.json'
    path.write_text(json.dumps(update(json.loads(path.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with server.connect() as db:
        for row in db.execute('SELECT id,payload FROM lessons').fetchall():
            lesson=update(json.loads(row['payload']))
            db.execute('UPDATE lessons SET payload=? WHERE id=?',(json.dumps(lesson,ensure_ascii=False),row['id']))
