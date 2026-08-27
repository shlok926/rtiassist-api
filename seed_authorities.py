"""
DEVELOPMENT / PILOT DATA SEEDING ONLY
Do NOT run this in production without caution. It does not run DB migrations.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import engine, get_db
from models.schemas import AuthorityImportRequest, AuthorityImportRecord
from services.authority_service import admin_import_authorities
from models.orm.user import User

def seed_pilot_data():
    db = next(get_db())
    
    # Require an existing admin email via environment variable
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin = db.query(User).filter(User.email == admin_email).first()
    
    if not admin or admin.role != "admin":
        print(f"❌ Error: Admin user '{admin_email}' not found or is not an admin.")
        print("Please create an admin user first or specify a valid ADMIN_EMAIL.")
        sys.exit(1)
        
    print(f"✅ Found Admin User: {admin_email}")

    # 2. Prepare high-quality, verified pilot data
    # All marked UNVERIFIED initially. We will independently verify them through the UI or verification report.
    records = [
        AuthorityImportRecord(
            department="Prime Minister's Office",
            government_level="CENTRAL",
            source_url="https://www.pmindia.gov.in/en/right-to-information-rti/",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Under Secretary (RTI)",
            appellate_authority_designation="Director (RTI)",
            address="South Block, New Delhi - 110011",
            online_portal="https://rtionline.gov.in",
            filing_fee="₹10",
            payment_methods="Online via rtionline.gov.in, Postal Order, Demand Draft",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
        AuthorityImportRecord(
            department="Ministry of Railways",
            ministry="Ministry of Railways",
            government_level="CENTRAL",
            source_url="https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,1,304,366,546,842",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Public Information Officer, Railway Board",
            appellate_authority_designation="First Appellate Authority, Railway Board",
            address="Rail Bhavan, Raisina Road, New Delhi - 110001",
            online_portal="https://rtionline.gov.in",
            filing_fee="₹10",
            payment_methods="Online via rtionline.gov.in, Postal Order",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
        AuthorityImportRecord(
            department="Delhi Police",
            government_level="STATE",
            state="Delhi",
            source_url="https://delhipolice.gov.in/rti",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Public Information Officer (HQ)",
            appellate_authority_designation="Joint Commissioner of Police",
            address="Delhi Police Headquarters, Jai Singh Road, New Delhi - 110001",
            online_portal="https://rtionline.gov.in",
            filing_fee="₹10",
            payment_methods="Online via rtionline.gov.in, Indian Postal Order",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
        AuthorityImportRecord(
            department="Brihanmumbai Municipal Corporation",
            government_level="STATE",
            state="Maharashtra",
            district="Mumbai",
            source_url="https://portal.mcgm.gov.in/irj/portal/anonymous/qlrtiact",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Public Information Officer",
            appellate_authority_designation="First Appellate Authority",
            address="BMC Headquarters, Mahapalika Marg, Mumbai - 400001",
            online_portal="https://rtionline.maharashtra.gov.in/",
            filing_fee="₹10",
            payment_methods="Court Fee Stamp, Postal Order, Online",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
        AuthorityImportRecord(
            department="Reserve Bank of India",
            government_level="CENTRAL",
            source_url="https://www.rbi.org.in/Scripts/Righttoinfoact.aspx",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Central Public Information Officer",
            appellate_authority_designation="First Appellate Authority, RIA Division",
            address="Reserve Bank of India, Central Office, Shahid Bhagat Singh Road, Mumbai - 400001",
            online_portal="https://rtionline.gov.in",
            filing_fee="₹10",
            payment_methods="Online via rtionline.gov.in, Demand Draft, Postal Order",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
        AuthorityImportRecord(
            department="Election Commission of India",
            government_level="CENTRAL",
            source_url="https://rti.eci.gov.in/",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Public Information Officer",
            appellate_authority_designation="First Appellate Authority",
            address="Election Commission of India, Nirvachan Sadan, Ashoka Road, New Delhi - 110001",
            online_portal="https://rti.eci.gov.in/",
            filing_fee="₹10",
            payment_methods="Online via rti.eci.gov.in, Postal Order",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
        AuthorityImportRecord(
            department="Unique Identification Authority of India (UIDAI)",
            government_level="CENTRAL",
            source_url="https://uidai.gov.in/",
            source_type="OFFICIAL_WEBSITE",
            pio_designation="Central Public Information Officer (CPIO)",
            appellate_authority_designation="First Appellate Authority",
            address="UIDAI Headquarters, Bangla Sahib Road, Behind Kali Mandir, Gole Market, New Delhi - 110001",
            online_portal="https://rtionline.gov.in",
            filing_fee="₹10",
            payment_methods="Online via rtionline.gov.in, Postal Order",
            verification_status="UNVERIFIED",
            verification_notes=None
        ),
    ]
    
    import_req = AuthorityImportRequest(records=records)
    
    print("\n📦 Importing Pilot Authority Dataset...")
    try:
        response = admin_import_authorities(db, import_req, admin)
        print(f"Import Complete!")
        print(f"Total Processed: {response.total_processed}")
        print(f"Successfully Imported: {response.imported}")
        print(f"Rejected: {response.rejected}")
        print(f"Possible Duplicates: {response.possible_duplicates}")
        
        for res in response.results:
            print(f" - Record {res.index}: {res.status} (Authority ID: {res.authority_id})")
            
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_pilot_data()
