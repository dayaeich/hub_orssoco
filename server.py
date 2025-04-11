from flask import Flask
from main import main  

app = Flask(__name__)

@app.route('/', methods=['GET'])
def run_job():
    main()
    return 'Main executado com sucesso!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
