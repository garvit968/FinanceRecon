from sqlalchemy import Column, Integer, String, Float
from app.config.dbConfig import Base

class UploadedData(Base):
    __tablename__ = "uploaded_data"

    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(String, index=True)
    source = Column(String)
    product_name = Column(String)
    transaction_id = Column(Integer)
    amount = Column(Integer)
    