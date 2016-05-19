#coding: utf-8
import tornado.ioloop
import tornado.web
import io
import cv2
import picap
import argparse

parser = argparse.ArgumentParser(description='webカメラとかからストリーミングするスクリプト')
parser.add_argument('-c', '--camera_module',
        help='Raspi のカメラモジュールを使用する',
        action='store_true')
parser.add_argument('-r', '--resolution',
        help='解像度.横,高さ',
        nargs=2,
        type=int,
        metavar='X',
        default=[320,240])
args = parser.parse_args()

cap = picap.get_capturer(args.camera_module, resolution=args.resolution)

class rootpage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class SendImage(tornado.web.RequestHandler):
    def get(self, slug=None):
        print(slug)
        self.set_header('Content-Type', 'image/jpg')
        stream = io.BytesIO()
        ret, image = cap.read()
        ret, encoded = cv2.imencode('.jpg',image)
        stream.write(encoded)
        stream.seek(0)
        self.write(stream.read())

application = tornado.web.Application([
    (r'/', rootpage),
    (r'/img/([^/]*.jpg)', SendImage),
    ])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
