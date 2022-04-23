# DOXAEL READ ME FILE FOR BACKEND
Read me file for the backend routes for the doxael app

## ROUTES
- /test: GET
    - Params:
        - None
    - Return:
        - type: JSON
        - keys: message,success
        - sample: {"message": f"Api for DOXAEL APP is Alive", "status": "success"})


- /create_admin: POST
    - Params:
        - email
        - password
    - Return:
        - type: JSON
        - keys: username,password,email,push_notification_token,status_message,status,status_code
        - sample: 
            - success: {"id":id,"username":username,"password":Password,"email":email,"push_notification_token":push_notification_token,"status_message":Admin Account Created","status":"success","status_code":200}
            - failed: {"status_message":f"Account Already Exists with email admin_mail@doxael.com}","status":"failed","status_code":200}


- /admin_login: POST
    - Params:
        - email
        - password
    - Return:
        - type: JSON
        - keys: admin_id,username,email,push_notification_token,status_message,status,status_code
        - sample:
            - success: {"admin_id":admin_id,"user_name":admin_name,"email":admin_email,"push_notification_token":push_notification_token,"status_message":"Admin Logged In","status":"success","status_code":200}
            - failed: {"status_message":"Invalid Password","status":"failed","status_code":400}


- /all_vendors: POST
    - Params:
        - admin_id
        - filter:
            - options: all,active,inactive
    - Return:
        - type: JSON
        - keys: vendors,status_message,status,status_code
        - sample:
            - success: {"vendors":[{"vendor_id":vendor_id,"vendor_name":vendor_name,"vendor_email":vendor_email,"vendor_push_notification_token":vendor_push_notification_token, "vendor_permitted":permitted}],"status_message":"Vendors Fetched","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Fetch Vendors","status":"failed","status_code":400}


- /single_vendor: POST
    - Params:
        - vendor_id
    - Return:
        - type: JSON
        - keys: vendor,status_message,status,status_code
        - sample:
            - success: {"vendor":[{"vendor_id":vendor_id,"vendor_name":vendor_name,"vendor_email":vendor_email,"vendor_push_notification_token":vendor_push_notification_token,"vendor_permitted":permitted}],"status_message":"Vendor Fetched","status":"success","status_code":200}
            - failed: {"status_message":"Vendor Not Found","status":"failed","status_code":400}


- /enable_vendors: POST
    - Params:
        - admin_id
        - vendor_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Vendor Activated","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Toggle Enable Vendor","status":"failed","status_code":400}


- /disable_vendors: POST
    - Params:
        - admin_id
        - vendor_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Vendor Deactivated","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Toggle Enable Vendor","status":"failed","status_code":400}


- /all_products: GET
    - Params:
        - None
    - Return
        - type: JSON
        - keys: product_data,status_message,status,status_code
        - sample:
            - success: {"product_data":[{"product_id":product_id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":image_URL,"product_discount":product_discount,"product_is_available":product_is_available,"product_owner":product_owner}],"status_message":"All Products Fetched","status":"success","status_code":200}
            - failed: {"status_message":"No Products Found","status":"failed","status_code":400}