"""Add an idempotent bank of present-simple exercises, preserving old indexes."""
import json
import server

def bank():
    out=[]
    def add(group,prompt,answer,why,options=None,accepted=None):
        q=dict(category='grammar',group=group,type='choice' if options else 'write',prompt=prompt,answer=answer,explanation=why)
        if options: q['options']=options
        if accepted: q['accepted']=accepted
        out.append(q)
    verbs=[('She','study','studies','English every evening','Phụ âm + y: đổi y thành ies.'),('He','watch','watches','TV after dinner','Động từ kết thúc bằng ch: thêm es.'),('My sister','go','goes','to school by bus','Go thêm es thành goes.'),('Tom','play','plays','football on Sundays','Nguyên âm + y: giữ y và thêm s.'),('The teacher','teach','teaches','English','Động từ kết thúc bằng ch: thêm es.'),('My father','work','works','in a hospital','Chủ ngữ số ít: thêm s.'),('The bus','stop','stops','near my house','Chủ ngữ số ít: thêm s.'),('She','have','has','breakfast at seven','Have đổi thành has với he/she/it.'),('He','do','does','his homework after school','Do đổi thành does với he/she/it.'),('My brother','wash','washes','the dishes','Động từ kết thúc bằng sh: thêm es.'),('Anna','read','reads','before bed','Chủ ngữ số ít: thêm s.'),('The baby','cry','cries','at night','Phụ âm + y: đổi y thành ies.')]
    for subject,base,form,tail,rule in verbs:
        add('Chia động từ',f'Điền dạng đúng: {subject} ___ ({base}) {tail}.',form,f'{subject} là ngôi thứ ba số ít. {rule} Câu đúng: {subject} {form} {tail}.')
    negatives=[('I','like','coffee','don’t','do not'),('She','eat','meat','doesn’t','does not'),('They','live','here','don’t','do not'),('He','drive','to work','doesn’t','does not'),('We','study','on Sundays','don’t','do not'),('My mother','watch','TV at night','doesn’t','does not'),('You','need','a ticket','don’t','do not'),('Tom','play','tennis','doesn’t','does not'),('The children','go','to school on Sundays','don’t','do not'),('This shop','open','on Mondays','doesn’t','does not'),('My parents','work','at night','don’t','do not'),('The dog','sleep','in the kitchen','doesn’t','does not')]
    for sub,v,tail,short,long in negatives:
        add('Câu phủ định',f'Điền trợ động từ phủ định (dạng đầy đủ): {sub} ___ {v} {tail}.',long,f'Dùng {long} với {sub}. Sau trợ động từ, {v} giữ nguyên mẫu.',accepted=[short,short.replace('’',"'")])
    subjects=[('you','like music','Do'),('she','speak English','Does'),('they','work here','Do'),('he','play the guitar','Does'),('your parents','live nearby','Do'),('your sister','study French','Does'),('we','need a pen','Do'),('the library','open at nine','Does'),('these students','read every day','Do'),('your father','cook dinner','Does'),('the train','stop here','Does'),('I','need a dictionary','Do')]
    for sub,tail,answer in subjects:
        add('Câu hỏi',f'Chọn trợ động từ: ___ {sub} {tail}?',answer,f'Chủ ngữ “{sub}” dùng {answer.lower()} trong câu hỏi hiện tại đơn. Động từ chính giữ nguyên mẫu.',['Do','Does','Is','Are'])
    corrections=[("She don't like tea.","She doesn't like tea.",'She dùng doesn’t.'),("He doesn't plays football.","He doesn't play football.",'Sau doesn’t dùng play nguyên mẫu.'),('Does she studies English?','Does she study English?','Sau does dùng study nguyên mẫu.'),('They goes to school.','They go to school.','They dùng động từ nguyên mẫu go.'),('My brother watch TV.','My brother watches TV.','My brother là số ít; watch thêm es.'),('I likes this book.','I like this book.','I dùng like nguyên mẫu.'),('Do he work here?','Does he work here?','He dùng does trong câu hỏi.'),('She have a notebook.','She has a notebook.','Have đổi thành has với she.'),('We does not study at night.','We do not study at night.','We dùng do not.'),('The baby cry every night.','The baby cries every night.','Chủ ngữ số ít; cry đổi y thành ies.'),('Does your parents live here?','Do your parents live here?','Your parents là số nhiều; dùng do.'),('He go to work by bus.','He goes to work by bus.','He dùng goes.')]
    for bad,good,why in corrections:
        variants=[good.replace("doesn't",'does not').replace("don't",'do not'),good.replace('do not',"don't").replace('does not',"doesn't")]
        add('Sửa lỗi',f'Viết lại cho đúng (chỉ sửa lỗi ngữ pháp): {bad}',good,why+' Câu đúng: '+good,accepted=variants)
    ordered=[('every day / I / English / study','I study English every day.'),('reads / she / every evening','She reads every evening.'),('do / live / where / you','Where do you live?'),('does / he / what / do','What does he do?'),('not / we / do / work / on Sundays','We do not work on Sundays.'),('at seven / gets up / she','She gets up at seven.'),('English / does / speak / your brother','Does your brother speak English?'),('they / after school / play / football','They play football after school.'),('does / not / he / coffee / drink','He does not drink coffee.'),('you / do / when / study','When do you study?'),('my mother / dinner / cooks / every day','My mother cooks dinner every day.'),('on Mondays / the shop / opens','The shop opens on Mondays.')]
    for pieces,answer in ordered:
        accepted=[]
        if 'every day' in answer: accepted.append('Every day, '+answer.replace(' every day','')[0].lower()+answer.replace(' every day','')[1:])
        add('Sắp xếp câu',f'Sắp xếp thành câu, bắt đầu bằng chủ ngữ (câu hỏi bắt đầu bằng từ hỏi hoặc trợ động từ): {pieces}',answer,'Câu mẫu: '+answer+' Câu kể: chủ ngữ + động từ + phần còn lại. Câu hỏi: (từ hỏi) + do/does + chủ ngữ + động từ nguyên mẫu.',accepted=accepted)
    return out

def extend(lesson):
    for q in lesson['questions']:
        if 'category' not in q:
            q['category']='grammar' if q['prompt'] in ['She ___ English every day.','Chọn câu đúng.','Điền dạng đúng: He ___ (study) every evening.'] else 'vocabulary'
    prompts={q['prompt'] for q in lesson['questions']}
    lesson['questions'].extend(q for q in bank() if q['prompt'] not in prompts)
    return lesson

if __name__=='__main__':
    path=server.ROOT/'sample.json'
    path.write_text(json.dumps(extend(json.loads(path.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with server.connect() as db:
        for row in db.execute('SELECT id,payload FROM lessons').fetchall():
            lesson=json.loads(row['payload'])
            if lesson['title']!='A little space to focus': continue
            extend(lesson)
            db.execute('UPDATE lessons SET payload=? WHERE id=?',(json.dumps(lesson,ensure_ascii=False),row['id']))
            print('Grammar exercises:',sum(q.get('category')=='grammar' for q in lesson['questions']))
