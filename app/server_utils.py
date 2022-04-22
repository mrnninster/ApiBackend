###########################################################
#####                                                ######
#####       SERVER UTILS CALLBACK DATA SECTION       ######
#####                                                ######
###########################################################

import os
import secrets
import logging

from io import BytesIO
from PIL import Image
from app.db_model import db, Admin, Product, Vendor, Customer
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log File Logging Format
formatter = logging.Formatter("%(asctime)s:%(levelname)s::%(message)s")

# Log File Handler
Log_File_Handler = logging.FileHandler("doxael_server_utils.log")
Log_File_Handler.setLevel(logging.DEBUG)
Log_File_Handler.setFormatter(formatter)

# Stream Handlers
Stream_Handler = logging.StreamHandler()

# Adding The Handlers
logger.addHandler(Log_File_Handler)
logger.addHandler(Stream_Handler)

# Log On START 
logger.debug("")
logger.debug("="*100)
logger.info("Server Utils Section :: Logging Active")
logger.debug("")


def genID(N=16):
    """ 
    Randomly generates a N character long
    alphanumeric

    Params
    ------
    N: Length of ID to be generated

    Returns
    -------
    Type: String
    """
    gen_id = secrets.token_hex(N)
    return gen_id


def genUniqueID(table):
    """
    Randomly generates a Unique 16 character
    long alphanumeric by checking the table 
    to ensure uniqueness

    Params
    ------
    table: Database table against which the 
            uniqueness of the generated ID 
            is checked. 

    Returns
    -------
    Type: String
    """
    # Generated ID
    newID = genID()

    # Check IDs uniqueness
    if table == Admin:
        checkID = Admin.query.filter_by(admin_id = newID).all()

    if table == Customer:
        checkID = Customer.query.filter_by(customer_id = newID).all()

    if table == Vendor:
        checkID = Vendor.query.filter_by(vendor_id = newID).all()

    if table == Product:
        checkID = Product.query.filter_by(product_id = newID).all()

    if len(checkID) > 0:
        genUniqueID(table)
    else:
        return newID


def genToken(N=32):
    """
    Randomly generates a N character long url
    safe token

    Params
    ------
    N: Length of generated token

    Returns
    -------
    Type: String
    """
    gen_token = secrets.token_urlsafe(N)
    return gen_token


def genUniqueToken(table):
    """
    Randomly generates a Unique 32 character
    long url safe token by checking the table 
    to ensure uniqueness

    Params
    ------
    table: Database table against which the 
            uniqueness of the generated ID 
            is checked.

    Returns
    -------
    Type: String
    """
    # Generated ID
    newToken = genToken()

    # Check IDs uniqueness
    if table == Admin:
        checkToken = Admin.query.filter_by(admin_push_notification_token = newToken).all()

    if table == Customer:
        checkToken = Customer.query.filter_by(customer_push_notification_token = newToken).all()

    if table == Vendor:
        checkToken = Vendor.query.filter_by(vendor_push_notification_token = newToken).all()

    if len(checkToken) > 0:
        genUniqueToken(table)
    else:
        return newToken


def Create_Account(account_type,**kwargs):
    """ 
    Creates the defaul admin user if one dosent exit

    Params
    ------
    account_type: The type of account
            user is creating
    kwargs: Keyword arguments for
            email -> "email"
            password -> "password"
            username -> "username"

    Returns
    -------
    Type: Dict
    keys: username,password
    status_message: the result of the api query
    status: Login status
            options: success,failed
    status_code: request status code
    """

    # Check Account Exists
    if account_type == "admin":

        # Check if admin exists
        Account = Admin.query.filter_by(admin_email=kwargs["email"]).first()

    elif account_type == "vendor":

        # Check if vendor exists
        Account = Vendor.query.filter_by(vendor_email=kwargs["email"]).first()

    elif account_type == "customer":

        # Check if customer exists
        Account = Customer.query.filter_by(customer_email=kwargs["email"]).first()

    # if Account Does Not Exist
    if Account is None:
        
        # Params
        username = kwargs["username"] if kwargs["username"] is not None else None
        email = kwargs["email"]
        Password = kwargs["password"]
        hashedPassword = generate_password_hash(Password)


        # Create admin account
        if account_type == "admin":

            id = genUniqueID(Admin)
            push_notification_token = genUniqueToken(Admin)

            admin_user = Admin(admin_id=id, admin_name=username, admin_email=email, password=hashedPassword, admin_push_notification_token=push_notification_token)
            db.session.add(admin_user)
            db.session.commit()

        # Create vendor account
        elif account_type == "vendor":

            id = genUniqueID(Vendor)
            push_notification_token = genUniqueToken(Vendor)

            vendor_user = Vendor(vendor_id=id, vendor_name=username, vendor_email=email, password=hashedPassword, vendor_push_notification_token=push_notification_token)
            db.session.add(vendor_user)
            db.session.commit()

        # Create customer account
        elif account_type == "customer":

            id = genUniqueID(Customer)
            push_notification_token = genUniqueToken(Customer)

            customer_user = Customer(customer_id=id, customer_name=username, customer_email=email, password=hashedPassword, customer_push_notification_token=push_notification_token)
            db.session.add(customer_user)
            db.session.commit()

        # Response
        return {"id":id,"username":username,"password":Password,"email":email,"push_notification_token":push_notification_token,"status_message":f"{account_type.capitalize()} Account Created","status":"success","status_code":200}
    
    # If Account Exists
    else:
        return {"status_message":f"Account Already Exists with email {kwargs['email']}","status":"success","status_code":200}


def Account_Login(account_type,email,password):
    """
    Function validates that account exist and
    logs user in

    Params
    ------
    email: Account Email
    password: Account Password
    account_type: The type of account
            user is logging into

    Returns
    -------
    id: account ID
    username: account password
    email: account email
    push_notification_token: account 
            associated push notification token
    status_message: the result of the api query
    status: Login status
            options: success,failed
    status_code: request status code
    """

    # For Admin
    if(account_type == "admin"):
        Account = Admin.query.filter_by(admin_email=email).first()

    # For Vendor
    elif(account_type == "vendor"):
        Account = Vendor.query.filter_by(vendor_email=email).first()

    # For Customer
    elif(account_type == "customer"):
        Account = Customer.query.filter_by(customer_email=email).first()

    
    # Check Account Exists
    if Account is not None:
        
        # Check For Permitted Vendor Accounts
        if (account_type == "vendor") and (Account.permitted == True):
            vendor_permitted = True
        else:
            return({"status_message":"Admin Has Not Permitted Account","status":"failed","status_code":401})


        # Checked Password
        hashedpassword = Account.password
        checkPassword = check_password_hash(hashedpassword,password)

        if checkPassword == True:
            # For Admin
            if(account_type == "admin"):
                return{"admin_id":Account.admin_id,"user_name":Account.admin_name,"email":Account.admin_email,"push_notification_token":Account.admin_push_notification_token,"status_message":"Admin Logged In","status":"success","status_code":200}

            # For Vendor
            elif(account_type == "vendor")and (vendor_permitted == True):
                return{"vendor_id":Account.vendor_id,"user_name":Account.vendor_name,"email":Account.vendor_email,"push_notification_token":Account.vendor_push_notification_token,"status_message":"Vendor Logged In","status":"success","status_code":200}

            # For Customer
            elif(account_type == "customer"):
                return{"customer_id":Account.customer_id,"user_name":Account.customer_name,"email":Account.customer_email,"push_notification_token":Account.customer_push_notification_token,"status_message":"Customer Logged In","status":"success","status_code":200}

        else:
            return{"status_message":"Invalid Password","status":"failed","status_code":400}

    else:
        return{"status_message":"account does not exist","status":"failed","status_code":400}
    

def Add_Product(account_id,product_name,product_description,product_price,product_image,product_image_name,product_discount):
    """
    This function adds a product to the database

    Params
    ------
    product_name: The name of the product
    product_description: The description of the product
    product_price: The price of the product
    product_image: The image of the product
    product_image_name: The name of the image
    product_discount: The discount of the product

    Returns
    -------
    product_id: The id of the product
    product_name: The name of the product
    product_description: The description of the product
    product_price: The price of the product
    product_image: The image of the product
    product_discount: The discount of the product
    product_is_available: The availability of the product
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
            
        # Get Image
        image = product_image.read()

        # Convert Image To Bytes
        image = BytesIO(image)

        # Convert Image To PIL Image
        image = Image.open(image)

        # Image Name
        image_name = f"{genID()}_{product_image_name}"

        # Image Destination
        image_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"static/images/products/{image_name}")

        # Product ID
        id = genUniqueID(Product)

        # Save Image
        image.save(image_destination)

        # Add Product
        product = Product(product_id=id,product_name=product_name,product_description=product_description,product_price=product_price,product_image_name=image_name,product_image_filepath=image_destination,product_discount=product_discount,product_owner=account_id,product_is_available=True)
        db.session.add(product)
        db.session.commit()

        # Response
        return {"product_id":id,"product_name":product_name,"product_description":product_description,"product_price":product_price,"product_image":f"localhost:5003/static/images/products/{image_name}","product_discount":product_discount,"product_is_available":True,"status_message":f"Product {product_name} Added","status":"success","status_code":200}

    except Exception as e:
        logger.debug(f"AddNewProductError: Failed to Add New Product,{e}")
        return{"status_message":"Failed to Add New Product","status":"failed","status_code":400}


def Get_Single_Product(product_id):
    """
    This function fetches data for a single product

    Params
    ------
    product_id: The id of the product being fetched

    Returns
    -------
    product_id: The id of the product
    product_name: The name of the product
    product_description: The description of the product
    product_price: The price of the product
    product_image: The image of the product
    product_discount: The discount of the product
    product_is_available: The availability of the product
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Fetch Product
        product = Product.query.filter_by(product_id=product_id).first()

        # Check Product Exists and Return Response
        if product is not None:
            return {"product_id":product.product_id,"product_name":product.product_name,"product_description":product.product_description,"product_price":product.product_price,"product_image":f"localhost:5003/static/images/products/{product.product_image_name}","product_discount":product.product_discount,"product_is_available":product.product_is_available,"status_message":"Product Fetched","status":"success","status_code":200}
        else:
            return{"status_message":"Product Not Found","status":"failed","status_code":400}

    # On Error Handler and Return Response
    except Exception as e:
        logger.debug(f"GetSingleProductError: Failed to Get Single Product,{e}")
        return{"status_message":"Failed to Get Single Product","status":"failed","status_code":400}


def Get_All_Products(account_type=None,account_id=None):
    """
    This function fetches product from the database,
    if account_type is admin, it fetches all admin products
    if account_type is vendor, it fetches all vendor products
    if account_type is None, it fetches all products

    Params
    ------
    account_type: The type of account used to fetch products
    account_id: The id of the account used to fetch products

    Returns
    -------
    product_id: The id of the product
    product_name: The name of the product
    product_description: The description of the product
    product_price: The price of the product
    product_image: The image of the product
    product_discount: The discount of the product
    product_is_available: The availability of the product
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Fetch All Products
        if (account_type == None and account_id == None):
            products = Product.query.all()

        # Fetch Admin Products
        elif(account_type == "admin"):
            products = Product.query.filter_by(product_owner=account_id).all()

        # Fetch Vendor Products
        elif(account_type == "vendor"):
            products = Product.query.filter_by(product_owner=account_id).all()

        # Check Products Exists and Return Response
        if products is not None:
            product_data = [{"product_id":product.product_id,"product_name":product.product_name,"product_description":product.product_description,"product_price":product.product_price,"product_image":f"localhost:5003/static/images/products/{product.product_image_name}","product_discount":product.product_discount,"product_is_available":product.product_is_available,"product_owner":product.product_owner} for product in products]
            return {"product_data":product_data,"status_message":"All Products Fetched","status":"success","status_code":200}
        else:
            return{"status_message":"No Products Found","status":"failed","status_code":400}

    # On Error Handler and Return Response
    except Exception as e:
        logger.debug(f"GetAllProductsError: Failed to Get All Products,{e}")
        return{"status_message":"Failed to Get All Products","status":"failed","status_code":400}


def Toggle_Enable_Vendor(action,admin_id,vendor_id):
    """ 
    This function enables admin to activate or deactivate a vendors account

    Params
    ------
    action: The action to be performed
            ation options: activate,deactivate
    admin_id: The id of the admin
    vendor_id: The id of the vendor

    Returns
    -------
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Fetch Admin
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        # Check Admin Exists
        if admin is not None: 

            # Fetch Vendor
            vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
            
            #  Activate Vendor
            if action == "activate":
                vendor.permitted = True
                vendor.permited_by = admin_id
                db.session.commit()
                return {"status_message":"Vendor Activated","status":"success","status_code":200}

            # Deactivate Vendor
            elif action == "deactivate":
                vendor.permitted = False
                vendor.permited_by = admin_id
                db.session.commit()
                return {"status_message":"Vendor Deactivated","status":"success","status_code":200}

            # On Invalid Action
            else:
                return{"status_message":"Invalid Action","status":"failed","status_code":400}

        # On Invalid Admin
        else:
            return{"status_message":"Invalid Admin","status":"failed","status_code":400}

    # On Error Handler and Return Response
    except Exception as e:
        logger.debug(f"ToggleEnableVendorError: Failed to Toggle Enable Vendor,{e}")
        return{"message":"Failed to Toggle Enable Vendor","status":"failed","status_code":400}


def Remove_Product(account_type,account_id,product_id):
    """
    This function is used to remove products from the database

    Params
    ------
    account_type: The type of account used to remove products
                    account_type options: admin,vendor
    account_id: The id of the account used to remove products
    product_id: The id of the product to be removed

    Returns
    -------
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # For Admin
        if account_type == "admin":
            
            # Verify Account Is Admin
            admin = Admin.query.filter_by(admin_id=account_id).first()
            
            # Verify Admin Exists
            if admin is not None:

                # Admin Remove Product
                product = Product.query.filter_by(product_id=product_id).first()

        # For Vendor
        elif account_type == "vendor":

            # Fetch Vendor Product
            product = Product.query.filter_by(product_id=product_id,product_owner=account_id).first()

        # Verify Product Exists
        if product is not None:

            # Remove Product Image
            os.remove(product.product_image_filepath)

            # Remove Product
            db.session.delete(product)
            db.session.commit()
            return {"status_message":"Product Removed","status":"success","status_code":200}
        else:
            return{"status_message":"Product Not Found","status":"failed","status_code":400}

    except Exception as e:
        logger.debug(f"RemoveProductError: Failed to Remove Product,{e}")
        return{"status_message":"Failed to Remove Product","status":"failed","status_code":400}


def Edit_Product(account_type,account_id,**kwargs):
    """
    This function edits an uploaded product

    Params
    ------
    account_type: The type of account used to edit products
                    account_type options: admin,vendor
    account_id: The id of the account used to edit products
    product_id: The id of the product to be edited
    product_name: The name of the product to be edited
    product_description: The description of the product to be edited
    product_price: The price of the product to be edited
    product_image: The image of the product to be edited
    product_discount: The discount of the product to be edited
    product_is_available: The availability of the product to be edited

    Returns
    -------
    updated_product_id: The id of the product to be edited
    updated_product_name: The name of the product to be edited
    updated_product_description: The description of the product to be edited
    updated_product_price: The price of the product to be edited
    updated_product_image: The image of the product to be edited
    updated_product_discount: The discount of the product to be edited
    updated_product_is_available: The availability of the product to be edited
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # For Admin
        if account_type == "admin":
            
            # Verify Account Is Admin
            admin = Admin.query.filter_by(admin_id=account_id).first()
            
            # Verify Admin Exists
            if admin is not None:

                # Admin Edit Product
                product = Product.query.filter_by(product_id=kwargs["product_id"]).first()

        # For Vendor
        elif account_type == "vendor":

            # Fetch Vendor Product
            product = Product.query.filter_by(product_id=kwargs["product_id"],product_owner=account_id).first()

        else:
            product = None

        # Verify Product Exists
        if product is not None:
            
            # Get Product Image
            product_image = kwargs["product_image"]

            # Get Image
            if product_image is not None:

                # Read Product Image
                image = product_image.read()

                # Convert Image To Bytes
                image = BytesIO(image)

                # Convert Image To PIL Image
                image = Image.open(image)

                # Get Image Name
                image_name = product_image.filename

                # Image Name
                product_image_name = f"{genID()}_{image_name}"

                # Image Destination
                image_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"static/images/products/{product_image_name}")

                # Save Image
                image.save(image_destination)

                # remove old image
                old_image = product.product_image_filepath
                os.remove(old_image)

                # Edit Image Data
                product.product_image_name = product_image_name
                product.product_image_filepath = image_destination

            # Edit Product
            product.product_name = kwargs["product_name"] if kwargs["product_name"] is not None else product.product_name
            product.product_description = kwargs["product_description"] if kwargs["product_description"] is not None else product.product_description
            product.product_price = kwargs["product_price"] if kwargs["product_price"] is not None else product.product_price
            product.product_discount = kwargs["product_discount"] if kwargs["product_discount"] is not None else product.product_discount
            product.product_is_available = kwargs["product_is_available"] if kwargs["product_is_available"] is not None else product.product_is_available
            db.session.commit()

            return {"product_id":product.product_id,"product_name":product.product_name,"product_description":product.product_description,"product_price":product.product_price,"product_image_name":f"localhost:5003/static/images/products/{product.product_image_name}","product_discount":product.product_discount,"product_is_available":product.product_is_available,"status_message":"Product Edited","status":"success","status_code":200}
        else:
            return{"status_message":"Product Not Found","status":"failed","status_code":400}

    except Exception as e:
        logger.debug(f"EditProductError: Failed to Edit Product,{e}")
        return{"status_message":"Failed to Edit Product","status":"failed","status_code":400}


def Fetch_Vendors(admin_id,filter):
    """
    This function fetches all the vendors 
    and filters them depending on the filter

    Params
    ------
    admin_id: The id of the admin used to fetch vendors
    filter: The filter used to filter vendors
            options: all,active,inactive

    Returns
    -------
    vendors: The list of vendors
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Check For Admin
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        # Verify Admin Exists
        if admin is not None:

            # Fetch Vendors
            vendors = Vendor.query.all()

            # Filter Vendors
            if filter == "active":
                vendors = [{"vendor_id":vendor.vendor_id,"vendor_name":vendor.vendor_name,"vendor_email":vendor.vendor_email,"vendor_push_notification_token":vendor.vendor_push_notification_token} for vendor in vendors if vendor.permitted == True]
            elif filter == "inactive":
                vendors = [{"vendor_id":vendor.vendor_id,"vendor_name":vendor.vendor_name,"vendor_email":vendor.vendor_email,"vendor_push_notification_token":vendor.vendor_push_notification_token} for vendor in vendors if not vendor.permitted == True]
            else:
                vendors = [{"vendor_id":vendor.vendor_id,"vendor_name":vendor.vendor_name,"vendor_email":vendor.vendor_email,"vendor_push_notification_token":vendor.vendor_push_notification_token, "vendor_permitted":vendor.permitted} for vendor in vendors]

        # Return Vendors
        return {"vendors":vendors,"status_message":"Vendors Fetched","status":"success","status_code":200}

    except Exception as e:
        logger.debug(f"FetchVendorsError: Failed to Fetch Vendors,{e}")
        return{"status_message":"Failed to Fetch Vendors","status":"failed","status_code":400}


def Single_Vendor(vendor_id):
    """
    This function fetches a single vendor

    Params
    ------
    vendor_id: The id of the vendor to be fetched

    Returns
    -------
    vendor: The vendor to be fetched
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Fetch Vendor
        vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()

        # Verify Vendor Exists
        if vendor is not None:

            # Return Vendor
            return {"vendor":{"vendor_id":vendor.vendor_id,"vendor_name":vendor.vendor_name,"vendor_email":vendor.vendor_email,"vendor_push_notification_token":vendor.vendor_push_notification_token,"vendor_permitted":vendor.permitted},"status_message":"Vendor Fetched","status":"success","status_code":200}
        else:
            return{"status_message":"Vendor Not Found","status":"failed","status_code":400}

    except Exception as e:
        logger.debug(f"SingleVendorError: Failed to Fetch Vendor,{e}")
        return{"status_message":"Failed to Fetch Vendor","status":"failed","status_code":400}


def Make_Featured_Product(admin_id,product_id):
    """
    This function makes a product featured

    Params
    ------
    admin_id: The id of the admin used to make a product featured
    product_id: The id of the product to be made featured

    Returns
    -------
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Check For Admin
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        # Verify Admin Exists
        if admin is not None:

            # Fetch Product
            product = Product.query.filter_by(product_id=product_id).first()

            # Verify Product Exists
            if product is not None:

                # Make Product Featured
                product.product_is_featured = True

                # Commit Changes
                db.session.commit()

                # Return Success
                return {"status_message":"Product Made Featured","status":"success","status_code":200}
            else:
                return{"status_message":"Product Not Found","status":"failed","status_code":400}

        else:
            return{"status_message":"Admin Not Found","status":"failed","status_code":400}

    except Exception as e:
        logger.debug(f"MakeFeaturedProductError: Failed to Make Product Featured,{e}")
        return{"status_message":"Failed to Make Product Featured","status":"failed","status_code":400}


def Make_Non_Featured_Product(admin_id,product_id):
    """
    This function makes a product non featured

    Params
    ------
    admin_id: The id of the admin used to make a product non featured
    product_id: The id of the product to be made non featured

    Returns
    -------
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Check For Admin
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        # Verify Admin Exists
        if admin is not None:

            # Fetch Product
            product = Product.query.filter_by(product_id=product_id).first()

            # Verify Product Exists
            if product is not None:

                # Make Product Non Featured
                product.product_is_featured = False

                # Commit Changes
                db.session.commit()

                # Return Success
                return {"status_message":"Product Made Non Featured","status":"success","status_code":200}
            else:
                return{"status_message":"Product Not Found","status":"failed","status_code":400}

        else:
            return{"status_message":"Admin Not Found","status":"failed","status_code":400}

    except Exception as e:
        logger.debug(f"MakeNonFeaturedProductError: Failed to Make Product Non Featured,{e}")
        return{"status_message":"Failed to Make Product Non Featured","status":"failed","status_code":400}


def Get_Featured_Products():
    """
    This function returns all featured products

    Params
    ------
    None

    Returns
    -------
    featured_products: The featured products
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Fetch Featured Products
        products = Product.query.filter_by(product_is_featured=True).all()

        # Verify Products Exists
        if products is not None:
            
            # Get Featured Products
            featured_products = [{"product_id":product.product_id,"product_name":product.product_name,"product_description":product.product_description,"product_price":product.product_price,"product_image":f"localhost:5003/static/images/products/{product.product_image_name}","product_discount":product.product_discount,"product_is_available":product.product_is_available,"product_owner":product.product_owner} for product in products]

            # Return Featured Products
            return {"featured_products":featured_products,"status_message":"Featured Products Fetched","status":"success","status_code":200}
        else:
            return{"status_message":"Featured Products Not Found","status":"failed","status_code":400}

    except Exception as e:
        logger.debug(f"GetFeaturedProductError: Failed to Fetch Featured Products,{e}")
        return{"status_message":"Failed to Fetch Featured Products","status":"failed","status_code":400}


def Toggle_Enable_Customer(action,admin_id,customer_id):
    """ 
    This function enables admin to activate or deactivate a vendors account

    Params
    ------
    action: The action to be performed
            ation options: activate,deactivate
    admin_id: The id of the admin
    vendor_id: The id of the vendor

    Returns
    -------
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Fetch Admin
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        # Check Admin Exists
        if admin is not None: 

            # Fetch Vendor
            customer = Customer.query.filter_by(customer_id=customer_id).first()
            
            #  Activate Vendor
            if action == "activate":
                customer.permitted = True
                customer.permited_by = admin_id
                db.session.commit()
                return {"status_message":"Customer Activated","status":"success","status_code":200}

            # Deactivate Vendor
            elif action == "deactivate":
                customer.permitted = False
                customer.permited_by = admin_id
                db.session.commit()
                return {"status_message":"Customer Deactivated","status":"success","status_code":200}

            # On Invalid Action
            else:
                return{"status_message":"Invalid Action","status":"failed","status_code":400}

        # On Invalid Admin
        else:
            return{"status_message":"Invalid Admin","status":"failed","status_code":400}

    # On Error Handler and Return Response
    except Exception as e:
        logger.debug(f"ToggleEnableCustomerError: Failed to Toggle Enable Vendor,{e}")
        return{"message":"Failed to Toggle Enable Customer","status":"failed","status_code":400}


def Get_All_Customers(admin_id,filter):
    """
    This function fetches all the vendors 
    and filters them depending on the filter

    Params
    ------
    admin_id: The id of the admin used to fetch vendors
    filter: The filter used to filter vendors
            options: all,active,inactive

    Returns
    -------
    customers: The list of customers
    status_message: the result of the api query
    status: Add Product Status
            options: success,failed
    status_code: request status code
    """
    try:
        # Check For Admin
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        # Verify Admin Exists
        if admin is not None:

            # Fetch Vendors
            customers = Customer.query.all()

            # Filter Vendors
            if filter == "active":
                customers = [{"customer_id":customer.customer_id,"customer_name":customer.customer_name,"customer_email":customer.customer_email,"customer_address":customer.customer_address,"customer_push_notification_token":customer.customer_push_notification_token} for customer in customers if customer.permitted == True]
            elif filter == "inactive":
                customers = [{"customer_id":customer.customer_id,"customer_name":customer.customer_name,"customer_email":customer.customer_email,"customer_address":customer.customer_address,"customer_push_notification_token":customer.customer_push_notification_token} for customer in customers if not customer.permitted == True]
            else:
                customers = [{"customer_id":customer.customer_id,"customer_name":customer.customer_name,"customer_email":customer.customer_email,"customer_address":customer.customer_address,"customer_push_notification_token":customer.customer_push_notification_token, "customer_permitted":customer.permitted} for customer in customers]

        # Return Vendors
        return {"vendors":customers,"status_message":"Customers Fetched","status":"success","status_code":200}

    except Exception as e:
        logger.debug(f"FetchCustomersError: Failed to Fetch Customers,{e}")
        return{"status_message":"Failed to Fetch Customers","status":"failed","status_code":400}