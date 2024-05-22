import time
import MySQLdb
from MySQLdb import OperationalError
import os

def wait_for_mysql(host, port, user, password, dbname, retries=30, interval=5):
    for _ in range(retries):
        try:
            conn = MySQLdb.connect(
                host=host, port=port, user=user, passwd=password, db=dbname
            )
            conn.close()
            print("MySQL is accepting connections")
            return
        except OperationalError:
            print("MySQL is not yet accepting connections")
            time.sleep(interval)
    
    print("Exceeded maximum retries. MySQL is not accepting connections.")

if __name__ == "__main__":
    wait_for_mysql(
        host=os.environ.get("MYSQL_HOST"),
        port=int(os.environ.get("MYSQL_PORT")),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        dbname=os.environ.get("MYSQL_DATABASE"),
    )
