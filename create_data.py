from Capp import create_app, db

app = create_app()

with app.app_context():
    db.drop_all()     # <- Sletter alle tabeller (valgfritt)
    db.create_all()   # <- Lager alle tabeller på nytt
    print("Database created!")
