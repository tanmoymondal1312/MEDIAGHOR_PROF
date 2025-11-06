from django.http import JsonResponse
from .models import SubscribeModel,Contact
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.core.mail import send_mail
import threading
from django.conf import settings



def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Please enter an email address.'})

        if SubscribeModel.objects.filter(email=email).exists():
            return JsonResponse({'status': 'info', 'message': 'You are already subscribed!'})

        SubscribeModel.objects.create(email=email, subject="New Subscription")
        return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



@csrf_exempt  # Remove this if you are sending a CSRF token from JS
@require_POST
def ContactView(request):
    print("Hello")
    try:
        # Parse JSON data from request body
        data = json.loads(request.body.decode('utf-8'))

        # Create and save Contact entry
        contact = Contact.objects.create(
            sender_name=data.get('name', ''),
            sender_mail=data.get('email', ''),
            sender_phone=data.get('phone', None),
            title=data.get('service', ''),  # or "subject" if that's more appropriate
            message=data.get('message', '')[:5000]
        )
        try:
            contact_notify_to_admin(contact)
        except Exception as email_error:
            print(f"Email notification failed (non-critical): {str(email_error)}")
        

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Message received successfully.'}, status=200)

    except Exception as e:
        print("Error saving contact form:", e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



def contact_notify_to_admin(contact):
    """
    Send notification email to admin about new Contact.
    """
    def _send():
        try:
            subject = f"Someone Want to Contact: {contact.id}"
            message = f"""
            Contactor Details:
            ---------------
            Request ID: #{contact.id}
            Contactor Name: {contact.sender_name}
            Contactor Email: {contact.sender_mail}
            Contactor Number: {contact.sender_phone}
            
            Message Body:
            ---------------
            Title: {contact.title}
            Message: {contact.message}

            Please Contact as soon as posible.
            """

            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["tanmoymondal1315@gmail.com"],
                fail_silently=False,
            )

            print(f"✅ Admin email sent for resource")

        except Exception as e:
            print(f"❌ Error sending admin notification: {str(e)}")

    # Start async thread
    threading.Thread(target=_send).start()
