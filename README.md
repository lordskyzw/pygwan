# Pygwan

Unofficial Python wrapper for the WhatsApp Cloud API by <b>[Tarmica Chiwara](https://github.com/lordskyzw)</b>.

## Installation

To install the WhatsApp Python wrapper, use the following command:

```bash
pip install pygwan
```

## Usage

Import the `WhatsApp` class from the package and initialize an instance with your WhatsApp token and phone number ID:

```python
from pygwan import WhatsApp

whatsapp = WhatsApp(token="your_token", phone_number_id="your_phone_number_id")
```

### Sending a Message

You can send a text message to a WhatsApp user using the `send_message` method:

```python
whatsapp.send_message("Hello, this is a test message.", "recipient_phone_number")
```

### Replying to a Message

Reply to a message using the `reply_to_message` method:

```python
whatsapp.reply_to_message("message_id", "recipient_phone_number", "Reply message.")
```

### Sending a Template

Send a template message using the `send_template` method:

```python
components = [
    # List of template components
    # Example: {"type": "text", "text": "Hello, this is a template message."}
]
whatsapp.send_template("template_name", "recipient_phone_number", components)
```

### Sending a Location

Send a location message using the `send_location` method:

```python
whatsapp.send_location("-23.564", "-46.654", "Location Name", "Location Address", "recipient_phone_number")
```

### Sending an Image

Send an image message using the `send_image` method:

```python
image_link = "https://example.com/image.jpg"
whatsapp.send_image(image_link, "recipient_phone_number")
```


For more detailed usage and information, please refer to the official documentation in the code lol

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
