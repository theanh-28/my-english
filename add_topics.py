"""Assistant-authored topic packs. Running again does not duplicate lessons."""
import json
import server

IT=[
('software','/ˈsɔːftwer/','phần mềm','We update the software every month.'),
('hardware','/ˈhɑːrdwer/','phần cứng','This problem affects the hardware.'),
('database','/ˈdeɪtəbeɪs/','cơ sở dữ liệu','We store user information in a database.'),
('server','/ˈsɜːrvər/','máy chủ','The server handles incoming requests.'),
('client','/ˈklaɪənt/','ứng dụng khách','The client sends a request to the server.'),
('network','/ˈnetwɜːrk/','mạng','The office network is slow today.'),
('function','/ˈfʌŋkʃən/','hàm','This function returns a number.'),
('variable','/ˈveriəbəl/','biến','This variable stores the current score.'),
('array','/əˈreɪ/','mảng','The array contains five items.'),
('string','/strɪŋ/','chuỗi ký tự','The username is a string.'),
('bug','/bʌɡ/','lỗi phần mềm','We found a bug in the login form.'),
('debug','/ˌdiːˈbʌɡ/','gỡ lỗi','I debug the application with my teammate.'),
('deploy','/dɪˈplɔɪ/','triển khai','We deploy the application on Fridays.'),
('request','/rɪˈkwest/','yêu cầu gửi đến hệ thống','The server receives a request.'),
('response','/rɪˈspɑːns/','phản hồi của hệ thống','The response contains the requested data.'),
('repository','/rɪˈpɑːzətɔːri/','kho mã nguồn','We keep the code in a repository.'),
('branch','/bræntʃ/','nhánh mã nguồn','Create a branch for the new feature.'),
('commit','/kəˈmɪt/','bản ghi thay đổi trong Git','This commit fixes the login issue.'),
('merge','/mɜːrdʒ/','hợp nhất','We merge the branch after review.'),
('backup','/ˈbækʌp/','bản sao lưu','We create a backup every night.')]
DAILY=[
('greet','/ɡriːt/','chào hỏi','I greet my neighbors every morning.'),
('introduce','/ˌɪntrəˈduːs/','giới thiệu','Let me introduce my friend.'),
('neighbor','/ˈneɪbər/','hàng xóm','My neighbor is very friendly.'),
('appointment','/əˈpɔɪntmənt/','cuộc hẹn','I have an appointment at ten.'),
('available','/əˈveɪləbəl/','rảnh, có thể gặp','Are you available this afternoon?'),
('busy','/ˈbɪzi/','bận rộn','I am busy right now.'),
('hungry','/ˈhʌŋɡri/','đói','I am hungry after work.'),
('thirsty','/ˈθɜːrsti/','khát','Are you thirsty?'),
('order','/ˈɔːrdər/','gọi món','I would like to order lunch.'),
('menu','/ˈmenjuː/','thực đơn','Could I see the menu?'),
('bill','/bɪl/','hóa đơn thanh toán','Could we have the bill, please?'),
('receipt','/rɪˈsiːt/','biên lai','Can I have a receipt?'),
('directions','/dəˈrekʃənz/','chỉ dẫn đường đi','Could you give me directions?'),
('nearby','/ˌnɪrˈbaɪ/','ở gần','Is there a pharmacy nearby?'),
('straight','/streɪt/','thẳng','Go straight and turn left.'),
('invite','/ɪnˈvaɪt/','mời','I want to invite you to dinner.'),
('prefer','/prɪˈfɜːr/','thích hơn','I prefer tea to coffee.'),
('recommend','/ˌrekəˈmend/','gợi ý, đề xuất','What do you recommend?'),
('excuse','/ɪkˈskjuːz/','xin thứ lỗi','Excuse me, is this seat taken?'),
('welcome','/ˈwelkəm/','chào đón','Welcome to our home.')]
IT_PHRASES=[
('Could you review my code?','Bạn có thể xem giúp mã của tôi không?','Nhờ đồng nghiệp review code'),
('I am working on the login feature.','Tôi đang làm tính năng đăng nhập.','Báo cáo việc đang làm'),
('I found a bug in the application.','Tôi phát hiện một lỗi trong ứng dụng.','Báo lỗi'),
('How can I reproduce this issue?','Làm thế nào để tái hiện lỗi này?','Hỏi cách tái hiện lỗi'),
('The server is down.','Máy chủ đang ngừng hoạt động.','Báo sự cố'),
('Could you share the error message?','Bạn gửi giúp thông báo lỗi được không?','Xin thông tin lỗi'),
('I have pushed my changes.','Tôi đã đẩy các thay đổi lên kho mã.','Cập nhật công việc'),
('Let me check the logs.','Để tôi kiểm tra nhật ký hệ thống.','Điều tra sự cố'),
('When can we deploy this update?','Khi nào chúng ta có thể triển khai bản cập nhật này?','Hỏi lịch triển khai'),
('I need more time to test this.','Tôi cần thêm thời gian để kiểm thử phần này.','Trao đổi tiến độ'),
('Can you help me resolve this conflict?','Bạn giúp tôi xử lý xung đột này được không?','Nhờ xử lý xung đột mã'),
('The fix is ready for review.','Bản sửa lỗi đã sẵn sàng để xem xét.','Báo hoàn thành bản sửa')]
DAILY_PHRASES=[
('How is your day going?','Hôm nay bạn thế nào?','Bắt chuyện'),
('Nice to meet you.','Rất vui được gặp bạn.','Lần đầu gặp mặt'),
('Could you say that again?','Bạn nói lại được không?','Nhờ nhắc lại'),
('Could you speak more slowly?','Bạn nói chậm hơn được không?','Nhờ nói chậm'),
('I would like a cup of coffee, please.','Cho tôi một tách cà phê.','Gọi đồ uống lịch sự'),
('Could we have the bill, please?','Cho chúng tôi xin hóa đơn.','Thanh toán ở nhà hàng'),
('How much does this cost?','Cái này giá bao nhiêu?','Hỏi giá'),
('Is there a pharmacy nearby?','Có hiệu thuốc nào gần đây không?','Hỏi địa điểm'),
('Would you like to have lunch together?','Bạn có muốn ăn trưa cùng không?','Mời ăn trưa'),
('Sorry, I am running late.','Xin lỗi, tôi đang bị trễ.','Báo đến muộn'),
('No worries.','Không sao đâu.','Đáp lại lời xin lỗi thân mật'),
('See you tomorrow.','Hẹn gặp bạn ngày mai.','Chào tạm biệt')]

def pack(topic,title,rows,phrases):
    words=[dict(word=w,ipa=ipa,meaning=m,example=e) for w,ipa,m,e in rows]
    questions=[]
    for i,w in enumerate(words):
        choices=[w['meaning']]+[x['meaning'] for x in words if x!=w][:3]
        shift=i%4;choices=choices[shift:]+choices[:shift]
        explanation=f'{w["word"]}: {w["meaning"]}. Ví dụ: {w["example"]}'
        questions.extend([
            dict(type='choice',category='vocabulary',group='Nhận biết nghĩa',prompt=f'Trong chủ đề này, “{w["word"]}” nghĩa là gì?',answer=w['meaning'],options=choices,explanation=explanation),
            dict(type='write',category='vocabulary',group='Nhớ từ',prompt=f'Viết từ tiếng Anh: {w["meaning"]}.',answer=w['word'],explanation=explanation),
            dict(type='listen',category='vocabulary',group='Nghe từ',prompt=f'Nghe và viết từ số {i+1} trong chủ đề {topic}.',audio=w['word'],answer=w['word'],explanation=explanation)])
    for i,(en,vi,context) in enumerate(phrases):
        distractors=[p[0] for p in phrases if p[0]!=en][:3]
        options=[en]+distractors;shift=i%4;options=options[shift:]+options[:shift]
        questions.extend([
            dict(type='choice',category='conversation',group='Chọn câu giao tiếp',prompt=f'{context}: chọn câu phù hợp với ý “{vi}”.',answer=en,options=options,explanation=f'{en} — {vi} Dùng khi: {context.lower()}.'),
            dict(type='listen',category='conversation',group='Nghe câu giao tiếp',prompt=f'Nghe và viết lại câu giao tiếp số {i+1} ({context.lower()}).',audio=en,answer=en,explanation=f'{en} — {vi}')])
    grammar={'title':'Could you…? · Nhờ vả lịch sự','body':'Could you + động từ nguyên mẫu…? Dùng để nhờ ai đó làm một việc một cách lịch sự.','sections':[
        {'title':'Cách dùng','items':['Dùng Could you…? để nhờ vả lịch sự trong công việc và đời thường.','Sau could dùng động từ nguyên mẫu, không thêm s hoặc to.']},
        {'title':'Công thức','columns':['Dạng câu','Cấu trúc'],'rows':[['Nhờ vả','Could you + V nguyên mẫu + …?'],['Đồng ý','Sure. / Of course.'],['Từ chối lịch sự','Sorry, I can’t right now.']]},
        {'title':'Ví dụ','examples':[{'en':phrases[0][0],'vi':phrases[0][1]},{'en':'Could you help me, please?','vi':'Bạn giúp tôi được không?'}]},
        {'title':'Lỗi thường gặp','contrast':{'wrong':'Could you to help me?','right':'Could you help me?'}}]}
    for verb,tail in [('help','me'),('check','this sentence'),('repeat','the question'),('open','the door'),('send','me the file'),('speak','more slowly'),('explain','this word'),('wait','a moment'),('close','the window'),('show','me an example'),('read','this sentence'),('call','me tomorrow')]:
        questions.append(dict(type='choice',category='grammar',group='Nhờ vả lịch sự',prompt=f'Chọn dạng đúng của {verb}: Could you ___ {tail}?',options=[verb,'to '+verb,verb+'ing',verb+'s'],answer=verb,explanation=f'Sau could dùng động từ nguyên mẫu: Could you {verb} {tail}?'))
    return dict(topic=topic,title=title,description=f'20 từ · 12 mẫu câu · {len(questions)} bài luyện từ vựng, nghe, giao tiếp và ngữ pháp',words=words,phrases=[dict(en=en,vi=vi,context=c) for en,vi,c in phrases],grammar=grammar,questions=questions)

if __name__=='__main__':
    server.init()
    with server.connect() as db:
        for row in db.execute('SELECT id,payload FROM lessons').fetchall():
            lesson=json.loads(row['payload'])
            if 'topic' not in lesson:
                lesson['topic']='Học tập & thói quen'
                db.execute('UPDATE lessons SET payload=? WHERE id=?',(json.dumps(lesson,ensure_ascii=False),row['id']))
        for lesson in [pack('Tiếng Anh IT','IT · Lập trình & làm việc cùng đội nhóm',IT,IT_PHRASES),pack('Giao tiếp đời thường','Daily English · Những cuộc trò chuyện mỗi ngày',DAILY,DAILY_PHRASES)]:
            if db.execute('SELECT 1 FROM lessons WHERE title=?',(lesson['title'],)).fetchone(): continue
            server.save_lesson(db,lesson)
            print(lesson['title'],len(lesson['questions']))
