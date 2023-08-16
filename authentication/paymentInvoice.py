import json
import time

import paypalrestsdk
from decouple import config


class PaypalPayment:
    apps_credential = [
        {'client_id': 'AVTVIIRzjYmNIyh7Ku_7UpaVg6Qv0iL3R8sM2qihoDDj0A8xuXRX1pxmbVnFsdaHc2eDSHn6Zyo6HVpC',
         'client_secret': 'EPl7QpoTkuUJAWAsYXmzEvmAu2VCQqne29Kw2THCtFgmozwb6Quvyl2mtUhIs3o7E_wX-RmhknHWm7zf',
         'merchan_email': 'barron12260-PatriciaAnderton@yahoo.com'
        },
        {'client_id': 'Aa-lw8CJf-SVrUF4WZE3XM-ZD2O5GJjnm__BMmnG3ChKIPRXO4VFUTePzZYzBQmEI-Xerv6oISXDD51O',
         'client_secret': 'EL_cJLslqwN29xRNVvCVSbVAtSW3o29nWKtOi8yKPxgr3E37yDTwGwvJOXwRqatm8hu7dJPZ5qupo8x9',
         'merchan_email': 'gacasis515@v1zw.com'
        }
    ]
    # CLIENT_ID = config('PAYPAL_CLIENT_ID')
    # CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')
    

    i = 0

    def emailSet(self, list):
        email_dict_list = []
        for email in list:
            email_dict = {"email": email}
            email_dict_list.append(email_dict)

        return email_dict_list

    def getInvoice(self, client_mail, cc_mail, item_name, amount, note, address, city, state, postal_code):
        CLIENT_ID = self.apps_credential[self.i]['client_id']
        CLIENT_SECRET = self.apps_credential[self.i]['client_secret']
        MERCHAN_EMAIL = self.apps_credential[self.i]['merchan_email']
        paypalrestsdk.configure({
        "mode": "live", 
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
        })
        cc = []
        
        if len(cc_mail) > 0:
            cc = self.emailSet(cc_mail)

        invoice = paypalrestsdk.Invoice({
        "merchant_info": {
            "email": MERCHAN_EMAIL,
            "first_name": "Paypal",
            "last_name": "Merchant"
        },
        "billing_info": [{
            "email": client_mail
        }],
        "cc_info": cc,
        "subject": "Your Custom Subject Here",
        "items": [{
            "name": item_name,
            "quantity": 1,
            "unit_price": {
                "currency": "USD",
                "value": int(amount)
            }
        }],
        "note": note,
        "payment_term": {
            "term_type": "NET_30"
        },
        "shipping_info": {
                "first_name": "Paypal",
                "last_name": "User",
                "business_name": "Paypal User",
                "phone": {
                    "country_code": "+880",
                    "national_number": "1963510362"
                },
                "address": {
                    "line1": address,
                    "city": city,
                    "state": state,
                    "postal_code": postal_code,
                    "country_code": "US"
                }
            }
        })
        create_invoice = invoice.create()
        print(create_invoice)
        print(self.i, "value of i ")
        print(CLIENT_ID, "Client Id")
        print(CLIENT_SECRET, "Client Secret")
        print(MERCHAN_EMAIL, "Client Marchat Email")
        details = paypalrestsdk.Invoice.find(invoice.id)
        missing_mail = details['billing_info'][0]['email']
        if create_invoice:
            send = False
            try:
                send = invoice.send()
            except Exception as e:
                print(e, "Error is ->")
                time.sleep(5)
                
            time.sleep(10)
            self.i = self.i + 1
            if len(self.apps_credential)== self.i:
                self.i = 0
            if send:
                return True
            else:
                return missing_mail
        else:
            return missing_mail