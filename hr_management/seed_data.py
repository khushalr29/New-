import os
import django
import random
from datetime import date, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_management.settings')
django.setup()

from shared.models.core import Company, User
from shared.models.hr_management import (
    Branch, Department, Designation, DocumentType, AwardType, 
    IndicatorCategory, Indicator, GoalType, ReviewCycle, 
    Resignations, Termination, Announcement, Trip, Warning,
    Promotion, Transfer, EmployeeGoal, EmployeeReview, Complaint,
    TrainingType, TrainingProgram, TrainingSession, AssignTraining
)
from shared.models.core.employee import Employee, EmployeeDocument
from shared.models.hr_management.asset_manage import Assets, AssetType
from shared.models.hr_management.award import Award

def seed_data():
    company = Company.objects.get(id=7)
    user = User.objects.get(id=2)

    # Update company limits for seeding
    company.no_of_employees = 100
    company.no_of_users = 100
    company.save()

    # Cleanup existing data to avoid unique constraint violations
    print("Cleaning up existing data...")
    AssignTraining.objects.filter(company=company).delete()
    TrainingSession.objects.filter(company=company).delete()
    TrainingProgram.objects.filter(company=company).delete()
    TrainingType.objects.filter(company=company).delete()
    Assets.objects.filter(company=company).delete()
    AssetType.objects.filter(company=company).delete()
    Announcement.objects.filter(company=company).delete()
    Complaint.objects.filter(company=company).delete()
    Warning.objects.filter(company=company).delete()
    Trip.objects.filter(company=company).delete()
    Transfer.objects.filter(company=company).delete()
    Termination.objects.filter(company=company).delete()
    Resignations.objects.filter(company=company).delete()
    Promotion.objects.filter(company=company).delete()
    EmployeeReview.objects.filter(company=company).delete()
    ReviewCycle.objects.filter(company=company).delete()
    EmployeeGoal.objects.filter(company=company).delete()
    GoalType.objects.filter(company=company).delete()
    Indicator.objects.filter(company=company).delete()
    IndicatorCategory.objects.filter(company=company).delete()
    Award.objects.filter(company=company).delete()
    AwardType.objects.filter(company=company).delete()
    Employee.objects.filter(company=company).delete()
    Designation.objects.filter(company=company).delete()
    Department.objects.filter(company=company).delete()
    Branch.objects.filter(company=company).delete()

    print("Seeding Branches...")
    branches = []
    for i in range(1, 6):
        branch = Branch.objects.create(
            company=company,
            branch_name=f"Branch {i}",
            branch_code=f"BR-{random.randint(1000, 9999)}",
            city="New York" if i % 2 == 0 else "London",
            state="NY" if i % 2 == 0 else "UK",
            zip_code=f"1000{i}",
            phone_number=f"12345678{i}",
            email=f"branch{i}@example.com",
            status="active"
        )
        branches.append(branch)

    print("Seeding Departments...")
    departments = []
    for i in range(1, 6):
        dept = Department.objects.create(
            company=company,
            department=f"Department {i}",
            branch=random.choice(branches),
            unique_code=f"DEPT-{random.randint(1000, 9999)}",
            status="active"
        )
        departments.append(dept)

    print("Seeding Designations...")
    designations = []
    designation_names = ["Software Engineer", "HR Manager", "Product Owner", "QA Analyst", "Data Scientist"]
    for i in range(5):
        desig = Designation.objects.create(
            company=company,
            name=designation_names[i],
            department=random.choice(departments),
            status="active"
        )
        designations.append(desig)

    print("Seeding Employees and Users...")
    employees = []
    first_names = ["James", "Mary", "Robert", "Patricia", "John"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    for i in range(5):
        # Create a user for each employee
        user_emp = User.objects.create_user(
            email=f"user{i}_{random.randint(100, 999)}@example.com",
            password="password123",
            full_name=f"{first_names[i]} {last_names[i]}",
            phone_number=f"987654321{i}",
            gender="male" if i % 2 == 0 else "female"
        )
        user_emp.company = company
        user_emp.save()

        emp = Employee.objects.create(
            company=company,
            user_id=user_emp,
            full_name=f"{first_names[i]} {last_names[i]}",
            employee_id=f"EMP{random.randint(10000, 99999)}_{i}",
            employee_code=f"CODE{random.randint(10000, 99999)}_{i}",
            official_email_id=f"official{i}_{random.randint(100, 999)}@company.com",
            personal_email_id=f"personal{i}_{random.randint(100, 999)}@gmail.com",
            gender="male" if i % 2 == 0 else "female",
            date_of_birth=date(1990, 1, 1),
            branch=random.choice(branches),
            department=random.choice(departments),
            designation=random.choice(designations),
            phone_number=f"987654321{i}",
            status="active",
            password="password123"
        )
        employees.append(emp)

    print("Seeding Award Types...")
    award_types = []
    for i in range(1, 6):
        at = AwardType.objects.create(
            company=company,
            award_type=f"Award Type {i}",
            status="active"
        )
        award_types.append(at)

    print("Seeding Awards...")
    for i in range(5):
        Award.objects.create(
            company=company,
            employee=random.choice(employees),
            award_type=random.choice(award_types),
            date_awarded=date.today(),
            gift=f"Bonus {i*100}",
            description=f"Excellence in work for month {i+1}"
        )

    print("Seeding Indicator Categories...")
    indicator_categories = []
    for i in range(1, 6):
        ic = IndicatorCategory.objects.create(
            company=company,
            category_name=f"Category {i}",
            status="active"
        )
        indicator_categories.append(ic)

    print("Seeding Indicators...")
    indicators = []
    for i in range(5):
        ind = Indicator.objects.create(
            company=company,
            indicator_name=f"Indicator {i}",
            category=random.choice(indicator_categories),
            target_value=100.00,
            status="active"
        )
        indicators.append(ind)

    print("Seeding Goal Types...")
    goal_types = []
    for i in range(1, 6):
        gt = GoalType.objects.create(
            company=company,
            goal_name=f"Goal {i}",
            status="active"
        )
        goal_types.append(gt)

    print("Seeding Employee Goals...")
    for i in range(5):
        EmployeeGoal.objects.create(
            company=company,
            employee=random.choice(employees),
            goal_type=random.choice(goal_types),
            goal_title=f"Quarterly Goal {i}",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
            status="IN_PROGRESS"
        )

    print("Seeding Review Cycles...")
    review_cycles = []
    for i in range(1, 6):
        rc = ReviewCycle.objects.create(
            company=company,
            cycle_name=f"Cycle {i}",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status="active"
        )
        review_cycles.append(rc)

    print("Seeding Employee Reviews...")
    for i in range(5):
        EmployeeReview.objects.create(
            company=company,
            employee=random.choice(employees),
            reviewer=random.choice(employees),
            review_cycle=random.choice(review_cycles),
            review_date=date.today(),
            rating=4.5,
            status="COMPLETED"
        )

    print("Seeding Promotions...")
    for i in range(5):
        Promotion.objects.create(
            company=company,
            employee=random.choice(employees),
            promotion_title=f"Promotion {i}",
            promotion_date=date.today(),
            old_designation=random.choice(designations),
            new_designation=random.choice(designations),
            status="approved"
        )

    print("Seeding Resignations...")
    for i in range(5):
        Resignations.objects.create(
            company=company,
            employee=random.choice(employees),
            resignation_date=date.today(),
            last_working_day=date.today() + timedelta(days=30),
            resignation_reason=f"Personal reasons {i}",
            status="active"
        )

    print("Seeding Terminations...")
    for i in range(5):
        Termination.objects.create(
            company=company,
            employee=random.choice(employees),
            termination_date=date.today(),
            last_working_day=date.today(),
            termination_reason=f"Policy violation {i}",
            status="active"
        )

    print("Seeding Transfers...")
    for i in range(5):
        Transfer.objects.create(
            company=company,
            employee=random.choice(employees),
            transfer_title=f"Transfer {i}",
            transfer_date=date.today(),
            old_department=random.choice(departments),
            new_department=random.choice(departments),
            old_branch=random.choice(branches),
            new_branch=random.choice(branches)
        )

    print("Seeding Trips...")
    for i in range(5):
        Trip.objects.create(
            company=company,
            employee=random.choice(employees),
            title=f"Business Trip {i}",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
            purpose_of_trip="Client meeting",
            place_of_visit="San Francisco"
        )

    print("Seeding Warnings...")
    for i in range(5):
        Warning.objects.create(
            company=company,
            warning_by=random.choice(employees),
            warning_to=random.choice(employees),
            warning_type="Behavioral",
            warning_date=date.today(),
            description=f"Talking too loud {i}"
        )

    print("Seeding Complaints...")
    for i in range(5):
        Complaint.objects.create(
            company=company,
            complainant=random.choice(employees),
            against_employee=random.choice(employees),
            complaint_type="Noise",
            complaint_date=date.today(),
            description=f"He plays music without headphones {i}"
        )

    print("Seeding Announcements...")
    for i in range(5):
        Announcement.objects.create(
            company=company,
            title=f"Announcement {i}",
            category="GENERAL",
            content="This is a test announcement",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            is_company_wide_announcement=True
        )

    print("Seeding Asset Types and Assets...")
    for i in range(1, 6):
        at = AssetType.objects.create(
            company=company,
            asset_type_name=f"Asset Type {i}"
        )
        Assets.objects.create(
            company=company,
            asset_name=f"Asset {i}",
            asset_type=at,
            serial_number=f"SN-{random.randint(10000, 99999)}-{i}",
            asset_code=f"ASSET-{random.randint(1000, 9999)}-{i}",
            purchase_date=date.today(),
            purchase_cost=500.00,
            status="approved",
            condition="excellent",
            depreciation_method="straight_line",
            useful_life=5
        )

    print("Seeding Training models...")
    for i in range(1, 6):
        tt = TrainingType.objects.create(
            company=company,
            name=f"Training Type {i}",
            branch=random.choice(branches)
        )
        tp = TrainingProgram.objects.create(
            company=company,
            name=f"Program {i}",
            training_type=tt,
            duration=40,
            status="active"
        )
        ts = TrainingSession.objects.create(
            company=company,
            training_program=tp,
            session_name=f"Session {i}",
            start_date=date.today(),
            end_date=date.today(),
            status="active",
            trainer=random.choice(employees)
        )
        AssignTraining.objects.create(
            company=company,
            employee=random.choice(employees),
            training_program=tp,
            status="assigned",
            assigned_date=date.today()
        )

    print("Seeding Done!")

if __name__ == "__main__":
    seed_data()
