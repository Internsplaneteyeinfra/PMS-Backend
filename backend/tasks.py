from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_html_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Send an HTML email using a Django template.
    """
    try:
        logger.info(f"Sending email '{subject}' to recipients: {recipient_list}")

        # Check for empty emails in recipient list
        empty_emails = [email for email in recipient_list if not email or not email.strip()]
        if empty_emails:
            logger.error(f"FOUND EMPTY EMAILS IN RECIPIENT LIST: {empty_emails}")
            logger.error(f"Full recipient list: {recipient_list}")
            import traceback
            logger.error(f"Call stack: {''.join(traceback.format_stack())}")
            return False

        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL

        template_path = f'emails/{template_name}.html'
        logger.info(f"Loading template: {template_path}")

        # Add base_url to context for absolute URLs in emails
        context = context.copy()
        context['base_url'] = settings.BASE_URL

        # Render the HTML content
        html_content = render_to_string(template_path, context)

        # Log first 200 chars of content for debugging
        logger.info(f"Email content preview: {html_content[:200]}...")

        # Filter out empty or invalid email addresses
        valid_recipients = []
        for email in recipient_list:
            if isinstance(email, str) and email.strip():
                valid_recipients.append(email.strip())

        if not valid_recipients:
            logger.warning("No valid email recipients found, skipping email send")
            return False

        # Send the email
        result = send_mail(
            subject=subject,
            message='',  # Plain text message (empty for HTML-only)
            html_message=html_content,
            from_email=from_email,
            recipient_list=valid_recipients,
            fail_silently=False,
        )

        if result == 1:  # send_mail returns number of successfully sent emails
            logger.info(f"Email sent successfully to {recipient_list}")
            return True
        else:
            logger.error(f"Failed to send email to {recipient_list}")
            return False

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False


