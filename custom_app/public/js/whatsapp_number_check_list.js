frappe.listview_settings['Whatsapp Number Check'] = {
    onload: function(listview) {
        listview.page.add_action_item(__("Send Whatsapp Message"), function() {
            make_popup(listview)
        });

        listview.page.add_action_item(__("Check Whatsapp Number"), function() {
            check_number(listview)
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
                reqd: 1
            },
            {
                label: 'Message',
                fieldname: 'message',
                fieldtype: 'Small Text',
                depends_on: 'eval: doc.type == "Message"',
                mandatory_depends_on: 'eval: doc.type == "Message"',
                description: "Max length : 4096 characters."
            },
            {
                label: 'Video Link',
                fieldname: 'video_link',
                fieldtype: 'Attach',
                depends_on: 'eval: doc.type == "Video"',
                mandatory_depends_on: 'eval: doc.type == "Video"',
                description: "Supported extensions : ( mp4 , 3gp , mov ) </br> Max file size : 16MB"
            },
            {
                label: 'Document Link',
                fieldname: 'document_link',
                fieldtype: 'Attach',
                depends_on: 'eval: doc.type == "Document"',
                mandatory_depends_on: 'eval: doc.type == "Document"',
                description: "Supported most extensions like : ( zip , xlsx , csv , txt , pptx , docx ....etc ) </br>Max file size : 30MB"
            },
            {
                label: 'Image Link',
                fieldname: 'image_link',
                fieldtype: 'Attach Image',
                depends_on: 'eval: doc.type == "Image"',
                mandatory_depends_on: 'eval: doc.type == "Image"',
                description: "Supported extensions:  ( jpg , jpeg , gif , png , webp , bmp ). </br> Max file size : 16MB"
            },
            {
                label: 'Caption',
                fieldname: 'caption',
                fieldtype: 'Small Text',
                depends_on: 'eval: doc.type == "Video" ||  doc.type == "Document" ||  doc.type == "Image"',
                description: "Max length : 1024 char."
            },
          
        ],
        size: 'small', // small, large, extra-large
        primary_action_label: 'Send Messsage',
        primary_action(values) {
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


// check number is using whatsapp or not

function check_number(listview){
    data = []
    $.each(listview.get_checked_items(), function(key, value) {
        // console.log("value", value)
        data.push(value.mobile_no)
        console.log("nnn", data)
    });
    frappe.call({
        method: 'custom_app.api.check_selected_no',
        args:{
            data: {"numbers": data},
        }
    })
}


frappe.ui.get_list('Whatsapp Number Check', {
    refresh: function (listView) {
        // Add a custom button
        listView.page.add_menu_item(__('Custom Button'), function () {
            frappe.msgprint('Custom Button clicked');
            // You can perform your custom action here
        });
    }
});
