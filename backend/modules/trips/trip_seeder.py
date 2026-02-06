import logging
from config.database import SessionLocal
from . import trip_schema


def seed_data():
    db = SessionLocal()
    try:
        # Check if trips already exist
        if db.query(trip_schema.Trip).count() == 0:
            default_trips = [
                trip_schema.Trip(
                    id="b96af40e-6976-423f-809d-116bf0b5abbb",
                    name="Greenwood High Field Trip",
                    description="A fun and educational trip for Greenwood High students.",
                    destination="Greenwood Park",
                    school_id="b96af40e-6976-423f-809d-116bf0b5abbb",
                    price_in_cents=2500,
                    start_date="2026-03-01T09:00:00+00:00",
                    end_date="2026-03-01T17:00:00+00:00",
                    published=True
                ),
                trip_schema.Trip(
                    id="e4eb662e-82fa-4689-9062-0bb84d97a90d",
                    name="Oakridge International Science Tour",
                    description="Science museum tour for Oakridge International.",
                    destination="City Science Museum",
                    school_id="e4eb662e-82fa-4689-9062-0bb84d97a90d",
                    price_in_cents=3000,
                    start_date="2026-04-15T08:00:00+00:00",
                    end_date="2026-04-15T18:00:00+00:00",
                    published=True
                ),
            ]
            db.add_all(default_trips)
            db.commit()
            logging.info("Default trips have been added.")
        else:
            logging.info("Trips table is not empty. Skipping seed.")
    finally:
        db.close()
