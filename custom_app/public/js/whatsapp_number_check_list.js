frappe.listview_settings['Whatsapp Number Check'] = {
    onload: function(listview) {
        listview.page.add_action_item(__("Send Whatsapp Message"), function() {
            make_popup(listview)
        });
    }
};


function make_popup(listview){
    data = []
    $.each(listview.get_checked_items(), function(key, value) {
        // console.log("value", value)
        data.push(value)
    });
    let d = new frappe.ui.Dialog({
        title: 'Enter details',
        fields: [
            {
                label: 'Content Type',
                fieldname: 'type',
                fieldtype: 'Select',
                options: ["Message", "Video", "Document", "Image"],
            },
            {
                label: 'Message',
                fieldname: 'message',
                fieldtype: 'Data',
                depends_on: 'eval: doc.type == "Message"'
            },
            {
                label: 'Video Link',
                fieldname: 'video_link',
                fieldtype: 'Attach',
                depends_on: 'eval: doc.type == "Video"'
            },
            {
                label: 'Document Link',
                fieldname: 'document_link',
                fieldtype: 'Attach',
                depends_on: 'eval: doc.type == "Document"'
            },
            {
                label: 'Image Link',
                fieldname: 'image_link',
                fieldtype: 'Attach Image',
                depends_on: 'eval: doc.type == "Image"'
            },
            {
                label: 'Caption',
                fieldname: 'caption',
                fieldtype: 'Data',
                depends_on: 'eval: doc.type == "Video" ||  doc.type == "Document" ||  doc.type == "Image"'
            },
          
        ],
        size: 'small', // small, large, extra-large 
        primary_action_label: 'Send Video',
        primary_action(values) {
            console.log(values);

            frappe.call({
                method: 'custom_app.api.send_whatsapp_message',
                args:{
                    data: data,
                    details: values
                }
            })

            d.hide();
        }
    });
    
    d.show();
    if (names.length === 0) {
        frappe.throw(__("No rows selected."));
    }
}