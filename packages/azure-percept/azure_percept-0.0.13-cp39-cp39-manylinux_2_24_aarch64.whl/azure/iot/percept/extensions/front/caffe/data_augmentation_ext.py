# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from extensions.ops.data_augmentation import DataAugmentationOp
from mo.front.caffe.collect_attributes import merge_attrs
from mo.front.caffe.extractors.utils import embed_input
from mo.front.extractor import FrontExtractorOp


class DataAugmentationFrontExtractor(FrontExtractorOp):
    op = 'DataAugmentation'
    enabled = True

    @classmethod
    def extract(cls, node):
        proto_layer = node.pb
        param = proto_layer.augmentation_param
        # slice_dim is deprecated parameter and is used as alias for axis
        # however if slice_dim is defined and axis is default, we use slice_dim
        update_attrs = {
            'crop_width': param.crop_width,
            'crop_height': param.crop_height,
            'write_augmented': param.write_augmented,
            'max_multiplier': param.max_multiplier,
            'augment_during_test': int(param.augment_during_test),
            'recompute_mean': param.recompute_mean,
            'write_mean': param.write_mean,
            'mean_per_pixel': int(param.mean_per_pixel),
            'mean': param.mean,
            'mode': param.mode,
            'bottomwidth': param.bottomwidth,
            'bottomheight': param.bottomheight,
            'num': param.num,
            'chromatic_eigvec': param.chromatic_eigvec
        }

        mapping_rule = merge_attrs(param, update_attrs)

        if node.model_pb:
            for index in range(0, len(node.model_pb.blobs)):
                embed_input(mapping_rule, index + 1, 'custom_{}'.format(index), node.model_pb.blobs[index].data)

        # update the attributes of the node
        DataAugmentationOp.update_node_stat(node, mapping_rule)
        return cls.enabled
