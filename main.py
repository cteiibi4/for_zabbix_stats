from time import gmtime, strftime
import sqlite3
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    db = sqlite3.connect('token_statistics.sqlite')
    cursor = db.cursor()

    def initialize(self):
        self._init_db()

    def get(self):
        try:
            token = self.get_argument('token')
            cart_id = self.get_argument('cart_id')
            if token and cart_id:
                self._insert_data(token, cart_id)
                self.set_status(200)
            else:
                self.set_status(400, "No token or cart_id")
            self.finish()
        except:
            self.set_status(500)
            self.finish()

    def _init_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS token_statistics
                          (token TEXT,
                          cart_id int PRIMARY_KEY,
                          date TEXT)
                          """)
        self.db.commit()

    def _insert_data(self, token, cart_id):
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.cursor.execute(f"""INSERT INTO token_statistics
                            (token, cart_id, date) 
                            VALUES('{token}', '{cart_id}', '{date}');
                            """)
        self.db.commit()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(2121)
    tornado.ioloop.IOLoop.current().start()
