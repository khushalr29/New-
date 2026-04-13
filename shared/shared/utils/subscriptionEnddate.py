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

def renew_company_subscription(company, plan, start_date, payment_mode, payment_status):
    end_date = get_subscription_end_date(start_date, plan.payment_duration)
    company.plan_activation_date = start_date
    company.subscription_end_date = end_date
    company.payment_mode = payment_mode
    company.payment_status = payment_status
    company.save()
    return end_date

def verify_easebuzz_payment(txnid, payment_data):

    try:
        received_hash = payment_data.get('hash', '')
        status = payment_data.get('status', '')
        amount = payment_data.get('amount', '')
        productinfo = payment_data.get('productinfo', '')
        firstname = payment_data.get('firstname', '')
        email = payment_data.get('email', '')
        
        udf1 = payment_data.get('udf1', '')
        udf2 = payment_data.get('udf2', '')
        udf3 = payment_data.get('udf3', '')
        udf4 = payment_data.get('udf4', '')
        udf5 = payment_data.get('udf5', '')
        udf6 = payment_data.get('udf6', '')
        udf7 = payment_data.get('udf7', '')
        udf8 = payment_data.get('udf8', '')
        udf9 = payment_data.get('udf9', '')
        udf10 = payment_data.get('udf10', '')
        
        if not received_hash:
            return False, 'Failed', "Missing hash"
        
        hash_string = f"{settings.EASEBUZZ_SALT}|{status}|{udf10}|{udf9}|{udf8}|{udf7}|{udf6}|{udf5}|{udf4}|{udf3}|{udf2}|{udf1}|{email}|{firstname}|{productinfo}|{amount}|{txnid}|{settings.EASEBUZZ_KEY}"
        
        calculated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
        
        if calculated_hash != received_hash:
            return False, 'Failed', "Hash verification failed"        
        if not txnid or not amount or not email:
            return False, 'Failed', "Missing required fields"
        
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                return False, 'Failed', "Invalid amount"
        except (ValueError, TypeError):
            return False, 'Failed', "Invalid amount format"
        
        return True, status, "Verification successful"
        
    except Exception as e:
        return False, 'Failed', "Verification error"