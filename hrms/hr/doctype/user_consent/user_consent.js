// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("User Consent", {
    refresh(frm) {
        // Check if the document is already created (not new)
        if (!frm.is_new()) {
            // Set the related_user field to read-only
            frm.set_df_property("related_user", "read_only", 1);
            frm.set_df_property("request_details", "read_only", 1);
			if(frm.doc.approve){
				frm.set_df_property("approve", "read_only", 1);
			}
        }
		// Send a backend request to get consent attachments
		frappe.call({
			method: "hrms.hr.doctype.user_consent.user_consent.get_consent_attachments",
			args: {
				request_details: frm.doc.request_details
			},
			callback: function (r) {
				if (r.message) {
					// Clear existing attachments
					frm.clear_table("attachments");

					// Add each attachment to the attachment child table
					r.message.forEach(attachment => {
						let child = frm.add_child("attachments");
						child.attachment = attachment;
					});

					// Refresh the field to show the new attachments
					frm.refresh_field("attachments");
					frm.set_df_property("attachments", "read_only", 1);
				}
			}
		});
	},
});

