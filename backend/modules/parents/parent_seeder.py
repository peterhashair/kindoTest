import logging
import uuid
from config.database import SessionLocal
from . import parent_schema


def seed_data():
    db = SessionLocal()
    try:
        # Check if parents already exist
        if db.query(parent_schema.Parent).count() == 0:
            default_parents = [
                parent_schema.Parent(
                    id=uuid.UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef"),
                    name="John Smith",
                    email="john.smith@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("b2c3d4e5-f6a7-8901-2345-67890abcdef0"),
                    name="Jane Doe",
                    email="jane.doe@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("c3d4e5f6-a7b8-9012-3456-7890abcdef01"),
                    name="Peter Jones",
                    email="peter.jones@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("d4e5f6a7-b8c9-0123-4567-890abcdef012"),
                    name="Mary Williams",
                    email="mary.williams@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("e5f6a7b8-c9d0-1234-5678-90abcdef0123"),
                    name="David Brown",
                    email="david.brown@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("f6a7b8c9-d0e1-2345-6789-0abcdef01234"),
                    name="Susan Davis",
                    email="susan.davis@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("a7b8c9d0-e1f2-3456-7890-bcdef0123456"),
                    name="Michael Miller",
                    email="michael.miller@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("b8c9d0e1-f2a3-4567-8901-cdef01234567"),
                    name="Linda Wilson",
                    email="linda.wilson@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("c9d0e1f2-a3b4-5678-9012-def012345678"),
                    name="Robert Moore",
                    email="robert.moore@example.com",
                ),
                parent_schema.Parent(
                    id=uuid.UUID("d0e1f2a3-b4c5-6789-0123-ef0123456789"),
                    name="Patricia Taylor",
                    email="patricia.taylor@example.com",
                ),
            ]
            db.add_all(default_parents)
            db.commit()
            logging.info("Default parents have been added.")
        else:
            logging.info("Parents table is not empty. Skipping seed.")
    finally:
        db.close()
