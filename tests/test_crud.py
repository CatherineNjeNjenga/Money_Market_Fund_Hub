import pytest
from datetime import date

from app import crud
from database import SessionLocal

# use a test date of 4/1/2024 to test the min_last_changed_date.
test_date = date(2024,4,1)

@pytest.fixture(scope="function")
def db_session():
    """This starts a database session and closes it when done"""
    session = SessionLocal()
    yield session
    session.close()

def test_get_firm(db_session):
    firm = crud.get_firm(db_session, firm_id = 1)
    assert firm.firm_id == 1

def test_get_firms(db_session):
    firms = crud.get_firms(db_session, skip=0, limit=10000, min_last_changed_date=test_date)
    assert len(firms) == 34

def test_get_firms_by_name(db_session):
    firms = crud.get_firms(db_session, firm_name="Bryce")
    assert len(firms) == 1
    assert firms[0].firm_id == 2009


def test_get_all_reports(db_session):
    reports = crud.get_reports(db_session, skip=0, limit=18000)
    assert len(reports) == 17306

def test_get_new_reports(db_session):
    reports = crud.get_reports(db_session, skip=0, limit=18000,
                                        min_last_changed_date=test_date)

def test_get_firm_count(db_session):
    firm_count = crud.get_firm_count(db_session)
    assert firm_count == 1018