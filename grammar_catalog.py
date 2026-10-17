"""Shared curriculum, authored summaries and original examples, not learner data."""
PRESENT = {
 'title':'Present simple · Hiện tại đơn',
 'body':'Học theo thứ tự: cách dùng → động từ thường → be → câu hỏi → luyện tập.',
 'level':'A1–A2 · Có phần mở rộng',
 'sections':[
  {'title':'Bản đồ bài học','items':['S = chủ ngữ; V = động từ nguyên mẫu.','Chọn nhánh: động từ thường (work, study) hoặc be (am/is/are). Không trộn hai công thức.']},
  {'title':'Cách dùng','items':['Thói quen: I review words after lunch. — Tôi ôn từ sau bữa trưa.','Trạng thái hiện tại: She works in IT. — Cô ấy làm trong ngành IT.','Sự thật: Ice melts in heat. — Băng tan khi gặp nhiệt.','Lịch cố định: The meeting starts at ten. — Cuộc họp bắt đầu lúc mười giờ.']},
  {'title':'Động từ thường','columns':['Dạng','I / You / We / They','He / She / It'], 'rows':[
   ['Khẳng định','S + V','S + V-s/es'],['Phủ định','S + do not + V','S + does not + V'],['Câu hỏi','Do + S + V?','Does + S + V?'],['Trả lời ngắn','Yes, S + do. / No, S + don’t.','Yes, S + does. / No, S + doesn’t.']],
   'hint':'S trong câu trả lời là đại từ: Does Mai code? → Yes, she does. Don’t = do not; doesn’t = does not.'},
  {'title':'Động từ be','columns':['Chủ ngữ','Khẳng định','Phủ định','Câu hỏi'], 'rows':[
   ['I','I am ready.','I am not ready.','Am I ready?'],['He / She / It','She is ready.','She is not ready.','Is she ready?'],['You / We / They','They are ready.','They are not ready.','Are they ready?']],
   'hint':'Không dùng do/does với be trong các câu này. Is she ready? → Yes, she is. / No, she isn’t.'},
  {'title':'Thêm s / es','columns':['Quy tắc','Ví dụ'], 'rows':[
   ['Thông thường thêm s','read → reads; play → plays'],['Kết thúc -s, -ss, -sh, -ch, -x, -z: thường thêm es','pass → passes; wash → washes; fix → fixes'],['Phụ âm + y → ies','study → studies'],['Nguyên âm + y: thêm s','enjoy → enjoys'],['Một số dạng cần nhớ','have → has; do → does; go → goes']],
   'hint':'Chỉ áp dụng đuôi này ở khẳng định ngôi thứ ba số ít. Sau does/doesn’t: dùng nguyên mẫu.'},
  {'title':'Câu hỏi với từ hỏi','examples':[
   {'en':'Where does your team work?','vi':'Đội của bạn làm việc ở đâu? Từ hỏi + does + chủ ngữ + V.'},
   {'en':'Who maintains this server?','vi':'Ai bảo trì máy chủ này? Who là chủ ngữ nên không thêm does.'}]},
  {'title':'Tần suất và ngữ cảnh','items':['Usually/often/never thường đứng trước động từ thường: I often code.','Với be, thường đứng sau: She is often busy.','Every day / twice a week thường ở cuối câu. Không dùng từ khóa làm quy tắc tuyệt đối.','I code every day: thói quen. I am coding now: hoạt động đang diễn ra.'],
   'hint':'Know, like, want thường diễn tả trạng thái và dùng hiện tại đơn; một số động từ có nghĩa khác khi dùng dạng tiếp diễn.'},
  {'title':'Ví dụ Anh–Việt','examples':[
   {'en':'The application stores your settings.','vi':'Ứng dụng lưu các thiết lập của bạn.'},
   {'en':'We don’t deploy on Sundays.','vi':'Chúng tôi không triển khai vào Chủ nhật.'},
   {'en':'Does this function return a string?','vi':'Hàm này có trả về chuỗi không?'},
   {'en':'The database is available.','vi':'Cơ sở dữ liệu đang sẵn sàng để truy cập.'}]},
  {'title':'Lỗi cần tránh','contrast':{'wrong':'She doesn’t studies English.','right':'She doesn’t study English.'},'hint':'Không viết She is study… để diễn tả thói quen. Dùng She studies…; nếu đang diễn ra: She is studying…'},
  {'title':'Mở rộng: chưa cần học thuộc ngay','items':['Mệnh đề thời gian nói về tương lai thường dùng hiện tại đơn: I’ll call when I finish.','Hiện tại đơn cũng xuất hiện trong tóm tắt truyện, bình luận trực tiếp và hướng dẫn. Học riêng theo ngữ cảnh.']}
 ],
 'sources':[
  {'title':'British Council · Present simple','url':'https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/present-simple'},
  {'title':'British Council · A1–A2','url':'https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2/present-simple'},
  {'title':'EF · Simple present','url':'https://www.ef.com/wwen/english-resources/english-grammar/simple-present-tense/'}]
}

REQUESTS = {
 'title':'Could you…? · Nhờ vả lịch sự', 'level':'A1–A2 · Giao tiếp',
 'body':'Nhờ người khác làm việc gì: Could you + động từ nguyên mẫu…?',
 'sections':[
  {'title':'Mục đích','items':['Dùng để nhờ người khác hành động. Could thường lịch sự, gián tiếp hơn can; giọng điệu và hoàn cảnh cũng quan trọng.','Could trong lời nhờ hiện tại không mang nghĩa quá khứ. Bài này chỉ học cách nhờ vả, chưa bao quát mọi nghĩa của could.']},
  {'title':'Công thức','columns':['Mục đích','Cấu trúc / ví dụ'],'rows':[
   ['Nhờ ai làm gì','Could you + V + …?'],['Thêm please','Could you please check this?'],['Đồng ý','Sure. / Of course.'],['Từ chối','Sorry, I can’t right now.']]},
  {'title':'Ví dụ thực tế','examples':[
   {'en':'Could you check this branch?','vi':'Bạn kiểm tra nhánh này giúp tôi được không?'},
   {'en':'Could you speak a little more slowly?','vi':'Bạn nói chậm hơn một chút được không?'},
   {'en':'Could you show me the menu, please?','vi':'Bạn cho tôi xem thực đơn được không?'}]},
  {'title':'Phân biệt dễ nhầm','columns':['Câu','Mục đích'],'rows':[
   ['Could you open the window?','Nhờ người khác mở cửa sổ.'],['Could I open the window?','Xin phép tự mình mở cửa sổ.']],
   'hint':'Đáp lời nhờ bằng Sure hoặc Sorry, I can’t… tự nhiên hơn việc chỉ nói Yes, I could.'},
  {'title':'Lỗi thường gặp','items':['Không dùng to sau could; không chia động từ theo you.','Không thêm do/does trước could.'], 'contrast':{'wrong':'Do you could to help me?','right':'Could you help me?'}}
 ],
 'sources':[{'title':'British Council · Requests, offers and invitations','url':'https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/requests-offers-invitations'}]
}

def apply(lesson):
    import copy
    title=lesson.get('grammar',{}).get('title','')
    if title.startswith('Present simple'): lesson['grammar']=copy.deepcopy(PRESENT)
    elif title.startswith('Could you'): lesson['grammar']=copy.deepcopy(REQUESTS)
    return lesson

if __name__=='__main__':
    import json, server
    path=server.ROOT/'sample.json'
    path.write_text(json.dumps(apply(json.loads(path.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with server.connect() as db:
        for row in db.execute('SELECT id,payload FROM lessons').fetchall():
            db.execute('UPDATE lessons SET payload=? WHERE id=?',(json.dumps(apply(json.loads(row['payload'])),ensure_ascii=False),row['id']))
