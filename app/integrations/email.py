import resend
from resend import Emails

from core.config import config
from core.utils.current_timestamp import current_timestamp

resend.api_key = config.RESEND_API_KEY


class EmailService:
    """Service for sending emails via Resend"""

    @staticmethod
    def send_verification_email(
        to_email: str, verification_token: str, user_name: str
    ) -> Emails.SendResponse:
        """Send email verification link"""
        verification_link = (
            f"{config.FRONTEND_URL}/verify-email?token={verification_token}"
        )

        params: resend.Emails.SendParams = {
            "from": config.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "Verify Your Email Address",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Welcome {user_name}!</h2>
                    <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
                    <div style="margin: 30px 0;">
                        <a href="{verification_link}" 
                           style="background-color: #4F46E5; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 6px; display: inline-block;">
                            Verify Email Address
                        </a>
                    </div>
                    <p style="color: #6B7280; font-size: 14px;">
                        Or copy this link: <br/>
                        <code style="background: #F3F4F6; padding: 4px 8px; border-radius: 4px;">
                            {verification_link}
                        </code>
                    </p>
                    <p style="color: #6B7280; font-size: 12px;">
                        This link will expire in 24 hours.
                    </p>
                </div>
            """,
        }

        return resend.Emails.send(params)

    @staticmethod
    def send_password_reset_email(
        to_email: str, reset_token: str, user_name: str
    ) -> resend.Emails.SendResponse:
        """Send password reset link"""
        reset_link = f"{config.FRONTEND_URL}/reset-password?token={reset_token}"

        params: resend.Emails.SendParams = {
            "from": config.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "Reset Your Password",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Password Reset Request</h2>
                    <p>Hello {user_name},</p>
                    <p>We received a request to reset your password. Click the button below to create a new password:</p>
                    <div style="margin: 30px 0;">
                        <a href="{reset_link}" 
                           style="background-color: #EF4444; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 6px; display: inline-block;">
                            Reset Password
                        </a>
                    </div>
                    <p style="color: #6B7280; font-size: 14px;">
                        Or copy this link: <br/>
                        <code style="background: #F3F4F6; padding: 4px 8px; border-radius: 4px;">
                            {reset_link}
                        </code>
                    </p>
                    <p style="color: #DC2626; font-size: 14px;">
                        If you didn't request this, please ignore this email and your password will remain unchanged.
                    </p>
                    <p style="color: #6B7280; font-size: 12px;">
                        This link will expire in 1 hour.
                    </p>
                </div>
            """,
        }

        return resend.Emails.send(params)

    @staticmethod
    def send_password_changed_email(
        to_email: str, user_name: str
    ) -> resend.Emails.SendResponse:
        """Notify user that password was changed"""
        params: resend.Emails.SendParams = {
            "from": config.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "Password Changed Successfully",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Password Changed</h2>
                    <p>Hello {user_name},</p>
                    <p>Your password has been successfully changed.</p>
                    <p style="color: #DC2626; font-size: 14px;">
                        If you didn't make this change, please contact support immediately.
                    </p>
                    <p style="color: #6B7280; font-size: 12px;">
                        Changed at: {current_timestamp()} UTC
                    </p>
                </div>
            """,
        }

        return resend.Emails.send(params)

    @staticmethod
    def send_login_notification(
        to_email: str,
        user_name: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> resend.Emails.SendResponse:
        """Notify user of successful login"""
        location_info = f"IP: {ip_address}" if ip_address else "Unknown location"
        device_info = user_agent if user_agent else "Unknown device"

        params: resend.Emails.SendParams = {
            "from": config.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "New Login to Your Account",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>New Login Detected</h2>
                    <p>Hello {user_name},</p>
                    <p>A new login was detected on your account:</p>
                    <ul style="background: #F3F4F6; padding: 20px; border-radius: 6px;">
                        <li><strong>Time:</strong> {current_timestamp()} UTC</li>
                        <li><strong>Location:</strong> {location_info}</li>
                        <li><strong>Device:</strong> {device_info}</li>
                    </ul>
                    <p style="color: #DC2626; font-size: 14px;">
                        If this wasn't you, please secure your account immediately by changing your password.
                    </p>
                </div>
            """,
        }

        return resend.Emails.send(params)

    @staticmethod
    def send_logout_notification(
        to_email: str, user_name: str
    ) -> resend.Emails.SendResponse:
        """Notify user of logout"""
        params: resend.Emails.SendParams = {
            "from": config.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "Logged Out Successfully",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Logged Out</h2>
                    <p>Hello {user_name},</p>
                    <p>You have been successfully logged out of your account.</p>
                    <p style="color: #6B7280; font-size: 12px;">
                        Time: {current_timestamp()} UTC
                    </p>
                    <p style="color: #DC2626; font-size: 14px;">
                        If you didn't perform this action, please contact support.
                    </p>
                </div>
            """,
        }

        return resend.Emails.send(params)

    @staticmethod
    def send_welcome_email(to_email: str, user_name: str) -> resend.Emails.SendResponse:
        """Send welcome email after successful registration"""

        params: resend.Emails.SendParams = {
            "from": config.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "Welcome",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Welcome aboard, {user_name}! 🎉</h2>
                    
                    <p>We're excited to have you.</p>
                    
                    <p>You can now explore all features and start using your account.</p>

                    <div style="margin: 30px 0;">
                        <a href="{config.FRONTEND_URL}" 
                        style="background-color: #10B981; color: white; padding: 12px 24px; 
                                text-decoration: none; border-radius: 6px; display: inline-block;">
                            Go to Dashboard
                        </a>
                    </div>

                    <p style="color: #6B7280; font-size: 14px;">
                        If you have any questions, feel free to reach out to our support team.
                    </p>

                    <p style="color: #6B7280; font-size: 12px;">
                        Joined at: {current_timestamp()} UTC
                    </p>
                </div>
            """,
        }

        return resend.Emails.send(params)
