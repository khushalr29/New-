from django.conf import settings
from shared.logs import log_activity
from django.core.mail import send_mail
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import uuid, hashlib, requests, qrcode,io,base64
from django.template.loader import render_to_string
from shared.utils.common import check_permissions
from shared.utils.response import ResponseHandler,ResponseMessages
from shared.models import Company, Plan,Subscription,UserActivityLog
from ..utils import get_subscription_end_date,update_company_subscription

class UpdateSubscriptionView(APIView):
    @log_activity(UserActivityLog.UPGRADE, 'Payment')
    def post(self, request):
        check_permissions(request, ['upgrade_subscription'])

        company_id = request.data.get('company')
        new_plan_id = request.data.get('plan_id')
        amount = request.data.get('amount_paid')
        remarks = request.data.get('remarks')
        payment_mode = request.data.get('payment_mode')
        send_email = str(request.data.get('send_email', 'true')).lower() == 'true'

        if not company_id or not new_plan_id:
            return ResponseHandler.bad_request(message=ResponseMessages.ID_REQUIRED)

        company = get_object_or_404(Company, pk=company_id)
        new_plan = get_object_or_404(Plan, pk=new_plan_id)

        if company.plan_type == new_plan:
            return ResponseHandler.bad_request(message=ResponseMessages.SUBSCRIBED_PLAN_ERROR)

        txnid = f"UPG-{company_id}-{uuid.uuid4().hex[:8]}"
        today = datetime.today().date()

        current_end_date = company.subscription_end_date or today
        new_start_date = today if current_end_date < today else current_end_date + timedelta(days=1)
        end_date = get_subscription_end_date(new_start_date, new_plan.payment_duration)
        is_offline = payment_mode.lower() == 'cash'

        if is_offline:
            if not amount or not str(amount).replace('.', '', 1).isdigit():
                return ResponseHandler.bad_request(message="Valid amount is required for offline payments.")
            amount_paid = float(amount)
        else:
            if not amount or not str(amount).replace('.', '', 1).isdigit():
                amount_paid = new_plan.plan_price_inr
            else:
                try:
                    amount_paid = float(amount)
                except (ValueError, TypeError):
                    return ResponseHandler.bad_request(message="Invalid amount provided.")

        subscription_data = {
            "company_id": company,
            "transaction_ref_no": txnid,
            "amount_paid": amount_paid,
            "plan_type": new_plan,
            "plan_activation_date": new_start_date,
            "subscription_end_date": end_date,
            "payment_mode": payment_mode,
            "status": 'Paid' if is_offline else 'Pending',
            "gateway": 'Offline' if is_offline else 'Easebuzz',
            "gateway_response": None if is_offline else {},
            "remarks": remarks,
        }
        Subscription.objects.create(**subscription_data)

        if is_offline:
            update_company_subscription(company, new_plan, new_start_date, payment_mode, 'Paid')
            return ResponseHandler.success(
                response_data={"transaction_ref_no": txnid, "status": "Paid"},
                message=ResponseMessages.SUBSCRIPTION_UPGRADED
            )

        key = settings.EASEBUZZ_KEY
        salt = settings.EASEBUZZ_SALT
        surl = settings.EASEBUZZ_SUCCESS_URL
        furl = settings.EASEBUZZ_FAILURE_URL
        productinfo = "Subscription Upgrade"

        hash_string = f"{key}|{txnid}|{amount_paid}|{productinfo}|{company.client_name}|{company.client_email}|||||||||||{salt}"
        hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

        payload = {
            "txnid": txnid,
            "amount": str(amount_paid),
            "firstname": company.client_name,
            "email": company.client_email,
            "phone": company.client_number,
            "productinfo": productinfo,
            "surl": surl,
            "furl": furl,
            "key": key,
            "hash": hashh,
        }

        try:
            response = requests.post("https://pay.easebuzz.in/payment/initiateLink", data=payload)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == 1:
                data = response_data.get("data", {})

                if isinstance(data, str):
                    payment_token = data
                    expiry_time_iso = (datetime.utcnow() + timedelta(minutes=15)).isoformat() + 'Z'
                elif isinstance(data, dict):
                    payment_token = data.get("link")
                    expiry_time_iso = (
                        data.get("link_expiry_time")
                        or data.get("expiry")
                        or data.get("expires_at")
                        or (datetime.utcnow() + timedelta(minutes=15)).isoformat() + 'Z'
                    )
                else:
                    return ResponseHandler.bad_request(
                        response_data={"gateway_response": response_data},
                        message="Unexpected gateway data format."
                    )

                if not isinstance(payment_token, str) or not payment_token:
                    return ResponseHandler.bad_request(
                        response_data={"gateway_response": response_data},
                        message=ResponseMessages.PAYMENT_TOKEN_MISSING
                    )

                try:
                    expiry_dt = datetime.fromisoformat(expiry_time_iso.replace("Z", "+00:00"))
                except Exception:
                    expiry_dt = datetime.utcnow() + timedelta(minutes=15)

                expiry_time_human = expiry_dt.strftime('%B %d, %Y at %I:%M %p UTC')

                payment_link = f"https://pay.easebuzz.in/pay/{payment_token}"
                qr = qrcode.make(payment_link)
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()

                if send_email:
                    message = render_to_string('email_templates/upgrade_subscription_payment_link.html', {
                        'client_name': company.client_name,
                        'payment_link': payment_link,
                        'expiry_time': expiry_time_human,
                    })
                    subject = "Subscription Payment Link"
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [company.client_email],
                            html_message=message,
                        )
                    except Exception:
                        pass

                return ResponseHandler.success(
                    response_data={
                        "payment_link": payment_link,
                        "qr_code": qr_base64,
                        "link_expiry_time": expiry_time_iso,
                    },
                    message=ResponseMessages.PAYMENT_INITIATED,
                )

            else:
                return ResponseHandler.bad_request(
                    response_data={"gateway_response": response_data},
                    message=ResponseMessages.PAYMENT_INITIATION_FAILED,
                )

        except Exception as e:
            return ResponseHandler.server_error(
                message=ResponseMessages.PAYMENT_GATEWAY_ERROR,
                err=e,
            )
