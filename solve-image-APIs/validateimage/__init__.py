import logging
import json

import azure.functions as func

from PIL import Image
from azure.storage.blob import BlockBlobService
from io import BytesIO

from common import image_helper
from common import constants


def get_image_from_id(image_id):
    # Get the image generator from the Blob using the id
    block_blob_service = BlockBlobService(connection_string=constants.AZURE_STORAGE_CONNECTION_STRING)
    image_generator = block_blob_service.list_blobs(constants.CONTAINER_NAME)

    # Find the image with the id
    image_name = ''
    for image in image_generator:
        if image_id == image_helper.get_hash(image.name):
            # We found the image
            image_name = image.name
            break

    if image_name == '':
        # TODO: Should return the appropriate response
        raise ValueError('Invalid ID: No image was found with the ID')

    # Return the actual image
    return block_blob_service.get_blob_to_bytes(constants.CONTAINER_NAME, image_name).content


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # We grab the required values
    image = req.params.get('image')
    image_id = req.params.get('id')
    if not image:
        try:
            req_body = json.loads(req.get_body().decode())
        except ValueError:
            pass
        else:
            image = req_body.get('image')
            image_id = req_body.get('id')

    if image and image_id:
        # We get the image from the storage using the id, and decode the image from the request
        image_from_storage_decoded = get_image_from_id(image_id)
        image_from_url_decoded = image_helper.decode_image_base64(image)

        # We open the images and compare their data
        image_from_url = Image.open(BytesIO(image_from_url_decoded))
        image_from_storage = Image.open(BytesIO(image_from_storage_decoded))

        match = list(image_from_url.getdata()) == list(image_from_storage.getdata())

        # Create the json for the response
        json_response = {
            "match": match
        }

        return func.HttpResponse(
            json.dumps(json_response),
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=200,
            mimetype='application/json'
        )

    else:
        return func.HttpResponse(
            "Please pass an image and rotation direction in the query string or the body",
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=400
        )
