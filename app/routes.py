# importing libraries
import os

from io import BytesIO
from PIL import Image
from bcrypt import re
from itsdangerous import exc
from app.db_model import Admin
from datetime import datetime
from dotenv import load_dotenv
from app.server_utils import HelperClass
from flask import Flask,request,jsonify,current_app
from werkzeug.security import generate_password_hash, check_password_hash

# Set Up Logging For Automation
import logging

# Init App
app = current_app

# ------- Configuring Logging File -------- #

# Logger For Log File
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log File Logging Format
formatter = logging.Formatter("%(asctime)s:%(levelname)s::%(message)s")

# Log File Handler
Log_File_Handler = logging.FileHandler("doxael.log")
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
logger.info("App Backend :: Logging Active")
logger.debug("")

# Load env File
load_dotenv(".env")

# Test Route
@app.route("/test")
def test():
    return jsonify({"message": f"Api for {os.environ.get('PROJECT_NAME').upper()} is Alive", "status": "success"})


# Create Admin
@app.route(f"/create_admin", methods=["POST"])
def create_admin():
    
    try:
        # Get Form Data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]

        admin_id = HelperClass.genUniqueID(Admin)
        push_notification_token = HelperClass.genUniqueToken(Admin)
        hashed_password = generate_password_hash(password, method="pbkdf2:sha512:80000")

        kwargs = {
            "admin_id":admin_id,
            "admin_name":f"{first_name}_{last_name}",
            "admin_email":email,
            "password":hashed_password,
            "admin_push_notification_token":push_notification_token
        }

        # Create Admin Account
        response = Admin.create_account(**kwargs)
        return response

    except Exception as e:
        logger.exception(e)
        return{
            "message":'Unable to create admin',
            "status":"failed"
        }


# Edit Admin
@app.route("/edit_admin/<string:admin_id>", methods=["PUT"])
def edit_admin(admin_id):
    try:
        form_keys = list(request.form.keys())

        kwargs = {}
        for key in form_keys:
            kwargs[key] = request.form[key]

        response = Admin.edit_account(admin_id,**kwargs)
        return response

    except Exception as e:
        logger.exception(e)
        return{
            "message":"Unable to edit account",
            "status":"failed"
        }

# Delete Admin
@app.route("/delete_admin/<string:admin_id>", methods=["DELETE"])
def delete_admin(admin_id):
    try:
        response = Admin.delete_account(admin_id)
        return response

    except Exception as e:
        logger.exception(e)
        return{
            "message":"An error occurred while deleting account",
            "status":"failed"
        }


# @app.route(f"/admin_login",methods=["POST"])
# def admin_login():

#     # Handle Request
#     email = request.form["email"]
#     password = request.form["password"]

#     # Account Login
#     login_response = Account_Login("admin",email,password)

#     # Request Response
#     return(login_response)


# @app.route(f"/all_vendors",methods=["POST"])
# def all_vendors():

#     # Handle Request Filter
#     admin_id = request.form["admin_id"]
#     filter = request.form["filter"]

#     # Fetch Vendor
#     fetch_vendor_response = Fetch_Vendors(admin_id,filter)
#     return fetch_vendor_response


# @app.route(f"/admin_enable_vendor",methods=["POST"])
# def enable_vendor():
    
#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     vendor_id = request.form["vendor_id"]

#     # Enable Vendor
#     Enable_Vendor_Response = Toggle_Enable_Vendor("activate",admin_id,vendor_id)
#     return Enable_Vendor_Response


# @app.route(f"/admin_disable_vendor",methods=["POST"])
# def disable_vendor():
    
#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     vendor_id = request.form["vendor_id"]

#     # Enable Vendor
#     Enable_Vendor_Response = Toggle_Enable_Vendor("deactivate",admin_id,vendor_id)
#     return Enable_Vendor_Response


# @app.route(f"/all_admin_products",methods=["POST"])
# def all_admin_products():

#     # Get Vendor ID
#     admin_id = request.form["admin_id"]

#     # Get All Products
#     all_products = Get_All_Products("admin",admin_id)
#     return all_products


# @app.route(f"/admin_remove_product",methods=["POST"])
# def admin_remove_product():
    
#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     product_id = request.form["product_id"]

#     # Remove Product
#     Remove_Product_Response = Remove_Product("admin",admin_id,product_id)
#     return Remove_Product_Response


# @app.route(f"/admin_edit_product",methods=["POST"])
# def admin_edit_product():

#     # Get Form Data
#     owner_id = request.form["admin_id"]
#     product_id = request.form["product_id"]

#     product_name = request.form["product_name"] if "product_name" in request.form else None
#     product_description = request.form["product_description"] if "product_description" in request.form else None
#     product_price = request.form["product_price"] if "product_price" in request.form else None
#     product_image = request.files["product_image"] if "product_image" in request.files else None
#     product_discount = request.form["product_discount"] if "product_discount" in request.form else None
#     product_is_available = request.form["product_is_available"] if "product_is_available" in request.form else None

#     # Edit Product
#     Edit_Product_Response = Edit_Product("admin",account_id=owner_id,product_id=product_id,product_name=product_name,product_description=product_description,product_price=product_price,product_image=product_image,product_discount=product_discount,product_is_available=product_is_available)
#     return Edit_Product_Response


# @app.route(f"/admin_make_featured_product",methods=["POST"])
# def make_featured_product():

#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     product_id = request.form["product_id"]

#     # Make Featured Product
#     Make_Featured_Product_Response = Make_Featured_Product(admin_id,product_id)
#     return Make_Featured_Product_Response


# @app.route(f"/admin_remove_featured_product",methods=["POST"])
# def remove_featured_product():
 
#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     product_id = request.form["product_id"]

#     # Remove Featured Product
#     Remove_Featured_Product_Response = Make_Non_Featured_Product(admin_id,product_id)
#     return Remove_Featured_Product_Response


# @app.route(f"/admin_enable_customer",methods=["POST"])
# def enable_customer():
        
#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     customer_id = request.form["customer_id"]

#     # Enable Customer
#     Enable_Customer_Response = Toggle_Enable_Customer("activate",admin_id,customer_id)
#     return Enable_Customer_Response


# @app.route(f"/admin_disable_customer",methods=["POST"])
# def disable_customer():
        
#     # Get Form Data
#     admin_id = request.form["admin_id"]
#     customer_id = request.form["customer_id"]

#     # Enable Customer
#     Enable_Customer_Response = Toggle_Enable_Customer("deactivate",admin_id,customer_id)
#     return Enable_Customer_Response


# @app.route(f"/all_customers",methods=["POST"])
# def all_customers():
    
#     # Get Form Data
#     filter = request.form["filter"]
#     admin_id = request.form["admin_id"]

#     # Get All Customers
#     All_Customers_Response = Get_All_Customers(admin_id,filter)
#     return All_Customers_Response


# @app.route(f"/admin_reset_password",methods=["POST"])
# def admin_reset_password():

#     # Get Form Data
#     email = request.form["email"]

#     # Reset Password
#     Reset_Password_Response = Reset_Password("admin",email)
#     return Reset_Password_Response


# @app.route(f"/admin_update_password",methods=["POST"])
# def admin_update_password():

#     # Get Form Data
#     session_token = request.form["reset_token"]
#     pin = request.form["reset_pin"]
#     password = request.form["password"]
#     confirmPassword = request.form["confirmPassword"]

#     # Update Password
#     Update_Password_Response = Update_Password("admin",session_token,pin,password,confirmPassword)
#     return Update_Password_Response


# # Vendor Routes
# @app.route(f"/create_vendor", methods=["POST"])
# def create_vendor():

#     # Get Form Data
#     email = request.form["email"]
#     password = request.form["password"]
#     username = request.form["username"]

#     # Create Admin Account
#     Create_Response = Create_Account("vendor",email=email,password=password,username=username)
#     return Create_Response


# @app.route(f"/vendor_login",methods=["POST"])
# def vendor_login():

#     # Handle Request
#     email = request.form["email"]
#     password = request.form["password"]

#     # Account Login
#     login_response = Account_Login("vendor",email,password)

#     # Request Response
#     return(login_response)


# @app.route(f"/vendor_reset_password",methods=["POST"])
# def vendor_reset_password():

#     # Get Form Data
#     email = request.form["email"]

#     # Reset Password
#     Reset_Password_Response = Reset_Password("vendor",email)
#     return Reset_Password_Response


# @app.route(f"/vendor_update_password",methods=["POST"])
# def vendor_update_password():

#     # Get Form Data
#     session_token = request.form["reset_token"]
#     pin = request.form["reset_pin"]
#     password = request.form["password"]
#     confirmPassword = request.form["confirmPassword"]

#     # Update Password
#     Update_Password_Response = Update_Password("vendor",session_token,pin,password,confirmPassword)
#     return Update_Password_Response


# @app.route(f"/all_vendor_products",methods=["POST"])
# def all_vendor_products():

#     # Get Vendor ID
#     vendor_id = request.form["vendor_id"]

#     # Get All Products
#     all_products = Get_All_Products("vendor",vendor_id)
#     return all_products


# @app.route(f"/vendor_edit_product",methods=["POST"])
# def vendor_edit_product():
    
#     # Get Form Data
#     owner_id = request.form["vendor_id"]
#     product_id = request.form["product_id"]

#     product_name = request.form["product_name"] if "product_name" in request.form else None
#     product_description = request.form["product_description"] if "product_description" in request.form else None
#     product_price = request.form["product_price"] if "product_price" in request.form else None
#     product_image = request.files["product_image"] if "product_image" in request.files else None
#     product_discount = request.form["product_discount"] if "product_discount" in request.form else None
#     product_is_available = request.form["product_is_available"] if "product_is_available" in request.form else None

#     # Edit Product
#     Edit_Product_Response = Edit_Product("vendor",account_id=owner_id,product_id=product_id,product_name=product_name,product_description=product_description,product_price=product_price,product_image=product_image,product_discount=product_discount,product_is_available=product_is_available)
#     return Edit_Product_Response


# @app.route(f"/vendor_remove_product",methods=["POST"])
# def vendor_remove_product():
    
#     # Get Form Data
#     vendor_id = request.form["vendor_id"]
#     product_id = request.form["product_id"]

#     # Remove Product
#     Remove_Product_Response = Remove_Product("vendor",vendor_id,product_id)
#     return Remove_Product_Response


# # Customer Routes
# @app.route(f"/create_customer", methods=["POST"])
# def create_customer():

#     # Get Form Data
#     email = request.form["email"]
#     password = request.form["password"]
#     username = request.form["username"]

#     # Create Admin Account
#     Create_Response = Create_Account("customer",email=email,password=password,username=username)
#     return Create_Response


# @app.route(f"/customer_login",methods=["POST"])
# def customer_login():

#     # Handle Request
#     email = request.form["email"]
#     password = request.form["password"]

#     # Account Login
#     login_response = Account_Login("customer",email,password)

#     # Request Response
#     return(login_response)


# @app.route(f"/customer_reset_password",methods=["POST"])
# def customer_reset_password():

#     # Get Form Data
#     email = request.form["email"]

#     # Reset Password
#     Reset_Password_Response = Reset_Password("customer",email)
#     return Reset_Password_Response


# @app.route(f"/customer_update_password",methods=["POST"])
# def customer_update_password():

#     # Get Form Data
#     session_token = request.form["reset_token"]
#     pin = request.form["reset_pin"]
#     password = request.form["password"]
#     confirmPassword = request.form["confirmPassword"]

#     # Update Password
#     Update_Password_Response = Update_Password("customer",session_token,pin,password,confirmPassword)
#     return Update_Password_Response


# @app.route(f"/show_customer_purchases",methods=["POST"])
# def show_customer_purchases():
    
#         # Get Customer ID
#         customer_id = request.form["customer_id"]
#         filter_type = request.form["filter_type"] if "filter_type" in request.form else None
#         filter_value = request.form["filter_value"] if "filter_value" in request.form else None
    
#         # Get All Purchases
#         all_purchases = Show_Purchases(customer_id,filter_type,filter_value)
#         return all_purchases


# @app.route(f"/add_customer_purchases",methods=["POST"])
# def add_purchases():

#     try:
#         # Get Form Data
#         order_id = request.json["order_id"]
#         customer_id = request.json["customer_id"]
#         total_price = request.json["total_price"]
#         purchase_data = request.json["purchases"]

#         # Add Purchase
#         Add_Purchase_Response = Add_Purchase(customer_id,order_id,total_price,purchase_data)
#         return Add_Purchase_Response

#     except Exception as e:
#         return jsonify({"error":str(e)})


# # Multi Category Routes
# @app.route(f"/add_product",methods=["POST"])
# def add_product():
    
#     # Get Form Data
#     owner_id = request.form["owner_id"]
#     product_name = request.form["product_name"]
#     product_description = request.form["product_description"]
#     product_price = request.form["product_price"]
#     product_image_name = request.files["product_image"].filename
#     product_image = request.files["product_image"]
#     product_discount = request.form["product_discount"]

#     # Add Product
#     newProduct = Add_Product(owner_id,product_name,product_description,product_price,product_image,product_image_name,product_discount)
#     return newProduct


# @app.route(f"/single_product",methods=["POST"])
# def single_product():

#     # Get Product ID
#     product_id = request.form["product_id"]

#     # Get Product
#     product_data = Get_Single_Product(product_id)
#     return product_data


# @app.route(f"/all_products",methods=["GET"])
# def all_products():

#     # Get All Products
#     all_products = Get_All_Products()
#     return all_products


# @app.route(f"/single_vendor",methods=["POST"])
# def fetch_vendor_details():

#     # Handle Request
#     vendor_id = request.form["vendor_id"]

#     # Fetch Vendor Details
#     fetch_vendor_details_response = Single_Vendor(vendor_id)
#     return fetch_vendor_details_response


# @app.route(f"/featured_products",methods=["GET"])
# def feature_products():
    
#     # Get Featured Products
#     featured_products = Get_Featured_Products()
#     return featured_products
