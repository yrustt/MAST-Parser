from sqlalchemy import Column, Integer, String, Text, Boolean

from mast_parser.models.base import Base


class FamousPerson(Base):
    __tablename__ = "famous_persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    english_url = Column(String(512), unique=True, nullable=False)
    english_name = Column(String(256), index=True, nullable=False)
    english_text = Column(Text(), nullable=False)
    russian_url = Column(String(512), index=True, nullable=True)
    russian_name = Column(String(256), index=True, nullable=True)
    russain_text = Column(Text(), nullable=True)
    sent = Column(Boolean(), index=True, default=False)

    def __repr__(self):
        return self.english_name
