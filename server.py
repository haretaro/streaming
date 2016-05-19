import tornado.ioloop
import tornado.web
import io
import cv2
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 380)

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
