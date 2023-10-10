import frappe
import requests
import json

@frappe.whitelist()
def check_number():
    doc = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "send": 0}, fields=["name", 'mobile_no'])

    for i in doc:
        url = "https://api.ultramsg.com/instance63753/contacts/check"

        querystring = {
            "token": "rs85zam9idaor3c7",
            "chatId": i.mobile_no,
            "nocache": ""
        }

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)
        # print("\n\n data", data)
        if data['status'] == 'valid':
            doc = frappe.get_doc("Whatsapp Number Check", i.name)
            doc.is_valid_whatsapp_no = 1
            doc.save()
            frappe.db.commit()
        else:
            pass



@frappe.whitelist()
def wati_check_number():
    access_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlOTNjMTE5ZC00ZGJmLTQ2NDgtYTg5OC1jYWE3NDZhMDhkNzgiLCJ1bmlxdWVfbmFtZSI6ImhlbGxva2lyaXRAZ21haWwuY29tIiwibmFtZWlkIjoiaGVsbG9raXJpdEBnbWFpbC5jb20iLCJlbWFpbCI6ImhlbGxva2lyaXRAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMTAvMDkvMjAyMyAwNTo0Mjo0OSIsImRiX25hbWUiOiIxMDAxMTUiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.fSrnCZ3CkkDiO9ofSmdNG1enepj8f2g2hv6JMul9b6c'
    headers = {
        "Content-Type": "text/json",
        "Authorization": access_token
    }

    payload = {
                "broadcast_name": "shilanyas_invitation_new",
                "template_name": "shilanyas_invitation_new",
                "parameters": []
            }

    details = frappe.db.get_list("Wati Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "send": 0}, fields=["name", "mobile_no", "first_name", "last_name"])

    for number in details:
        
        # print("\n\n details", number["mobile_no"])
        url = f'https://live-server-100115.wati.io/api/v1/sendTemplateMessage?whatsappNumber={number["mobile_no"]}'
        # url = f'https://live-server-100115.wati.io/api/v1/sendTemplateMessage?whatsappNumber=917990915950'

        print("\n\n url", url)
        response = requests.post(url, json=payload, headers=headers)
        data = json.loads(response.text)

        print("\n\n response", response)
        print("\n\n data", data)
        if "result" in data and data["result"]:
            send = frappe.get_doc("Wati Whatsapp Number Check", number["name"])
            send.send = 1
            send.save()
            frappe.db.commit()

            log = frappe.new_doc("wati whatsapp check send message log")
            log.firstname = number["first_name"]
            log.lastname = number["last_name"]
            log.mobile_no = number["mobile_no"]
            log.send = 1
            log.data = json.dumps(data, indent=4)
            log.insert()
            frappe.db.commit()

        else:
            log = frappe.new_doc("wati whatsapp check send message log")
            log.firstname = number["first_name"]
            log.lastname = number["last_name"]
            log.mobile_no = number["mobile_no"]
            log.send = 0
            log.data = json.dumps(data, indent=4)
            log.insert()
            frappe.db.commit()

        # if "validWhatsAppNumber" in data and data["validWhatsAppNumber"] == True:
        #     doc = frappe.get_doc("Wati Whatsapp Number Check", number["name"])
        #     doc.is_valid_whatsapp_no = 1
        #     doc.save()
        #     frappe.db.commit()

        # else:
            # print("\n\n no")


@frappe.whitelist(allow_guest=True)
def sent_template_message_webhook():
    # when template message is send we store reponse id and other for get id
    response = frappe.form_dict
    wtsw = frappe.new_doc("Wati Template Sent Webhook")
    wtsw.mobile_no = response["waId"]
    wtsw.whatsapp_id = response["whatsappMessageId"]
    wtsw.template_name = response["templateName"]
    wtsw.data = frappe.as_json(response, 4)
    wtsw.insert(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist(allow_guest=True)
def delivered_template_message_webhook():
    # when template message is delivered we get reponse id and match with sent template message id if match get doctype and set value 1 in is_valid_whatsapp_no
    response = frappe.form_dict
    doc = frappe.db.get_value("Wati Template Sent Webhook", filters={"whatsapp_id": f'{response["whatsappMessageId"]}'}, fieldname=["mobile_no", "whatsapp_id", "template_name"], as_dict=True)
    if doc and doc.whatsapp_id == response["whatsappMessageId"]:
        wwnc = frappe.db.get_value("Wati Whatsapp Number Check", filters={"mobile_no": doc.mobile_no}, fieldname=["name"], as_dict=True)
        set_yes = frappe.get_doc("Wati Whatsapp Number Check", wwnc)
        set_yes.is_valid_whatsapp_no = 1
        set_yes.save(ignore_permissions=True)
        frappe.db.commit()


# @frappe.whitelist(allow_guest=True)
# def replied_on_template_message():
#     response = frappe.form_dict
#     return response