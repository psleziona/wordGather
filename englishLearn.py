from app import app, db
from app.models import *

db.create_all()
app.run(debug=True)