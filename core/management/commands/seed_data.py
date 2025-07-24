from django.core.management.base import BaseCommand
from core.models import CompanyDrive, MockInterviewQuestion
from datetime import date # Import the date object

class Command(BaseCommand):
    help = 'Seeds the database with initial, realistic company drive data.'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed the database...')

        # Clear existing data to avoid duplicates
        CompanyDrive.objects.all().delete()
        MockInterviewQuestion.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared old data.'))

        # --- Real Company Data Aligned with Your Schema ---

        # 1. Microsoft
        CompanyDrive.objects.create(
            company_name="Microsoft",
            role="Software Engineer (SWE)",
            domain="Product-Based",
            salary_range="18-25 LPA",
            hiring_timeline="Primarily August-October for campus hiring.",
            drive_date=date(2025, 8, 20), # Primary date for ordering
            location="Bengaluru, Hyderabad, Noida",
            interview_process_description=(
                "Round 1: Online Coding Assessment (2-3 questions). "
                "Round 2: Technical Phone Screen (1 hour, DSA). "
                "Round 3-5: Virtual Interviews (3-4 rounds) covering DSA, System Design basics, and behavioral questions."
            )
        )

        # 2. Amazon
        CompanyDrive.objects.create(
            company_name="Amazon",
            role="Software Development Engineer (SDE-1)",
            domain="E-commerce & Cloud Computing",
            salary_range="20-30 LPA (including stocks)",
            hiring_timeline="Major drives in July-September and January-March.",
            drive_date=date(2025, 8, 25), # Primary date for ordering
            location="Hyderabad, Bengaluru, Chennai, Delhi",
            interview_process_description=(
                "Round 1: Online Assessment (Coding + Work-style simulation). "
                "Round 2: Technical Phone Interview. "
                "Round 3-5: Virtual 'Loop' interviews (3-5 rounds) covering Data Structures, Algorithms, and Amazon's Leadership Principles."
            )
        )

        # 3. Google
        CompanyDrive.objects.create(
            company_name="Google",
            role="Software Engineer",
            domain="Search & Cloud",
            salary_range="25-35 LPA (including stocks)",
            hiring_timeline="On-campus hiring in top-tier colleges (Sept-Dec).",
            drive_date=date(2025, 9, 5), # Primary date for ordering
            location="Bengaluru, Hyderabad, Pune",
            interview_process_description=(
                "Round 1: Recruiter phone screen or Online Coding Challenge. "
                "Round 2-3: Technical Phone Interviews (2 rounds, complex DSA). "
                "Round 4-6: On-site/Virtual 'Loop' (3-4 rounds) with deep dives into algorithms, system design, and 'Googliness' (behavioral)."
            )
        )

        # 4. Adobe
        CompanyDrive.objects.create(
            company_name="Adobe",
            role="Member of Technical Staff (MTS)",
            domain="Software & Creative Cloud",
            salary_range="19-24 LPA",
            hiring_timeline="On-campus hiring from August to November.",
            drive_date=date(2025, 9, 10), # Primary date for ordering
            location="Noida, Bengaluru",
            interview_process_description=(
                "Round 1: Online Aptitude & Coding Test. "
                "Round 2: Technical Interview 1 (DS & Algo). "
                "Round 3: Technical Interview 2 (Projects, Puzzles, Core CS). "
                "Round 4: Hiring Manager / HR Round."
            )
        )

        # 5. Tata Consultancy Services (TCS)
        CompanyDrive.objects.create(
            company_name="Tata Consultancy Services (TCS)",
            role="System Engineer (Ninja/Digital)",
            domain="IT Services & Consulting",
            salary_range="Ninja: 3.5-4.5 LPA; Digital: 7-8 LPA",
            hiring_timeline="Mainly through the National Qualifier Test (NQT) held quarterly.",
            drive_date=date(2025, 9, 15), # Primary date for ordering
            location="Pan-India (Chennai, Bengaluru, Kolkata)",
            interview_process_description=(
                "Step 1: TCS National Qualifier Test (NQT). "
                "Step 2: Technical Interview (Resume, Projects, basic programming). "
                "Step 3: HR Interview (Communication skills, personality)."
            )
        )
        
        # 6. Infosys
        CompanyDrive.objects.create(
            company_name="Infosys",
            role="Systems Engineer",
            domain="IT Services & Consulting",
            salary_range="5-6 LPA",
            hiring_timeline="Primarily through 'InfyTQ' platform and 'HackWithInfy'.",
            drive_date=date(2025, 9, 20), # Primary date for ordering
            location="Mysore, Pune, Bengaluru, Hyderabad",
            interview_process_description=(
                "Round 1: Online Test (Aptitude and Technical MCQs). "
                "Round 2: Technical Interview (Programming language, SQL, Projects). "
                "Round 3: HR Interview (Communication and situational questions)."
            )
        )

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully with updated schema.'))
