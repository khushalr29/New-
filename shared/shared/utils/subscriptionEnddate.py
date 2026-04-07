from datetime import timedelta

def get_subscription_end_date(start_date, payment_duration):
    duration_mapping = {
        "monthly": 30,
        "quarterly": 90,
        "yearly": 365
    }
    days = duration_mapping.get(payment_duration.strip().lower(), 365)
    return start_date + timedelta(days=days)

def update_company_subscription(company, plan, start_date, payment_mode, payment_status):
    end_date = get_subscription_end_date(start_date, plan.payment_duration)
    company.plan_type = plan
    company.plan_activation_date = start_date
    company.subscription_end_date = end_date
    company.amount_paid = plan.plan_price_inr
    company.no_of_user = plan.no_of_user
    company.no_of_company = plan.no_of_company
    company.payment_mode = payment_mode
    company.payment_status = payment_status
    company.save()
    return end_date
