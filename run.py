from app import app

port = app.config['PORT']
if __name__ == '__main__':
    app.run(port=port)