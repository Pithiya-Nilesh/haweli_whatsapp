import frappe
import requests
import json

@frappe.whitelist()
def check_number():
    # doc = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "send": 0}, fields=["name", 'mobile_no'])
    data = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "sent": 0, "data": ""}, fields=["name", "mobile_no"], limit=40000)

    for i in data:
        url = "https://api.ultramsg.com/instance67403/contacts/check"

        querystring = {
            "token": "0srgh10epscrt41b",
            "chatId": i.mobile_no,
            "nocache": ""
        }

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)

        if "status" in data and data["status"] == "valid":
            doc = frappe.get_doc("Whatsapp Number Check", i.name)
            doc.is_valid_whatsapp_no = 1
            doc.data = json.dumps(data, indent=4)
            doc.sent = 1
            doc.save(ignore_permissions=True)
            frappe.db.commit()

        else:
            doc = frappe.get_doc("Whatsapp Number Check", i.name)
            doc.data = json.dumps(data, indent=4)
            doc.save(ignore_permissions=True)
            doc.sent = 1
            frappe.db.commit()


@frappe.whitelist()
def send_all_number_pdf():
    filename = "પુષ્ટિસંસ્કારધામ શિલાન્યાસ મહોત્સવ ફેઝ-૨ આમંત્રણ.pdf"
    document_link = "https://pushtisanskar.frappe.cloud/files/પુષ્ટિસંસ્કારધામ શિલાન્યાસ મહોત્સવ ફેઝ-૨ આમંત્રણ.pdf"
    caption = "પુષ્ટિસંસ્કારધામ સપ્તદિવસીય ફેઝ -2 શિલાન્યાસ મહોત્સવ તારીખ 14 થી 20 ડિસેમ્બર 2023 માં આપ સર્વેને ઉપસ્થિત રહેવા ભાવ ભર્યું આમંત્રણ. \n*સ્થાન :- પુષ્ટિસંસ્કારધામ નિર્માણ સ્થાન, વડાલ-કાથરોટા રોડ, વડાલ-જુનાગઢ.*"


    url = "https://api.ultramsg.com/instance67403/messages/document"
    user_details = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 1}, fields=["name", "mobile_no"], limit=40000)
    # return user_details
    for data in user_details:

        l = frappe.db.get_value("Whatsapp Message Log", filters={"number": data['mobile_no'], "type": "Document"}, fieldname=["name"])
        if l:
            print("pass")

        else:
            payload = f"token=0srgh10epscrt41b&to={data['mobile_no']}&filename={filename}&document={document_link}&caption={caption}"
            payload = payload.encode('utf8').decode('iso-8859-1')
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("POST", url, data=payload, headers=headers)

            print(response.text)
            res = json.loads(response.text)
            if "sent" in res and res["sent"]:
                status = "Success"
            else:
                status = "Failed"
            set_whatsapp_log(response.text, status, data['mobile_no'], "Document", link=document_link, caption=caption)

@frappe.whitelist()
def send_all_number_video():
    pass
    # video_link = "https://pushtisanskar.frappe.cloud/files/Pushtisanskardham Invitation Video.mp4"
    # caption = "પુષ્ટિસંસ્કાર સ્કૂલના બાળકો દ્વારા પુષ્ટિસંસ્કારધામ સપ્તદિવસીય ફેઝ -2 શિલાન્યાસ મહોત્સવ તારીખ 14 થી 20 ડિસેમ્બર 2023 માં આપ સર્વેને ઉપસ્થિત રહેવા ભાવ ભર્યું આમંત્રણ. \n*સ્થાન :- પુષ્ટિસંસ્કારધામ નિર્માણ  સ્થાન, વડાલ-કાથરોટા રોડ, વડાલ જુનાગઢ.* *Youtube :* https://youtu.be/Wada0NU6RPk"


    # url = "https://api.ultramsg.com/instance67403/messages/video"
    # user_details = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 1}, fields=["name", "mobile_no"], limit=40000)
    # # return user_details
    # for data in user_details:
    #     payload = f"token=0srgh10epscrt41b&to={data['mobile_no']}&video={video_link}&caption={caption}"
        
    #     payload = payload.encode('utf8').decode('iso-8859-1')
    #     headers = {'content-type': 'application/x-www-form-urlencoded'}

    #     response = requests.request("POST", url, data=payload, headers=headers)

    #     print(response.text)

    #     res = json.loads(response.text)
    #     if "sent" in res and res["sent"]:
    #         status = "Success"
    #     else:
    #         status = "Failed"
    #     set_whatsapp_log(response.text, status, data['mobile_no'], "Video", link=video_link, caption=caption)












def get_ultra_settings():
    return frappe.get_cached_doc("Ultramsg Whatsapp Settings")


@frappe.whitelist(allow_guest=True)
def check_selected_no(data):

    data = json.loads(data)
    # print("\n\n data ", data)
    # print("\n\n type data ", type(data))
    
    ultra_settings = get_ultra_settings()
    if ultra_settings.enable == 0:
        return frappe.msgprint("Please Enable Whatsapp API in Ultramsg Whatsapp Settings to Check Numbers")
    
    url = f"https://api.ultramsg.com/{ultra_settings.instance_id}/contacts/check"
    token = frappe.utils.password.get_decrypted_password("Ultramsg Whatsapp Settings", "Ultramsg Whatsapp Settings", fieldname="token")
    
    for i in data["numbers"]:

        querystring = {
            "token": token,
            "chatId": i,
            "nocache": ""
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
       
        response = requests.request("GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)

        if "status" in data and data["status"] == "valid":
            doc = frappe.get_doc("Whatsapp Number Check", i)
            doc.is_valid_whatsapp_no = 1
            doc.data = json.dumps(data, indent=4)
            doc.sent = 1
            doc.save(ignore_permissions=True)
            frappe.db.commit()

        else:
            doc = frappe.get_doc("Whatsapp Number Check", i)
            doc.data = json.dumps(data, indent=4)
            doc.save(ignore_permissions=True)
            frappe.db.commit()


@frappe.whitelist()
def send_whatsapp_message(data, details):
    user_details = json.loads(data)
    c_details = json.loads(details)

    # check whatsapp config
    ultra_settings = get_ultra_settings()
    if ultra_settings.enable == 0:
        return frappe.msgprint("Please Enable Whatsapp API in Ultramsg Whatsapp Settings to Send Messages")
    
    if c_details["type"] == "Video":
        send_video(user_details, c_details)

    elif c_details["type"] == "Document":
        send_document(user_details, c_details)

    elif c_details["type"] == "Image":
        send_image(user_details, c_details)

    elif c_details["type"] == "Message":
        send_message(user_details, c_details)

# @frappe.whitelist()
def send_video(data, video_details):
    user_details = data

    video_link = video_details['video_link']
    if video_link.startswith("/files"):
        from frappe.utils import get_url
        video_link = get_url() + video_link
    else:
       video_link = video_link
    
    caption = ""
    if "caption" in video_details:
        caption = video_details["caption"]

    ultra_settings = get_ultra_settings()
    token = frappe.utils.password.get_decrypted_password("Ultramsg Whatsapp Settings", "Ultramsg Whatsapp Settings", fieldname="token")

    url = f"https://api.ultramsg.com/{ultra_settings.instance_id}/messages/video"
    for data in user_details:
        # https://file-example.s3-accelerate.amazonaws.com/video/test.mp4
        payload = f"token={token}&to={data['mobile_no']}&video={video_link}&caption={caption}"
        
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)

        res = json.loads(response.text)
        if "sent" in res and res["sent"]:
            status = "Success"
        else:
            status = "Failed"
        set_whatsapp_log(response.text, status, data['mobile_no'], "Video", link=video_link, caption=caption)


def send_document(data, document_details):
    user_details = data

    document_link = document_details['document_link']
    if document_link.startswith("/files"):
        from frappe.utils import get_url
        document_link = get_url() + document_link
    else:
       document_link = document_link
    
    caption = ""
    if "caption" in document_details:
        caption = document_details["caption"]
    
    from urllib.parse import urlparse
    parsed_url = urlparse(document_link)

    ultra_settings = get_ultra_settings()
    token = frappe.utils.password.get_decrypted_password("Ultramsg Whatsapp Settings", "Ultramsg Whatsapp Settings", fieldname="token")

    url = f"https://api.ultramsg.com/{ultra_settings.instance_id}/messages/document"

    # Get the filename from the path component of the URL
    filename = parsed_url.path.split('/')[-1]

    for data in user_details:
        payload = f"token={token}&to={data['mobile_no']}&filename={filename}&document={document_link}&caption={caption}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        res = json.loads(response.text)
        if "sent" in res and res["sent"]:
            status = "Success"
        else:
            status = "Failed"
        set_whatsapp_log(response.text, status, data['mobile_no'], "Document", link=document_link, caption=caption)


def send_image(data, image_details):
    user_details = data

    image_link = image_details['image_link']
    if image_link.startswith("/files"):
        from frappe.utils import get_url
        image_link = get_url() + image_link
    else:
       image_link = image_link
    
    caption = ""
    if "caption" in image_details:
        caption = image_details["caption"]

    ultra_settings = get_ultra_settings()
    token = frappe.utils.password.get_decrypted_password("Ultramsg Whatsapp Settings", "Ultramsg Whatsapp Settings", fieldname="token")


    url = f"https://api.ultramsg.com/{ultra_settings.instance_id}/messages/image"
    for data in user_details:
        payload = f"token={token}&to={data['mobile_no']}&image={image_link}&caption={caption}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        res = json.loads(response.text)
        if "sent" in res and res["sent"]:
            status = "Success"
        else:
            status = "Failed"
        set_whatsapp_log(response.text, status, data['mobile_no'], "Image", link=image_link, caption=caption)


# @frappe.whitelist()
def send_message(data, message_details):
    user_details = data

    ultra_settings = get_ultra_settings()
    
    url = f"https://api.ultramsg.com/{ultra_settings.instance_id}/messages/chat"
    token = frappe.utils.password.get_decrypted_password("Ultramsg Whatsapp Settings", "Ultramsg Whatsapp Settings", fieldname="token")

    for data in user_details:
        payload = f"token={token}&to={data['mobile_no']}&body={message_details['message']}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        res = json.loads(response.text)
        if "sent" in res and res["sent"]:
            status = "Success"
        else:
            status = "Failed"
        set_whatsapp_log(response.text, status, data['mobile_no'], "Message", message=message_details['message'])


def set_whatsapp_log(response_data, status, number, c_type, link="", caption="", message=""):
    data = json.loads(response_data)
    log = frappe.new_doc("Whatsapp Message Log")
    log.data = json.dumps(data, indent=4)
    log.status = status
    log.number = number
    log.type = c_type
    log.link = link
    log.caption = caption
    log.message = message
    log.insert()
    frappe.db.commit()

############################# above code is for ultra messages ####################################

############################# below code is for wati ##############################################

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

    details = frappe.db.get_list("Wati Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "send": 0}, fields=["name", "mobile_no", "first_name", "last_name"], limit=100)

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

    wmdw = frappe.new_doc("Wati Message Delivered Webhook")
    wmdw.whatsapp_id = response["whatsappMessageId"]
    wmdw.data = frappe.as_json(response, 4)
    wmdw.insert(ignore_permissions=True)
    frappe.db.commit()


# @frappe.whitelist(allow_guest=True)
# def replied_on_template_message():
#     response = frappe.form_dict
#     return response



# @frappe.whitelist()
# def a():
#     # print("\n\n frappe.get_meta", frappe.get_meta('User'))
#     # return frappe.get_meta('User')

#     data = frappe.db.get_list("DocType")
#     for i in data:
#         # return i
#         # return frappe.get_meta(i["name"])
#         # print("\n\n frappe.get_meta", frappe.get_meta(i["name"]))
#         print("\n\n frappe.get_meta", frappe.get_meta(i["name"]).fields)


@frappe.whitelist()
def check_number_second():
    # doc = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "send": 0}, fields=["name", 'mobile_no'])
    data1 = frappe.db.get_list("Whatsapp Number Check", filters={"is_valid_whatsapp_no": 0, "sent": 0, "data": ""}, fields=["name", "mobile_no"], limit=40000)
    
    data = list(reversed(data1))

    for i in data:
        url = "https://api.ultramsg.com/instance67403/contacts/check"

        querystring = {
            "token": "0srgh10epscrt41b",
            "chatId": i.mobile_no,
            "nocache": ""
        }

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)

        if "status" in data and data["status"] == "valid":
            doc = frappe.get_doc("Whatsapp Number Check", i.name)
            doc.is_valid_whatsapp_no = 1
            doc.data = json.dumps(data, indent=4)
            doc.sent = 1
            doc.save(ignore_permissions=True)
            frappe.db.commit()

        else:
            doc = frappe.get_doc("Whatsapp Number Check", i.name)
            doc.data = json.dumps(data, indent=4)
            doc.save(ignore_permissions=True)
            doc.sent = 1
            frappe.db.commit()