import json
import time

import paypalrestsdk
from decouple import config


class PaypalPayment:
    apps_credential = [
        {'client_id': 'ARzu5O9MZfzkPQ5xWFKmdJfqEJvEzcnQfrKxCVPprNUoh_COX3i0VeaKHTcvg6DN8xHy25-1Zq4zXgwc',
         'client_secret': 'EG7L2EeXHv6EYZOtUIVSUfShGjWU1--UatgaJFxiLKJSugGJVx2ErJQbZwKB0sO_Cx6dYZHdyVWh1nBn',
         'merchan_email': 'linseluna-pam@yahoo.com'
        },
        {'client_id': 'EC5wQq7IXXs7_LzeivqIZhZvWtnfKlB2kwaXhveOxCslLG5EZOvBKauhjkxEYs8im2Kk61UDk4kimCok',
         'client_secret': 'EC5wQq7IXXs7_LzeivqIZhZvWtnfKlB2kwaXhveOxCslLG5EZOvBKauhjkxEYs8im2Kk61UDk4kimCok',
         'merchan_email': 'yekahi1329@royalka.com'
        },
        {'client_id': 'AfF3SSQ_b-qnPnDi4YBUXKvjVqLi5LJRZ5_thKaECh4A2gj72Uhoen7dgfXDqjhtJJMhOWdNq4PqJ9yu',
         'client_secret': 'EKhL-a26g2_QuXxC1bINaZ3jO50J_A06PyHMkARsAGjZHv_73M1WZVYxIqmWaHQ9virnCjtr6BRyIILo',
         'merchan_email': 'rohobed391@tipent.com'
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
                
            time.sleep(5)
            self.i = self.i + 1
            if len(self.apps_credential)== self.i:
                self.i = 0
            if send:
                return True
            else:
                return missing_mail
        else:
            return missing_mail