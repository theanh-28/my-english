"""Assistant-side lesson maintenance. Never exposed in the learner web interface."""
import argparse, json
import server

def main():
    parser=argparse.ArgumentParser(description='Ghi bài học trực tiếp vào SQLite')
    parser.add_argument('command',choices=['add','list'])
    parser.add_argument('file',nargs='?')
    args=parser.parse_args()
    server.init()
    if args.command=='add':
        if not args.file: parser.error('add cần đường dẫn bài học')
        with open(args.file,encoding='utf-8-sig') as f: lesson=json.load(f)
        with server.connect() as db: key=server.save_lesson(db,lesson)
        print('Đã lưu bài học: '+lesson['title']+' ('+key+')')
    else:
        with server.connect() as db:
            for row in db.execute('SELECT id,title,created FROM lessons ORDER BY rowid DESC'):
                print(f"{row['created']} | {row['id']} | {row['title']}")

if __name__=='__main__': main()
