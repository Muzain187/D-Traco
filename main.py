# main.py
from app.main import app
from app.models.database import Base, engine
import uvicorn


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
