from website import db, create_app,create_data
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
create_data()
quit()