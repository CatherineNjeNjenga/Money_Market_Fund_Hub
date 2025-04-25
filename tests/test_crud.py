import pytest
from datetime import date

from app import crud
from app.database import SessionLocal

# use a test date of 4/24/2025 to test the min_last_changed_date.
test_date = date(2025,4,24)

# fixture is used during the arrange phase, which prepares the testing setup
# This fixture uses session scope, which means it will run once for each function
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
    firms = crud.get_firms(db_session, skip=0, limit=100, min_last_changed_date=test_date)
    assert len(firms) == 34

def test_get_firms_by_name(db_session):
    firms = crud.get_firms(db_session, firm_name="Ndovu Money Market Fund")
    assert len(firms) == 1
    assert firms[0].firm_id == 26


def test_get_all_reports(db_session):
    reports = crud.get_reports(db_session, skip=0, limit=1000)
    assert len(reports) == 544

def test_get_new_reports(db_session):
    reports = crud.get_reports(db_session, skip=0, limit=1000,
                                        min_last_changed_date=test_date)

def test_get_firm_count(db_session):
    firm_count = crud.get_firm_count(db_session)
    assert firm_count == 34