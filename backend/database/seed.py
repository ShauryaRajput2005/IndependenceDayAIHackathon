"""
database/seed.py — Optional seed script for development.
Run manually: python -m database.seed
"""
from database.database import SessionLocal, init_db
from database.models import Product
import json


def seed():
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(Product).first()
        if existing:
            print("Database already seeded.")
            return

        sample = Product(
            name="AI Resume Builder",
            category="Education",
            description="AI tool that creates ATS-friendly resumes",
            features=json.dumps(["ATS optimization", "AI suggestions", "Resume templates"]),
            problem_solved="Students struggle to create effective resumes",
            target_audience="Indian college students",
            price="Free",
            platform="instagram",
            tone="sarcastic",
            requirements="Make it Hinglish, funny and meme-heavy",
        )
        db.add(sample)
        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
