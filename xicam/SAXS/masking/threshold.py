import numpy as np
from scipy.ndimage import morphology

from xicam.core.intents import OverlayIntent, ImageIntent
from xicam.plugins.operationplugin import operation, output_names, display_name, describe_input, describe_output, \
    categories, intent, visible

@operation
@display_name('Intensity Threshold')
@describe_input('images', 'Frame image data')
@describe_input('minimum', 'Threshold floor')
@describe_input('maximum', 'Threshold ceiling')
@describe_input('neighborhood', 'Neighborhood size in pixels for morphological opening. Only clusters of this size \
                            that fail the threshold are masked')
# @describe_output('mask', 'mask array for overlay')
@describe_output('images', 'original images')
@describe_output('threshold_mask', 'threshold mask')
@output_names('threshold_mask', 'images')
#FIXME: What values in output_map?
@intent(OverlayIntent, name='threshold', output_map={'image': 'threshold_mask'})
@intent(ImageIntent, name='image', output_map={'image': 'images'})
@visible('images', False)
@categories('Masking')
#TODO add the other decorators
def threshold_mask(images: np.ndarray,
             minimum: int=0,
             maximum: int=1e3,
             neighborhood: int=2):
    if minimum is None:
        minimum = np.min(images)
    if maximum is None:
        maximum = np.max(images)

    threshold_mask = np.logical_or(images < minimum, images > maximum)

    y, x = np.ogrid[-neighborhood:neighborhood + 1,
                    -neighborhood:neighborhood + 1]
    kernel = x ** 2 + y ** 2 <= neighborhood ** 2

    morphology.binary_opening(threshold_mask, kernel, output=threshold_mask)  # write-back to mask
    if threshold_mask is not None:
        threshold_mask = np.logical_or(threshold_mask, threshold_mask)  # .astype(np.int, copy=False)
    return threshold_mask, images

