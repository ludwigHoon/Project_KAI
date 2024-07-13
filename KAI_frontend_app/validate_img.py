from PIL import Image
import requests
from io import BytesIO

# URL of the image
url = 'https://i.imgur.com/fhtXyYJ.png'

try:
    # Download the image
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Create a BytesIO object from the response content
    image_data = BytesIO(response.content)

    # Open the image with PIL
    image = Image.open(image_data)
    image.verify()  # Verify that it is, in fact, an image

    # Optionally, display the image (requires matplotlib)
    # import matplotlib.pyplot as plt
    # plt.imshow(image)
    # plt.axis('off')
    # plt.show()

    print("Image successfully opened and verified")
except requests.exceptions.RequestException as e:
    print(f"Error downloading the image: {e}")
except (IOError, SyntaxError) as e:
    print(f"Image file is not valid: {e}")
