from azure.storage.blob import BlockBlobService
from random import randint
from common import constants


# Fetch a random image (in bytes) and the name of the image (in str)
def fetch_random_image():
    # Get the image generator reference from the Blob
    block_blob_service = BlockBlobService(connection_string=constants.AZURE_STORAGE_CONNECTION_STRING)
    image_generator = block_blob_service.list_blobs(constants.CONTAINER_NAME)

    # Collect all images
    all_images = []
    for image in image_generator:
        all_images.append(image.name)

    # Get a random image
    random_image_idx = randint(0, len(all_images) - 1)
    random_image_bytes = block_blob_service.get_blob_to_bytes(constants.CONTAINER_NAME, all_images[random_image_idx]).content

    return random_image_bytes, all_images[random_image_idx]