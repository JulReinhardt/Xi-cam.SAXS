import numpy as np
from scipy.ndimage import morphology

from xicam.core.intents import OverlayIntent
from xicam.plugins.operationplugin import operation, output_names, display_name, describe_input, describe_output, \
    categories, intent, visible

@operation
@display_name('Intensity Threshold')
@describe_input('images', 'Frame image data')
@describe_input('minimum', 'Threshold floor')
@describe_input('maximum', 'Threshold ceiling')
@describe_input('neighborhood', 'Neighborhood size in pixels for morphological opening. Only clusters of this size \
                            that fail the threshold are masked')
@intent(OverlayIntent, name='threshold', output_map={'image': 'threshold_mask'})
@visible('images', False)
@categories('Masking')
#TODO add the other decorators
def threshold_mask(images: np.ndarray,
             minimum: int=None,
             maximum: int=None,
             neighborhood: int=2):
    if minimum is None:
        minimum = np.min(images)
    if maximum is None:
        maximum = np.max(images)

    mask = np.logical_or(images < minimum, images > maximum)

    y, x = np.ogrid[-neighborhood:neighborhood + 1,
                    -neighborhood:neighborhood + 1]
    kernel = x ** 2 + y ** 2 <= neighborhood ** 2

    morphology.binary_opening(mask, kernel, output=mask)  # write-back to mask
    if mask is not None:
        mask = np.logical_or(mask, mask)  # .astype(np.int, copy=False)
    return mask

