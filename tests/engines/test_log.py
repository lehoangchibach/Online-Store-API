from sqlalchemy import func, select

from main import db
from main.models.log import LogModel


def test_log():
    def count_logs() -> int:
        statement = select(func.count()).select_from(LogModel)
        return db.session.execute(statement).scalars().one()

    assert count_logs() == 0

    db.session.add(LogModel(data={}))
    db.session.commit()

    assert count_logs() == 1
