from app import app, views, init_db


init_db()

if __name__ == "__main__":
    app.run(debug=True)



