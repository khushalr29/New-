import io
import uuid
import qrcode
import base64
import hashlib
import requests
from django.conf import settings
from shared.logs import log_activity
from django.core.mail import send_mail
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from shared.models import Company,Subscription,UserActivityLog
from shared.utils.response import ResponseHandler,ResponseMessages

class CreateEasebuzzPaymentView(APIView):
    @log_activity(UserActivityLog.CREATE, 'Payment')
    def post(self, request):
        company_id = request.data.get('company_id')
        send_email = str(request.data.get('send_email', 'true')).lower() == 'true'
        company = get_object_or_404(Company, pk=company_id)

        if company.payment_mode.lower() == 'cash':
            return ResponseHandler.bad_request(message=ResponseMessages.PAYMENT_MODE_ERROR)

        plan_type = company.plan_type
        plan_activation_date = company.plan_activation_date
        subscription_end_date = company.subscription_end_date
        payment_mode = company.payment_mode
        amount = company.amount_paid
        txnid = f"TXN-{company_id}-{uuid.uuid4().hex[:8]}"

        key = settings.EASEBUZZ_KEY
        salt = settings.EASEBUZZ_SALT
        surl = settings.EASEBUZZ_SUCCESS_URL
        furl = settings.EASEBUZZ_FAILURE_URL
        productinfo = "Subscription Payment"
        hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{company.client_name}|{company.client_email}|||||||||||{salt}"
        hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

        payload = {
            "txnid": txnid,
            "amount": str(amount),
            "firstname": company.client_name,
            "email": company.client_email,
            "phone": company.client_number,
            "productinfo": productinfo,
            "surl": surl,
            "furl": furl,
            "key": key,
            "hash": hashh
        }

        try:
            response = requests.post("https://pay.easebuzz.in/payment/initiateLink", data=payload)

            try:
                response_data = response.json()
            except ValueError:
                return ResponseHandler.bad_request(
                    response_data={"raw_response": response.text},
                    message=ResponseMessages.INVALID_JSON_RESPONSE
                )

            if response.status_code == 200 and response_data.get("status") == 1:
                data = response_data.get("data", {})
                payment_token = data if isinstance(data, str) else data.get("link")

                expiry_time_iso = None
                if isinstance(data, dict):
                    expiry_time_iso = data.get("link_expiry_time") or data.get("expiry") or data.get("expires_at")

                if not expiry_time_iso:
                    expiry_time_iso = (datetime.utcnow() + timedelta(minutes=15)).isoformat() + 'Z'

                try:
                    expiry_dt = datetime.fromisoformat(expiry_time_iso.replace("Z", "+00:00"))
                except Exception:
                    expiry_dt = datetime.utcnow() + timedelta(minutes=15)

                expiry_time_human = expiry_dt.strftime('%B %d, %Y at %I:%M %p')

                if not isinstance(payment_token, str):
                    return ResponseHandler.bad_request(
                        response_data={"gateway_response": response_data},
                        message=ResponseMessages.PAYMENT_TOKEN_MISSING
                    )

                Subscription.objects.create(
                    company_id=company_id,
                    transaction_ref_no=txnid,
                    amount_paid=amount,
                    plan_type=plan_type,
                    plan_activation_date=plan_activation_date,
                    subscription_end_date=subscription_end_date,
                    payment_mode=payment_mode,
                    status='Pending',
                    gateway='Easebuzz',
                    gateway_response=response_data
                )

                payment_link = f"https://pay.easebuzz.in/pay/{payment_token}"
                qr = qrcode.make(payment_link)
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()

                if send_email:
                    message = render_to_string('email_templates/create_subscription_payment_link.html', {
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
                    except Exception as email_error:
                        pass

                return ResponseHandler.success(
                    response_data={
                        "payment_link": payment_link,
                        "qr_code": qr_base64,
                        "link_expiry_time": expiry_time_iso
                    },
                    message=ResponseMessages.PAYMENT_INITIATED
                )

            else:
                data = response_data.get("data")
                error_message = data.get("message") if isinstance(data, dict) else response_data.get("message", ResponseMessages.PAYMENT_INITIATION_FAILED)

                return ResponseHandler.bad_request(
                    response_data={"gateway_response": response_data},
                    message=error_message
                )

        except Exception as e:
            return ResponseHandler.server_error(
                response_data=None,
                message=ResponseMessages.PAYMENT_GATEWAY_ERROR,
                err=e
            )
