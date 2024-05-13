from api import MyApp
import os

my_app = MyApp()  # Create an instance of MyApp

MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_ROOT_PASSWORD = os.environ["MYSQL_ROOT_PASSWORD"]
MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

print(MYSQL_DATABASE)
print(MYSQL_PASSWORD)
print(MYSQL_ROOT_PASSWORD)
print(MONGO_INITDB_ROOT_USERNAME)
print(MONGO_INITDB_ROOT_PASSWORD)

if __name__ == "__main__":
    # host the app on port 5000
    my_app.run(debug=True, port=5000, threaded=True, host='0.0.0.0')
