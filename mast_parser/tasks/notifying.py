from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from mast_parser.export.csv import LastFamousPersonToCSVGenerator
from mast_parser.db import engine
from mast_parser.models import FamousPerson
from mast_parser.notify.email import LastFamousPersonEmailSender


def notify():
    Session = sessionmaker(bind=engine)

    with Session() as session:
        last_persons = (
            session.query(FamousPerson)
            .filter(FamousPerson.sent == False)  # noqa: E712
            .with_for_update()
            .all()
        )
        ids = [person.id for person in last_persons]

        csv = LastFamousPersonToCSVGenerator().execute(last_persons)
        LastFamousPersonEmailSender().send(csv)

        session.execute(
            update(FamousPerson).where(FamousPerson.id.in_(ids)).values(sent=True)
        )
        session.commit()
