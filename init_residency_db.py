#!/usr/bin/env python
"""
Migration script to initialize residency platform database
Run this after updating models.py
"""

from app import app, db

def init_database():
    """Initialize the database with new models"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Initialize with sample data
        from models import ResidencyConsultant
        
        # Add sample consultants if none exist
        if ResidencyConsultant.query.count() == 0:
            consultants = [
                ResidencyConsultant(
                    name="John Smith",
                    email="john@nexoraconsultants.com",
                    phone="+1-555-0100",
                    specializations="Portugal, Malta, Greece, Spain",
                    experience_years=15,
                    bio="Immigration expert with 15 years of experience helping clients obtain residency worldwide. Specialist in European golden visas.",
                    hourly_rate=150.0,
                    verified=True,
                    rating=4.9,
                    total_reviews=47
                ),
                ResidencyConsultant(
                    name="Maria Garcia",
                    email="maria@nexoraconsultants.com",
                    phone="+34-555-0101",
                    specializations="Spain, Portugal, Italy, France",
                    experience_years=12,
                    bio="European residency specialist with focus on Southern European programs. 12 years of experience.",
                    hourly_rate=140.0,
                    verified=True,
                    rating=4.8,
                    total_reviews=39
                ),
                ResidencyConsultant(
                    name="Chen Wei",
                    email="chen@nexoraconsultants.com",
                    phone="+65-555-0102",
                    specializations="Singapore, Thailand, Malaysia, Australia",
                    experience_years=10,
                    bio="Asia-Pacific residency expert specializing in Asian golden visas and investment programs.",
                    hourly_rate=130.0,
                    verified=True,
                    rating=4.7,
                    total_reviews=34
                ),
                ResidencyConsultant(
                    name="James Miller",
                    email="james@nexoraconsultants.com",
                    phone="+1-555-0103",
                    specializations="Canada, USA, Australia, New Zealand",
                    experience_years=18,
                    bio="North American and Oceania specialist. Over 18 years helping clients with skilled migration and investment visas.",
                    hourly_rate=160.0,
                    verified=True,
                    rating=4.9,
                    total_reviews=52
                ),
                ResidencyConsultant(
                    name="Aisha Patel",
                    email="aisha@nexoraconsultants.com",
                    phone="+971-555-0104",
                    specializations="UAE, Qatar, Saudi Arabia, Middle East",
                    experience_years=14,
                    bio="Middle East visa expert. Specializes in GCC countries and golden visa programs in the region.",
                    hourly_rate=145.0,
                    verified=True,
                    rating=4.8,
                    total_reviews=41
                )
            ]
            
            for consultant in consultants:
                db.session.add(consultant)
            db.session.commit()
            print(f"✓ {len(consultants)} sample consultants created")
        
        print("\n✓ Database initialization complete!")
        print("✓ Nexora platform is ready to use!")
        print("\nAvailable consultants:")
        for consultant in ResidencyConsultant.query.all():
            print(f"  • {consultant.name} - ${consultant.hourly_rate}/hour")

if __name__ == '__main__':
    init_database()

