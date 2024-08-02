// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Consent Request", {
	refresh(frm) {
		if (!frm.is_new()) {
            // Set the related_user field to read-only
            frm.set_df_property("topic", "read_only", 1);
            frm.set_df_property("attachments", "read_only", 1);
			frm.set_df_property("dutch_description", "read_only", 1);
			frm.set_df_property("english_description", "read_only", 1);
			frm.set_df_property("turkish_description", "read_only", 1);
			frm.set_df_property("polish_description", "read_only", 1);
        }
	},
});
