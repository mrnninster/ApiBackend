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


- /admin_enable_vendors: POST
    - Params:
        - admin_id
        - vendor_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Vendor Activated","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Toggle Enable Vendor","status":"failed","status_code":400}


- /admin_disable_vendors: POST
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


- /all_admin_products: POST
    - Params:
        - admin_id
    - Returns:
        - type: JSON
        - keys: product_data,status_message,status,status_code
        - sample:
            - success: {"product_data":[{"product_id":product_id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":image_URL,"product_discount":product_discount,"product_is_available":product_is_available,"product_owner":product_owner}],"status_message":"All Products Fetched","status":"success","status_code":200}
            - failed: {"status_message":"No Products Found","status":"failed","status_code":400}


- /all_vendor_products: POST
    - Params:
        - vendor_id
    - Returns:
        - type: JSON
        - keys: product_data,status_message,status,status_code
        - sample:
            - success: {"product_data":[{"product_id":product_id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":image_URL,"product_discount":product_discount,"product_is_available":product_is_available,"product_owner":product_owner}],"status_message":"All Products Fetched","status":"success","status_code":200}
            - failed: {"status_message":"No Products Found","status":"failed","status_code":400}


- /single_product: GET
    - Params:
        - product_id
    - Return
        - type: JSON
        - keys: product_id,product_name,product_description,product_price,product_image,product_discount,product_is_available,status_message,status,status_code
        - sample:
            - success: {"product_id":product_id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":product_Img_URL,"product_discount":product_discount,"product_is_available":product_is_available,"status_message":"Product Fetched","status":"success","status_code":200}
        - failed: {"status_message":"Product Not Found","status":"failed","status_code":400}


- /add_product: POST:
    - Params:
        - owner_id(value is admin_id)
        - product_name
        - product_description
        - product_price
        - product_image
        - product_discount
    - Return:
        - type: JSON
        - keys: product_id,product_name,product_description,product_price,product_image,product_discount,product_is_available,status_message,status,status_code
        - sample:
            - success: {"product_id":product_id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":product_Img_URL,"product_discount":product_discount,"product_is_available":product_is_available,"status_message":"Product Fetched","status":"success","status_code":200}
        - failed: {"status_message":"Failed To Add New Product","status":"failed","status_code":400}


- /admin_edit_product: POST
    - Params:
        - admin_id
        - product_id
        - product_name(optional)
        - product_description(optional)
        - product_price(optional)
        - product_image(optional)
        - product_discount(optional)
        - product_is_available(optional)
    - Return:
        - type: JSON
        - keys: product_id,product_name,product_description,product_price,product_image,product_discount,product_is_available,status_message,status,status_code
        - sample:
            - success: {"product_id":product_id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":product_Img_URL,"product_discount":product_discount,"product_is_available":product_is_available,"status_message":"Product Fetched","status":"success","status_code":200}
        - failed: {"status_message":"Failed to Edit Product","status":"failed","status_code":400}


- /admin_make_featured_product: POST
    - Params:
        - admin_id
        - product_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Product Made Featured","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Make Product Featured","status":"failed","status_code":400}


- /admin_remove_featured_product: POST
    - Params: 
        - admin_id
        - product_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Product Made Non Featured","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Make Product Featured","status":"failed","status_code":400}


- /admin_remove_product: POST
    - Params:
        - admin_id
        - product_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Product Removed","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Remove Product","status":"failed","status_code":400}


- /all_customers: POST
    - Params:
        - admin_id
        - filter
            - options: all,active,inactive
    - Return:
        - type: JSON
        - keys: customers,status_message,status,status_code
        - sample:
            - success: {"customers": [{"customer_id":customer_id,"customer_name":customer_name,"customer_email":customer_email,"customer_address":customer_address,"customer_push_notification_token":customer_push_notification_token, "customer_permitted":permitted}],"status_message":"Customers Fetched","status":"success","status_code":200}
            - failed: {"status_message":"Failed to Fetch Customers","status":"failed","status_code":400}


- /admin_enable_customers: POST
    - Params:
        - admin_id
        - customer_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Customer Activated","status":"success","status_code":200}
            - failed: {"message":"Failed to Toggle Enable Customer","status":"failed","status_code":400}


- /admin_disable_customers: POST
    - Params:
        - admin_id
        - customer_id
    - Return:
        - type: JSON
        - keys: status_message,status,status_code
        - sample:
            - success: {"status_message":"Customer Deactivated","status":"success","status_code":200}
            - failed: {"message":"Failed to Toggle Enable Customer","status":"failed","status_code":400}