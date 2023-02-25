###############################
#####                    ######
#####       MODELS       ######
#####                    ######
###############################

# Imports
import os
from click import echo
from itsdangerous import exc
import jwt
import uuid
import logging
import datetime
import sib_api_v3_sdk

from app import db
from PIL import Image
from io import BytesIO
from sib_api_v3_sdk.rest import ApiException
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text


# Configure API key authorization: api-key for SENDINBLUE
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.environ.get("SENDINBLUE_API_KEY")


# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log File Logging Format
formatter = logging.Formatter("%(asctime)s:%(levelname)s::%(message)s")

# Make Logging Directory
LOGS_DIR = "app/logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Log File Handler
Log_File_Handler = logging.FileHandler(f"{LOGS_DIR}/model.log")
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
logger.info("Models Section :: Logging Active")
logger.debug("")


class Admin(db.Model):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    admin_id = Column(String(255),unique=True)
    admin_name = Column(String(255),unique=False)
    admin_email = Column(String(255),unique=True)
    password = Column(String(255))
    admin_reset_pin = Column(String(255),unique=True)
    admin_push_notification_token = Column(String(255),unique=True)

    def __repr__(self):
        return f"<admin {self.admin_id}>"

    def dict(self):
        return{
            "id":self.admin_id,
            "name":self.admin_name,
            "email":self.admin_email,
        }

    def get_admin_id(self):
        return self.admin_id

    def get_name(self):
        return self.admin_name

    def get_email(self):
        return self.admin_email

    def get_reset_pin(self):
        return self.admin_reset_pin

    def get_push_notification_token(self):
        return self.admin_push_notification_token
        
    @staticmethod
    def get_admin_by_id(admin_id):
        """
        This function fetches an admin
        using their id

        Params:
        -------
        admin_id: The unique id of the admin account

        Returns:
        --------
        message: The response message
        status: The response status 
        """
        try:
            accounts = db.session.query(Admin).filter(Admin.admin_id == admin_id).all()

            if len(accounts) == 1:
                accounts = [account.dict() for account in accounts]

                return{
                    "message":accounts,
                    "status":"success"
                }

            elif len(accounts) > 1:
                return{
                    "message":"Error, multiple accounts detected",
                    "status":"warning"
                }

            else:
                return{
                    "message":"account does not exist",
                    "status":"failed"
                }

        except Exception as e:
            logger.exception(e)
            return{
                "message":"An error occurred while fetching account",
                "status":"failed"
            }

    @staticmethod
    def get_account_by_email(admin_email):
        """
        This method fetches an account with the
        specified email

        Params:
        -------
        admin_email: The unique email of the admin account

        Returns:
        --------
        message: The response message
        status: The response status
        """
        try:
            accounts = db.session.query(Admin).filter(Admin.admin_email == admin_email).all()

            if len(accounts) == 1:
                account = [account.dict for account in accounts]

                return{
                    "message":account,
                    "status":"success"
                }

            elif len(accounts) > 1:
                return{
                    "message":"Error, multiple accounts detected",
                    "status":"warning"
                }

            else:
                return{
                    "message":"account does not exist",
                    "status":"failed"
                }

        except Exception as e:
            logger.exception(e)
            return{
                "message":"failed to fetch account",
                "status":"failed"
            }


    def get_account_by_push_notification_token(push_notification_token):
        """
        This method fetches the account
        using the push notification token

        Params:
        -------
        push_notification_token: The uniques push 
                notification token of an admin account

        Returns
        -------
        message: The response message
        status: The response status
        """
        accounts = db.session.query(Admin).filter(
            Admin.admin_push_notification_token == push_notification_token
            ).all()

        if len(accounts) == 1:
            account = [account.dict() for account in accounts]
            return{
                "message":account,
                "status":"success"
            }

        elif len(accounts) > 1:
            return{
                "message":"Error, multiple accounts detected",
                "status":"warning"
            }

        else:
            return{
                "message":"account does not exist",
                "status":"failed"
            }

    @classmethod
    def create_account(cls,**kwargs):
        """
        This function is used to create new 
        admin accounts

        Params:
        -------
        kwargs:{
            admin_id: The generated account id,
            admin_name: admin account fullname
            admin_email: admin account email
            password: hashed password
            admin_push_notification_token: account push notification token
        }

        Returns:
        --------
        message: response message
        status: response status
        """
        try:
            response = cls.get_account_by_email(kwargs["admin_email"])
            
            if response["status"] == "failed":

                admin = cls(**kwargs)
                db.session.add(admin)
                db.session.commit()

                return{
                    "info":admin.dict(),
                    "push_notification_token":admin.get_push_notification_token(),
                    "message": "Admin account created",
                    "status":"success"
                }

            else:
                return response

        except Exception as e:
            logger.exception(e)
            return{
                "message":"failed to create admin account",
                "status":"failed"
            }


    @staticmethod
    def edit_account(admin_id,**kwargs):
        """
        This method edits an admin
        account using the specified id

        Params:
        -------
        admin_id: The id of the admin account
        kwargs:any({
            admin_name: admin account fullname
            admin_email: admin account email
            password: hashed password
            admin_reset_pin: reset pin for password change
            admin_push_notification_token: account push notification token
        })
        
        Returns:
        --------
        message: response message
        status: response status
        """
        try:
            admin = db.session.query(Admin).filter(Admin.admin_id == admin_id).first()
            if admin:
                db.session.query(Admin).filter(Admin.admin_id == admin_id).update({**kwargs})
                db.session.commit()

                return{
                    "message":"Update complete",
                    "status":"success"
                }

            else:
                return{
                    "message":"account does not exist",
                    "status":"failed"
                }

        except Exception as e:
            logger.exception(e)
            return{
                "message":"An error occurred while edit account",
                "status":"failed"
            }


    @staticmethod
    def delete_account(admin_id):
        """
        This method deletes an admin
        account

        Params:
        -------
        admin_id: The id of the admin account

        Returns:
        --------
        message: The response message
        status: The response status
        """
        try:
            admin = db.session.query(Admin).filter(Admin.admin_id == admin_id).first()

            if admin:
                db.session.delete(admin)
                db.session.commit()

                return{
                    "message":"Delete complete",
                    "status":"success"
                }

            else:
                return{
                    "message":"account does not exist",
                    "status":"failed"
                }

        except Exception as e:
            logger.exception(e)
            return{
                "message":"An error occurred while deleteing account",
                "status":"failed"
            }


    # def account_login(self):
    #     """
    #     This function validates that an admin
    #     exist and logs the admin in
    #     """

class Product(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_id = Column(String(255),unique=True)
    product_name = Column(String(255),unique=False)
    product_description = Column(String(255),unique=False)
    product_price = Column(String(255),unique=False)
    product_image_name = Column(String(255),unique=True)
    product_image_filepath = Column(String(255),unique=True)
    product_discount = Column(Integer,unique=False)
    product_owner = Column(String(255),unique=False)
    product_is_available = Column(Boolean,unique=False)
    product_is_featured = Column(Boolean,unique=False)

    def __repr__(self):
        return f"<product {self.product_id}>"

    def dict(self):
        return{
            "product_id":self.product_id,
            "product_name":self.product_name,
            "product_description":self.product_description,
            "product_price":self.product_price,
            "product_image_name":self.product_image_name,
            "product_image_filepath":self.product_image_filepath,
            "product_discount":self.product_discount,
            "product_ownwer":self.product_owner,
            "is_available":self.product_is_available,
            "is_featured":self.product_is_featured
        }

    def get_product_id(self):
        return self.product_id

    def get_product_name(self):
        return self.product_name

    def get_product_description(self):
        return self.product_description


class Vendor(db.Model):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True)
    vendor_id = Column(String(255),unique=True)
    vendor_name = Column(String(255),unique=False)
    vendor_email = Column(String(255),unique=True)
    password = Column(String(255),unique=True)
    vendor_reset_pin = Column(String(255),unique=True)
    permitted = Column(Boolean,unique=False)
    permitted_by = Column(String(255),unique=False)
    vendor_push_notification_token = Column(String(255),unique=True)

    def __repr__(self):
        return f"<vendor {self.vendor_id}>"


class Customer(db.Model):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(255),unique=True)
    customer_name = Column(String(255),unique=False)
    customer_email = Column(String(255),unique=True)
    password = Column(String(255),unique=True)
    customer_address = Column(Text(2000),unique=False,index=False)
    customer_cards = Column(Text(2000),unique=False,index=False)
    customer_reset_pin = Column(String(255),unique=True)
    customer_push_notification_token = Column(String(255),unique=True)
    permitted = Column(Boolean,unique=False)
    permitted_by = Column(String(255),unique=False)

    def __repr__(self):
        return f"<customer {self.customer_id}>"


class Orders(db.Model):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(255),unique=False)
    order_vendor_id = Column(String(255),unique=False)
    order_customer_id = Column(String(255),unique=False)
    order_product_id = Column(String(255),unique=False)
    item_unique_id = Column(String(255),unique=True)
    order_product_name = Column(String(255),unique=False)
    order_product_price = Column(String(255),unique=False)
    order_product_discount = Column(String(255),unique=False)
    order_product_quantity = Column(String(255),unique=False)
    order_total_price = Column(String(255),unique=False)
    order_product_image = Column(String(255),unique=False)
    order_product_description = Column(String(255),unique=False)
    order_product_is_available = Column(Boolean,unique=False)
    order_date = Column(DateTime,unique=False)

    def __repr__(self):
        return f"<order {self.order_id}>"


class Apikeys(db.Model):
    __tablename__ = "apikeys"

    id = Column(Integer, primary_key=True)
    apikey_vendor = Column(String(255),unique=True)
    apikey = Column(String(255),unique=True)

    def __repr__(self):
        return f"<apikey {self.apikey_vendor}>"