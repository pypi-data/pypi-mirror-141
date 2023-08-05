# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from mo.front.extractor import FrontExtractorOp
from mo.ops.roipooling import ROIPooling


class ROIPoolingFrontExtractor(FrontExtractorOp):
    op = 'roipooling'
    enabled = True

    @classmethod
    def extract(cls, node):
        param = node.pb.roi_pooling_param
        attrs =  {
            'pooled_h': param.pooled_h,
            'pooled_w': param.pooled_w,
            'spatial_scale': param.spatial_scale,
        }
        
        ROIPooling.update_node_stat(node, attrs)
        return cls.enabled
