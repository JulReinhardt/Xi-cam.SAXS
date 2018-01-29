from xicam.plugins import QWidgetPlugin
from pyqtgraph import ImageView, PlotItem
from xicam.core.data import NonDBHeader
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import numpy as np
from xicam.core import msg


class SAXSViewerPlugin(ImageView, QWidgetPlugin):
    def __init__(self, header: NonDBHeader = None, field: str = 'primary', *args, **kwargs):

        # Add q axes
        self.axesItem = PlotItem()
        self.axesItem.setLabel('bottom', u'q (Å⁻¹)')  # , units='s')
        self.axesItem.setLabel('left', u'q (Å⁻¹)')
        self.axesItem.axes['left']['item'].setZValue(10)
        self.axesItem.axes['top']['item'].setZValue(10)
        if 'view' not in kwargs: kwargs['view'] = self.axesItem

        super(SAXSViewerPlugin, self).__init__()
        ImageView.__init__(self, *args, **kwargs)
        self.axesItem.invertY(False)

        # Setup axes reset button
        self.resetAxesBtn = QPushButton('Reset Axes')
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.resetAxesBtn.sizePolicy().hasHeightForWidth())
        self.resetAxesBtn.setSizePolicy(sizePolicy)
        self.resetAxesBtn.setObjectName("resetAxes")
        self.ui.gridLayout.addWidget(self.resetAxesBtn, 2, 1, 1, 1)
        self.resetAxesBtn.clicked.connect(self.autoRange)

        # Setup LUT reset button
        self.resetLUTBtn = QPushButton('Reset LUT')
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.resetLUTBtn.sizePolicy().hasHeightForWidth())
        # self.resetLUTBtn.setSizePolicy(sizePolicy)
        # self.resetLUTBtn.setObjectName("resetLUTBtn")
        self.ui.gridLayout.addWidget(self.resetLUTBtn, 3, 1, 1, 1)
        self.resetLUTBtn.clicked.connect(self.autoLevels)

        # Hide ROI button and rearrange
        self.ui.roiBtn.setParent(None)
        self.ui.gridLayout.addWidget(self.ui.menuBtn, 1, 1, 1, 1)
        self.ui.gridLayout.addWidget(self.ui.graphicsView, 0, 0, 3, 1)

        # Setup coordinates label
        self.coordinatesLbl = QLabel('--COORDINATES WILL GO HERE--')
        self.ui.gridLayout.addWidget(self.coordinatesLbl, 3, 0, 1, 1, alignment=Qt.AlignHCenter)

        # Use Viridis by default
        self.setPredefinedGradient('viridis')

        # Shrink LUT
        self.getHistogramWidget().setMinimumWidth(10)

        # Set header
        if header: self.setHeader(header, field)

    def quickMinMax(self, data):
        """
        Estimate the min/max values of *data* by subsampling. MODIFIED TO USE THE 99TH PERCENTILE instead of max.
        """
        while data.size > 1e6:
            ax = np.argmax(data.shape)
            sl = [slice(0, 1)] + [slice(None)] * (data.ndim - 1)
            sl[ax] = slice(None, None, 2)
            data = data[sl]
        return np.nanmin(data), np.nanpercentile(data, 99)

    def setHeader(self, header: NonDBHeader, field: str, *args, **kwargs):
        self.header = header
        # make lazy array from document
        data = None
        try:
            data = header.meta_array(field)
        except IndexError:
            msg.logMessage('Header object contained no frames with field ''{field}''.', msg.ERROR)

        if data:
            kwargs['transform'] = QTransform(0, -1, 1, 0, 0, data.shape[-2])
            super(SAXSViewerPlugin, self).setImage(img=data, *args, **kwargs)
