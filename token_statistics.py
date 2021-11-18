from time import gmtime, strftime
import sqlite3
import tornado.ioloop
import tornado.web
from tornado.log import gen_log as logger
import logging
logger.setLevel(logging.DEBUG)


class TokenStatisticsHandler(tornado.web.RequestHandler):
    db = sqlite3.connect('token_statistics.sqlite')
    cursor = db.cursor()

    def get(self):
        try:
            token = self.get_argument('token', None)
            cart_id = self.get_argument('cart_id', None)
            if token and cart_id:
                self._insert_data(token, cart_id)
                self.set_status(200)
                logger.info("Token Stats: Add token and cart id")
            else:
                self.set_status(400, "No token or cart_id")
                logger.info("Token Stats: Error(No token and cart id)")
            self.finish()
        except:
            self.set_status(500)
            self.finish()

    def _insert_data(self, token, cart_id):
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.cursor.execute(f"""REPLACE INTO token_statistics
                            (token, cart_id, date) 
                            VALUES('{token}', '{cart_id}', '{date}');
                            """)
        self.db.commit()


def make_app():
    return tornado.web.Application([
        (r"/", TokenStatisticsHandler),
    ])

def _init_db():
    db = sqlite3.connect('token_statistics.sqlite')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS token_statistics
                      (token TEXT,
                      cart_id int,
                      date TEXT,

                      UNIQUE(token, cart_id)
                      )
                      """)
    db.commit()


if __name__ == "__main__":
    _init_db()
    app = make_app()
    app.listen(2121)
    tornado.ioloop.IOLoop.current().start()
