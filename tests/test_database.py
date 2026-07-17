"""
Tests that the database functions work as expected.
Users should hopefully not need to modify these tests.
"""

from sqlalchemy.ext.automap import automap_base


def test_orm_use(db):
    # Tests validation using the SQLAlchemy ORM

    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Sources = Base.classes.Sources

    # Adding and removing a basic source
    s = Sources(source="YB0", yb_number=0, reference="WolfChase25")
    with db.session as session:
        session.add(s)
        session.commit()

    assert db.query(db.Sources).filter(db.Sources.c.source == "YB0").count() == 1

    # Remove added source so other tests don't include it
    with db.session as session:
        session.delete(s)
        session.commit()

    assert db.query(db.Sources).filter(db.Sources.c.source == "YB0").count() == 0


def test_adding_data(db):

    # Confirm the source isn't already present
    assert (
        db.query(db.Sources).filter(db.Sources.c.source == "Fake YB0").count() == 0
    )

    Base = automap_base(metadata=db.metadata)
    Base.prepare()

    # Creating the actual Table objects
    Sources = Base.classes.Sources
    Publications = Base.classes.Publications

    # Insert supporting data to (Publications, Sources)
    ref = Publications(reference="FakeRef99")
    s = Sources(source="Fake YB0", yb_number=0, reference="FakeRef99")

    with db.session as session:
        session.add_all([ref, s])
        session.commit()

    # Verify supporting information was stored
    assert (
        db.query(db.Sources).filter(db.Sources.c.source == "Fake YB0").count() == 1
    )
    assert (
        db.query(db.Publications)
        .filter(db.Publications.c.reference == "FakeRef99")
        .count()
        == 1
    )

    # Clean up — remove in reverse FK order so constraints aren't violated
    with db.session as session:
        session.delete(s)
        session.delete(ref)
        session.commit()
