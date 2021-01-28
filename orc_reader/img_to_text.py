import datetime
import os

import click
import cv2
import numpy as np
import orc_logger
import pytesseract
from PIL import Image

VALID_EXTEND_FILE = ['.PNG', '.PDF', '.JPEG']
TEMP_IMG = 'datatest/removed_noise.png'


def read_image_with_pil(image_directory):
    try:
        img = Image.open(image_directory)
        return img
    except IOError:
        orc_logger.error('PIL can not read a file, maybe it is not a image')
        raise IOError


def validate_file(image_directory):
    orc_logger.info('start validate input')

    def _validate_file_exist():
        if not os.path.isfile(image_directory) or not os.access(image_directory, os.R_OK):
            orc_logger.error('file not exists or not readable')
            raise Exception

    def _validate_file_extension():
        _, file_extension = os.path.splitext(image_directory)
        if file_extension.upper() in VALID_EXTEND_FILE:
            orc_logger.info('end validate input')
            return file_extension

        orc_logger.error(f"only allow file extend: {VALID_EXTEND_FILE}")
        raise Exception

    _validate_file_exist()
    return _validate_file_extension()


def recognize_text_with_tesseract(image_directory):
    try:
        orc_logger.info(f'start recognize text with tesseract')

        orc_logger.info(f'read image and convert it to gray')
        img = cv2.imread(image_directory)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        orc_logger.info(f'remove noise in image')
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        cv2.erode(img, kernel, iterations=1)
        cv2.imwrite(TEMP_IMG, img)
        image_detect = Image.open(TEMP_IMG)

        orc_logger.info(f'start recognize text with tesseract')
        result = pytesseract.image_to_string(image_detect)
        orc_logger.info(f'end recognize text with tesseract')

        return result.strip()
    except Exception as e:
        orc_logger.error(e)


def convert_pdf_to_img():
    # TODO
    pass


@click.command()
@click.option('--input', required=True, help='directory of image')
@click.option('--output', default='output.text', help='logout output')
@click.option('--verbose', '-v', is_flag=True, help='display login in command')
def get_string(input, output, verbose):
    try:
        if output:
            orc_logger.set_log_name(output)

        orc_logger.info(f'start time: {datetime.datetime.now()}')
        orc_logger.info(f'receive input file: {input}')
        orc_logger.info(f'receive output file: {output}')
        type_file = validate_file(input)
        if type_file == VALID_EXTEND_FILE[1]:
            input = convert_pdf_to_img()

        text = recognize_text_with_tesseract(input)
        orc_logger.info(f'result  = \n {text}')
    except Exception as e:
        orc_logger.error(e)
    finally:
        orc_logger.info(f'end time: {datetime.datetime.now()}')


if __name__ == '__main__':
    get_string()
