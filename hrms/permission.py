import frappe


def user_consent_query(user):
    # Get the current user's email
    user_email = user

    allowed_roles = ["System Manager", "Projectleider"]

    # Check if the user has admin privileges
    if any(role in allowed_roles for role in frappe.get_roles(user_email)):
        # Return a condition that includes all users
        return "1 = 1"

    # if related user is the current user then show the consent request
    return f"(`tabUser Consent`.related_user = '{user_email}')"
