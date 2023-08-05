# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from mo.front.extractor import FrontExtractorOp
from mo.front.onnx.extractors.utils import onnx_attr


class ImageScalerFrontExtractor(FrontExtractorOp):
    op = 'ImageScaler'
    enabled = True

    @classmethod
    def extract(cls, node):
        dst_type = lambda x: np.array(x)

        scale = onnx_attr(node, 'scale', 'f', default=np.array(1.0), dst_type=dst_type)
        bias = onnx_attr(node, 'bias', 'floats', default=None, dst_type=dst_type)

        # Expand dims for bias in case if it is not scalar
        if bias.ndim != 0:
            broadcast_dims_cnt = 2 if node.graph.graph['layout'] == 'NCHW' else 0
            for idx in range(broadcast_dims_cnt):
                bias = np.expand_dims(bias, axis=-1)

        node['scale'] = scale
        node['bias'] = bias

        return cls.enabled