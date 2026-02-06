import logging
from config.database import SessionLocal
from . import school_schema


def seed_data():
    db = SessionLocal()
    try:
        # Check if schools already exist
        if db.query(school_schema.School).count() == 0:
            default_schools = [
                school_schema.School(
                    name="Greenwood High", id="b96af40e-6976-423f-809d-116bf0b5abbb"
                ),
                school_schema.School(
                    name="Oakridge International",
                    id="e4eb662e-82fa-4689-9062-0bb84d97a90d",
                ),
            ]
            db.add_all(default_schools)
            db.commit()
            logging.info("Default schools have been added.")
        else:
            logging.info("Schools table is not empty. Skipping seed.")

    finally:
        db.close()
