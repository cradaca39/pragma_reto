from transactions import transactions
from flask import Flask
from merge_files import merge_csv_files


if __name__ == "__main__":
    
    try:
        merge_csv_files()
        app = Flask(__name__)
        app.register_blueprint(transactions)
        app.run(host="0.0.0.0", debug=True)
    except Exception as e:
        print('Error with the execution of the process',e)