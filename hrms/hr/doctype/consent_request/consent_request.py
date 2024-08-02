# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document


class ConsentRequest(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from erpnext.projects.doctype.employee_child_link.employee_child_link import EmployeeChildLink
        from frappe.types import DF

        assigned_user: DF.TableMultiSelect[EmployeeChildLink]
        attachments: DF.Attach | None
        creator: DF.Data | None
        date: DF.Datetime | None
        description: DF.TextEditor
        naming_series: DF.Literal["APPREQ-.####"]
        roles: DF.Link | None
        share_with: DF.Literal["All Users", "Role", "Employees"]
        topic: DF.Data | None
    # end: auto-generated types

    def on_trash(self):
        current_users = get_users_by_share_with_type(self)
        for user in current_users:
            frappe.db.delete("User Consent", {"related_user": user, "request_details": self.name})
        return

    def validate(self):
        if not frappe.db.exists("Consent Request", self.name):
            # Handle the case where the record does not exist
            return
        # Retrieve the non-modified object from the database
        original = frappe.get_doc("Consent Request", self.name)

        original_users = get_users_by_share_with_type(original)
        current_users = get_users_by_share_with_type(self)

        # Users to be deleted (in original but not in current)
        users_to_delete = original_users - current_users
        for user in users_to_delete:
            frappe.db.delete("User Consent", {"related_user": user, "request_details": self.name})

        # Users to be added (in current but not in original)
        users_to_add = current_users - original_users
        for user in users_to_add:
            consent_request = frappe.new_doc("User Consent")
            consent_request.related_user = user
            consent_request.request_details = self.name
            set_consent_request_details(consent_request, self)
            consent_request.insert()

        return

    def after_insert(self):
        shared_with_type = self.share_with
        if shared_with_type == "All Users":
            # get all users
            all_users = frappe.get_all("User", fields=["name"])
            for user in all_users:
                # for each user, we have to create a new User Consent document
                consent_request = frappe.new_doc("User Consent")
                consent_request.related_user = user.name
                consent_request.request_details = self.name
                set_consent_request_details(consent_request, self)
                consent_request.save()
        elif shared_with_type == "Role":
            # get all users in the role
            all_users = frappe.get_all("Has Role", filters={"parenttype": "User", "role": self.roles}, fields=["parent"])
            for user in all_users:
                # for each user, we have to create a new User Consent document
                consent_request = frappe.new_doc("User Consent")
                consent_request.related_user = user.parent
                consent_request.request_details = self.name
                set_consent_request_details(consent_request, self)
                consent_request.save()
        elif shared_with_type == "Employees":
            # get all users in the role
            all_users = self.assigned_user
            for user in all_users:
                # for each user, we have to create a new User Consent document
                consent_request = frappe.new_doc("User Consent")
                # from the user.employee we need to get the real user and assign the approval request to that user
                employee = frappe.get_value("Employee", user.employee, "user_id")
                user = frappe.get_value("User", {"email": employee}, "name")
                consent_request.related_user = user
                consent_request.request_details = self.name
                set_consent_request_details(consent_request, self)
                consent_request.insert()
        return


def get_users_by_share_with_type(consent_request):
    if consent_request.share_with == "Role":
        return set(frappe.get_all("Has Role", filters={"parenttype": "User", "role": consent_request.roles}, pluck="parent"))
    elif consent_request.share_with == "Employees":
        # from the consent_request.assigned_user we need to get the real user and assign the approval request to that user
        employees = [frappe.get_value("Employee", employee.employee, "user_id") for employee in consent_request.assigned_user]
        return set(frappe.get_all("User", filters={"email": ["in", employees]}, pluck="name"))
    elif consent_request.share_with == "All Users":
        return set(frappe.get_all("User", pluck="name"))
    return set()


def set_consent_request_details(consent_request, self):
    consent_request.topic = self.topic
    consent_request.language = self.language
    consent_request.dutch_description = self.dutch_description
    consent_request.english_description = self.english_description
    consent_request.turkish_description = self.turkish_description
    consent_request.polish_description = self.polish_description
