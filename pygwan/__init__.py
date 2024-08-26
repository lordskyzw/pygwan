"""
This is the second iteration of the unofficial python wrapper for the WhatsApp Cloud API by Tarmica Chiwara
"""
from __future__ import annotations
import requests
import logging
import warnings
from colorama import Fore, Style
from typing import Dict, Any, Union

# Setup logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


class WhatsApp(object):
    """ "
    WhatsApp Object
    """

    def __init__(self, token=None, phone_number_id=None):
        """
        Initialize the WhatsApp Object

        Args:
            token[str]: Token for the WhatsApp cloud API obtained from the developer portal
            phone_number_id[str]: Phone number id for the WhatsApp cloud API obtained from the developer portal
        """
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v18.0"
        self.v15_base_url = "https://graph.facebook.com/v18.0"
        self.url = f"{self.base_url}/{phone_number_id}/messages"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }
    
    

    def send_message(
        self, message, recipient_id, recipient_type="individual", preview_url=True
    ):
        """
         Sends a text message to a WhatsApp user

         Args:
                message[str]: Message to be sent to the user
                recipient_id[str]: Phone number of the user with country code wihout +
                recipient_type[str]: Type of the recipient, either individual or group
                preview_url[bool]: Whether to send a preview url or not

        Example:
            ```python
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_message("Hello World", "5511999999999")
            >>> whatsapp.send_message("Hello World", "5511999999999", preview_url=False)

        """
        # if the message length is greater than 4096 characters, split the message into multiple messages

        if len(message) > 4096:
            messages = [
                message[i : i + 4096] for i in range(0, len(message), 4096)
            ]
            for msg in messages:
                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": recipient_type,
                    "to": recipient_id,
                    "type": "text",
                    "text": {"preview_url": preview_url, "body": msg},
                }
                logging.info(f"Sending message to {recipient_id}")
                r = requests.post(f"{self.url}", headers=self.headers, json=data)
                if r.status_code == 200:
                    logging.info(f"Message sent to {recipient_id}")
                else:
                    logging.info(f"Message not sent to {recipient_id}")
                    logging.info(f"Status code: {r.status_code}")
                    logging.error(f"Response: {r.json()}")

        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "text",
                "text": {"preview_url": preview_url, "body": message},
            }
            logging.info(f"Sending message to {recipient_id}")
            r = requests.post(f"{self.url}", headers=self.headers, json=data)
            if r.status_code == 200:
                logging.info(f"Message sent to {recipient_id}")
        return r.json()

    def reply_to_message(
        self, message_id: str, recipient_id: str, message: str, preview_url: bool = True
    ):
        """
        Replies to a message

        Args:
            message_id[str]: Message id of the message to be replied to
            recipient_id[str]: Phone number of the user with country code wihout +
            message[str]: Message to be sent to the user
            preview_url[bool]: Whether to send a preview url or not
        """
        if len(message) > 4096:
            messages = [
                message[i : i + 4096] for i in range(0, len(message), 4096)
            ]
            for msg in messages:
                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": recipient_id,
                    "type": "text",
                    "context": {"message_id": message_id},
                    "text": {"preview_url": preview_url, "body": msg},
                }
                logging.info(f"Replying to {message_id}")
                r = requests.post(f"{self.url}", headers=self.headers, json=data)
                if r.status_code == 200:
                    logging.info(f"Message sent to {recipient_id}")
                else:
                    logging.info(f"Message not sent to {recipient_id}")
                    logging.info(f"Status code: {r.status_code}")
                    logging.error(f"Response: {r.json()}")


        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_id,
                "type": "text",
                "context": {"message_id": message_id},
                "text": {"preview_url": preview_url, "body": message},
            }

            logging.info(f"Replying to {message_id}")
            r = requests.post(f"{self.url}", headers=self.headers, json=data)
            if r.status_code == 200:
                logging.info(f"Message sent to {recipient_id}")
        
        return r.json()
        
    def send_reaction(self, message_id: str, reaction: str, recipient_id: str):
        """
        Sends a reaction to a message

        Args:
            message_id[str]: Message id of the message to be reacted to
            reaction[str]: Unicode escape sequence emoji to be sent to the user
            recipient_id[str]: Phone number of the user with country code wihout +
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": reaction
            }
        }
        logging.info(f"Sending reaction to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Reaction sent to {recipient_id}")
            return r.json()
        logging.info(f"Reaction not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_template(self, template, recipient_id, components, lang: str = "en_US"):
        """
        Sends a template message to a WhatsApp user, Template messages can either be;
            1. Text template
            2. Media based template
            3. Interactive template
        You can customize the template message by passing a dictionary of components.
        You can find the available components in the documentation.
        https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates
        Args:
            template[str]: Template name to be sent to the user
            recipient_id[str]: Phone number of the user with country code wihout +
            lang[str]: Language of the template message
            components[list]: List of components to be sent to the user  # CHANGE
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_template("hello_world", "5511999999999", lang="en_US"))
        """
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template,
                "language": {"code": lang},
                "components": components,
            },
        }
        logging.info(f"Sending template to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Template sent to {recipient_id}")
            return r.json()
        logging.info(f"Template not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()
    
    
    def send_payload_template(self, template_name, recipient_id, variables, lang="en"):
        """
        Sends a template message with dynamic variables.

        Args:
            template_name (str): The name of the template
            recipient_id (str): The recipient's phone number
            variables (list of str): Variables to replace placeholders in the template
            lang (str): Language of the template. Defaults to 'en_US'.
        """
        # Ensure variables are in the correct format, which is a list of dictionaries
        # Each dictionary should have the key 'type' set to 'text' and the key 'text' set to the variable
        parameters = [{"type": "text", "text": str(variable)} for variable in variables]

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": lang},
                "components": [
                    {
                        "type": "body",
                        "parameters": parameters
                    }
                ]
            },
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"Template message sent to {recipient_id}")
        else:
            logging.error(f"Failed to send template message: {response.json()}")
        return response
    
    def send_payload_template_with_header(self, template_name, recipient_id, header_variables, body_variables, lang="en_GB"):
        """
        Sends a template message with dynamic variables.

        Args:
            template_name (str): The name of the template
            recipient_id (str): The recipient's phone number
            variables (list of str): Variables to replace placeholders in the template
            lang (str): Language of the template. Defaults to 'en_GB'.
        """
        # Ensure variables are in the correct format, which is a list of dictionaries
        # Each dictionary should have the key 'type' set to 'text' and the key 'text' set to the variable
        header_parameters = [{"type": "text", "text": str(variable)} for variable in header_variables]
        body_parameters = [{"type": "text", "text": str(variable)} for variable in body_variables]
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": lang},
                "components": [
                    {
                       "type": "header",
                       "parameters": header_parameters
                    },
                    {
                        "type": "body",
                        "parameters": body_parameters
                    }
                ]
            },
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"Template message sent to {recipient_id}")
        else:
            logging.error(f"Failed to send template message: {response.json()}")
        return response

    def send_templatev2(self, template, recipient_id, components, lang: str = "en_US"):
        message = f"{Fore.RED}The 'send_templatev2' method is being deprecated and will be removed in the future. Please use the 'send_template' method instead.{Style.RESET_ALL}"
        warnings.warn(message, DeprecationWarning)
        return send_template(template, recipient_id, components, lang=lang)  # type: ignore

    def send_image(
        self,
        image,
        recipient_id,
        recipient_type="individual",
        caption=None,
        link=True,
    ):
        """
        Sends an image message to a WhatsApp user

        There are two ways to send an image message to a user, either by passing the image id or by passing the image link.
        Image id is the id of the image uploaded to the cloud api.

        Args:
            image[str]: Image id or link of the image
            recipient_id[str]: Phone number of the user with country code wihout +
            recipient_type[str]: Type of the recipient, either individual or group
            caption[str]: Caption of the image
            link[bool]: Whether to send an image id or an image link, True means that the image is an id, False means that the image is a link


        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_image("https://i.imgur.com/Fh7XVYY.jpeg", "5511999999999")
        """
        if link:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": image, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"id": image, "caption": caption},
            }
        logging.info(f"Sending image to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Image sent to {recipient_id}")
            return r.json()
        logging.info(f"Image not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(r.json())
        return r.json()

    def mark_as_read(self, message_id: str) -> Dict[Any, Any]:
        """
        Marks a message as read

        Args:
            message_id[str]: Id of the message to be marked as read

        Returns:
            Dict[Any, Any]: Response from the API

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.mark_as_read("message_id")
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        json_data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        logging.info(f"Marking message {message_id} as read")
        response = requests.post(
            f"{self.v15_base_url}/{self.phone_number_id}/messages",
            headers=headers,
            json=json_data,
        ).json()
        if response:
            logging.info(f"Message {message_id} marked as read")
            return response
        logging.info(f"Error marking message {message_id} as read")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.json()}")
        return response


    def create_button(self, button: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Method to create a button object to be used in the send_message method.

        This is method is designed to only be used internally by the send_button method.

        Args:
               button[dict]: A dictionary containing the button data
        
        Example:
            >>> from pygwan import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.create_button({"header": "Choose a package:", "body": "Select from below:", "footer": "Footer text", "action": {"buttons": [{"id": "1", "title": "Option 1"}, {"id": "2", "title": "Option 2"}]}})
        """
        data = {"type": "list", "action": button.get("action")}
        if button.get("header"):
            data["header"] = {"type": "text", "text": button.get("header")}
        if button.get("body"):
            data["body"] = {"text": button.get("body")}
        if button.get("footer"):
            data["footer"] = {"text": button.get("footer")}
        return data

    def send_button(self, button: Dict[Any, Any], recipient_id: str) -> Dict[Any, Any]:
        """
        Sends an interactive buttons message to a WhatsApp user

        Args:
            button[dict]: A dictionary containing the button data(rows-title may not exceed 20 characters)
            recipient_id[str]: Phone number of the user with country code wihout +
        Example:
            >>> from pygwan import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_button({"header": "Choose a package:", "body": "Select from below:", "footer": "Footer text", "action": {"buttons": [{"id": "1", "title": "Option 1"}, {"id": "2", "title": "Option 2"}]}}, "5511999999999")
        """
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button(button),
        }
        logging.info(f"Sending buttons to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Buttons sent to {recipient_id}")
            return r.json()
        logging.info(f"Buttons not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()
    
    def send_interactive_buttons(self, recipient_id: str, username):
        """
        Sends interactive buttons to a WhatsApp user

        Args:
            recipient_id[str]: Phone number of the user with country code without +
        """
        button_payload = {
            "type": "button",
            "body": {
                "text": f"Hello *{username}*!\U0001F60A\nWelcome to My Dish \U0001F4FA, the quickest way to pay for your DSTV\n\n _NB: To start-over at any point, type 'reset'_\n\nPlease choose an option below to proceed:"
            },
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "pay_dstv", "title": "Pay for DSTV"}},
                    {"type": "reply", "reply": {"id": "contact_admin", "title": "Contact Admin"}}
                ]
            }
        }

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": button_payload
        }

        logging.info(f"Sending interactive buttons to {recipient_id}")
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"Interactive buttons sent to {recipient_id}")
            return response.json()
        logging.error(f"Error sending interactive buttons to {recipient_id}: {response.json()}")
        return response.json()


    def send_reply_button(
        self, button: Dict[Any, Any], recipient_id: str
    ) -> Dict[Any, Any]:
        """
        Sends an interactive reply buttons[menu] message to a WhatsApp user

        Args:
            button[dict]: A dictionary containing the button data
            recipient_id[str]: Phone number of the user with country code wihout +

        Note:
            The maximum number of buttons is 3, more than 3 buttons will rise an error.
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": button,
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Reply buttons sent to {recipient_id}")
            return r.json()
        logging.info(f"Reply buttons not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()


    def send_list_message(self, recipient_id, header, body, footer, buttons):
        """
        Sends a list message to a WhatsApp user.

        Args:
            recipient_id (str): Phone number of the recipient with country code without +.
            header (str): Header text of the list message.
            body (str): Body text of the list message.
            footer (str): Footer text of the list message.
            buttons (list): List of button dictionaries, each with 'title' and 'payload'.

        Example usage:
            >>> whatsapp.send_list_message("1234567890", "Choose a package:", "Select from below:", "Footer text", [{"title": "Option 1", "payload": "1"}, {"title": "Option 2", "payload": "2"}])
        """

        sections = [{"title": "Select one", "rows": [{"id": button["payload"], "title": button["title"]} for button in buttons]}]

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": header
                },
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Choose",
                    "sections": sections
                }
            }
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"List message sent to {recipient_id}")
            return response.json()
        logging.error(f"List message not sent to {recipient_id}: {response.text}")
        return response.json()

    def send_cta_url_button(self, recipient_id, button_text, url, message=None):
        """
        Sends a call-to-action URL button to a WhatsApp user.

        Args:
            recipient_id (str): Phone number of the recipient with country code without +.
            title (str): Title of the button.
            url (str): URL to open when the button is clicked.

        Example usage:
            >>> whatsapp.send_cta_url_button("1234567890", "Visit our website", "https://example.com")
        """
        body = {"body": {"text": message}} if message else {}
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "cta_url",
                **body,
                "action": {
                    "name": "cta_url",
                    "parameters": {
                        "display_text": button_text,
                        "url": url
                    }
                }
            }
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"CTA URL button sent to {recipient_id}")
            return response.json()
        logging.error(f"CTA URL button not sent to {recipient_id}: {response.text}")
        return response.json()
    
    def send_document(self, document_url: str, recipient_id: str, caption: str = "", filename: str = ""):
        """
        Sends a document to a WhatsApp user.
        
        Args:
            document_url (str): URL of the document to send.
            recipient_id (str): Phone number of the recipient with country code without +.
            caption (str): Caption for the document.
            filename (str): Name of the file. it should include the file extension.
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "document",
            "document": {
                "link": document_url,
                "caption": caption,
                "filename": filename
            }
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"Document sent to {recipient_id}")
            return response.json()
        logging.error(f"Document not sent to {recipient_id}: {response.text}")
        return response.json()

    def request_location(self, recipient_id: str, message: str):
        """
        Sends a request for the user's location.

        Args:
            recipient_id (str): Phone number of the recipient with country code without +.
            message (str): Message to send with the location request.
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "type": "interactive",
            "to": recipient_id,
            "interactive": {
                "type": "location_request_message",
                "body": {
                "text": message
                },
                "action": {
                "name": "send_location"
                }
            }
        }
        if len(message) >= 1025:
            raise ValueError("Message length should not exceed 1024 characters")

        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            logging.info(f"Location request sent to {recipient_id}")
            return response.json()
        logging.error(f"Location request not sent to {recipient_id}: {response.text}")
        return response.json()


    def download_media(
        self, media_url: str, mime_type: str, file_path: str = "temp"
    ) -> Union[str, None]:
        """
        Download media from media url obtained either by manually uploading media or received media

        Args:
            media_url[str]: Media url of the media
            mime_type[str]: Mime type of the media
            file_path[str]: Path of the file to be downloaded to. Default is "temp"
                            Do not include the file extension. It will be added automatically.

        Returns:
            str: Media url

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.download_media("media_url", "image/jpeg")
            >>> whatsapp.download_media("media_url", "video/mp4", "path/to/file") #do not include the file extension
        """
        r = requests.get(media_url, headers=self.headers)
        content = r.content
        extension = mime_type.split("/")[1]
        # create a temporary file
        try:
            save_file_here = (
                f"{file_path}.{extension}" if file_path else f"temp.{extension}"
            )
            with open(save_file_here, "wb") as f:
                f.write(content)
            logging.info(f"Media downloaded to {save_file_here}")
            return f.name
        except Exception as e:
            logging.info(e)
            logging.ERROR(f"Error downloading media to {save_file_here}")
            return None

    def preprocess(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Preprocesses the data received from the webhook.

        This method is designed to only be used internally.

        Args:
            data[dict]: The data received from the webhook

        Returns:
            this returns another dictionary with the values of the changed fields
        """
        return data["entry"][0]["changes"][0]["value"]

    def is_message(self, data: Dict[Any, Any]) -> bool:
        """is_message checks if the data received from the webhook is a message.

        Args:
            data (Dict[Any, Any]): The data received from the webhook

        Returns:
            bool: True if the data is a message, False otherwise
        """
        data = self.preprocess(data)
        if "messages" in data:
            return True
        else:
            return False

    def get_mobile(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Extracts the mobile number of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The mobile number of the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> mobile = whatsapp.get_mobile(data)
        """
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]

    def get_name(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Extracts the name of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The name of the sender
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> mobile = whatsapp.get_name(data)
        """
        contact = self.preprocess(data)
        if contact:
            return contact["contacts"][0]["profile"]["name"]

    def get_message(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Extracts the message content based on the type of the message.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The text message or interactive response received from the sender
        """
        data = self.preprocess(data)
        if "messages" in data:
            message_data = data["messages"][0]
            if message_data["type"] == "text":
                return message_data["text"]["body"]
            elif message_data["type"] == "interactive":
                # Handle interactive message type
                if "button_reply" in message_data["interactive"]:
                    return message_data["interactive"]["button_reply"]["title"]
        return None


    def get_message_id(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Extracts the message id of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The message id of the sender
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> message_id = whatsapp.get_message_id(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["id"]
        return None

    def get_conversation_id(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Extracts the conversation id from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The conversation id, or None if not found
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> conversation_id = whatsapp.get_conversation_id(data)
        """
        data = self.preprocess(data)
        if "conversation_id" in data:
            return data.get("conversation_id")
        return None

    def get_message_timestamp(self, data: Dict[Any, Any]) -> Union[str, None]:
        """ "
        Extracts the timestamp of the message from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The timestamp of the message
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_message_timestamp(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["timestamp"]

    def get_interactive_response(self, data: Dict[Any, Any]) -> Union[Dict, None]:
        """
         Extracts the response of the interactive message from the data received from the webhook.

         Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The response of the interactive message

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> response = whatsapp.get_interactive_response(data)
            >>> interactive_type = response.get("type")
            >>> message_id = response[interactive_type]["id"]
            >>> message_text = response[interactive_type]["title"]
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "interactive" in data["messages"][0]:
                return data["messages"][0]["interactive"]


    def get_image(self, data: Dict[Any, Any]) -> Union[Dict, None]:
        """ "
        Extracts the image of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The image_id of an image sent by the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> image_id = whatsapp.get_image(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "image" in data["messages"][0]:
                return data["messages"][0]["image"]


    def get_message_type(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Gets the type of the message sent by the sender from the data received from the webhook.


        Args:
            data [dict]: The data received from the webhook

        Returns:
            str: The type of the message sent by the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_message_type(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["type"]

    def get_delivery(self, data: Dict[Any, Any]) -> Union[Dict, None]:
        """
        Extracts the delivery status of the message from the data received from the webhook.
        Args:
            data [dict]: The data received from the webhook

        Returns:
            dict: The delivery status of the message and message id of the message
        """
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["status"]

    def changed_field(self, data: Dict[Any, Any]) -> str:
        """
        Helper function to check if the field changed in the data received from the webhook.

        Args:
            data [dict]: The data received from the webhook

        Returns:
            str: The field changed in the data received from the webhook

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.changed_field(data)
        """
        return data["entry"][0]["changes"][0]["field"]