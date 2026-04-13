from django.conf import settings
from shared.logs import log_activity
from django.core.mail import send_mail
from rest_framework.views import APIView
from datetime import date, timedelta, datetime
from django.shortcuts import get_object_or_404
from ..utils import renew_company_subscription
from shared.utils.common import check_permissions
import base64, hashlib, io, qrcode, requests, uuid
from django.template.loader import render_to_string
from shared.models import Company,Subscription,UserActivityLog
from shared.utils.response import ResponseHandler,ResponseMessages

class SubscriptionRenewView(APIView):
    @log_activity(UserActivityLog.RENEW, 'Payment Renew')
    def post(self, request):
        check_permissions(request, ['renew_subscription'])

        company_id = request.data.get('company')
        payment_mode = request.data.get('payment_mode')
        amount = request.data.get('amount_paid')
        remarks = request.data.get('remarks')
        send_email = str(request.data.get('send_email', 'true')).lower() == 'true'
        company = get_object_or_404(Company, id=company_id)

        plan_t = company.plan_type
        if not plan_t:
            return ResponseHandler.bad_request(message=ResponseMessages.NOT_ACTIVE_PLAN)

        plan_duration = getattr(plan_t, 'duration_days', 30)
        current_end = company.subscription_end_date or date.today()

        new_start = date.today() if current_end < date.today() else current_end + timedelta(days=1)
        new_end = new_start + timedelta(days=plan_duration)

        if not amount:
            if company.allow_plan_renewal_on_same_price:
                amount = company.amount_paid
            else:
                amount = getattr(plan_t, 'plan_price_inr', 0)

        txnid = f"TXN-{company.id}-{uuid.uuid4().hex[:8]}"

        subscription_data = {
            "company_id": company,
            "transaction_ref_no": txnid,
            "amount_paid": amount,
            "plan_type": plan_t,
            "plan_activation_date": new_start,
            "subscription_end_date": new_end,
            "payment_mode": payment_mode,
            "remarks": remarks,
            "status": 'Paid' if payment_mode.lower() != 'online' else 'Pending',
            "gateway": 'Offline' if payment_mode.lower() != 'online' else 'Easebuzz',
            "gateway_response": None if payment_mode.lower() != 'online' else {}
        }

        if payment_mode.lower() == 'cash':
            Subscription.objects.create(**subscription_data)
            renew_company_subscription(company, plan_t, new_start, payment_mode, 'Paid')
            return ResponseHandler.success(
                message=f"Subscription renewed successfully with offline payment. Valid from {new_start.strftime('%d-%b-%Y')} to {new_end.strftime('%d-%b-%Y')}."
            )

        try:
            key = settings.EASEBUZZ_KEY
            salt = settings.EASEBUZZ_SALT
            surl = settings.EASEBUZZ_SUCCESS_URL
            furl = settings.EASEBUZZ_FAILURE_URL
            productinfo = "Subscription Payment"
            hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{company.company_name}|{company.email}|||||||||||{salt}"
            hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

            payload = {
                "txnid": txnid,
                "amount": str(amount),
                "firstname": company.company_name,
                "email": company.email,
                "phone": company.phone_number,
                "productinfo": productinfo,
                "surl": surl,
                "furl": furl,
                "key": key,
                "hash": hashh
            }

            response = requests.post("https://pay.easebuzz.in/payment/initiateLink", data=payload)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == 1:
                data = response_data.get("data", {})
                payment_token = data if isinstance(data, str) else data.get("link")

                expiry_time_iso = None
                if isinstance(data, dict):
                    expiry_time_iso = data.get("link_expiry_time") or data.get("expiry") or data.get("expires_at")
                if not expiry_time_iso:
                    expiry_time_iso = (datetime.utcnow() + timedelta(minutes=15)).isoformat() + 'Z'

                if not isinstance(payment_token, str):
                    return ResponseHandler.bad_request(
                        response_data={"gateway_response": response_data},
                        message=ResponseMessages.PAYMENT_TOKEN_MISSING
                    )

                Subscription.objects.create(**subscription_data)

                payment_link = f"https://pay.easebuzz.in/pay/{payment_token}"
                qr = qrcode.make(payment_link)
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()
                expiry_dt = datetime.fromisoformat(expiry_time_iso.replace("Z", "+00:00"))
                expiry_time_human = expiry_dt.strftime('%B %d, %Y at %I:%M %p UTC')

                if send_email:
                    message = render_to_string('email_templates/Renew_subscription_payment_link.html', {
                        'client_name': company.company_name,
                        'payment_link': payment_link,
                        'expiry_time': expiry_time_human,
                    })
                    subject = "Subscription Payment Link"
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [company.email],
                            html_message=message,
                        )
                    except Exception as email_error:
                        pass

                return ResponseHandler.success({
                    "payment_link": payment_link,
                    "qr_code": qr_base64,
                    "link_expiry_time": expiry_time_iso
                }, message=f"Payment initiated. Subscription valid from {new_start.strftime('%d-%b-%Y')} to {new_end.strftime('%d-%b-%Y')}.")

            else:
                error_msg = response_data.get("data", {}).get("message") or response_data.get("message", "Payment failed.")
                return ResponseHandler.bad_request({"gateway_response": response_data}, message=error_msg)

        except Exception as e:
            return ResponseHandler.server_error(message=ResponseMessages.PAYMENT_GATEWAY_ERROR, err=e)
