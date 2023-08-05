# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from mo.front.extractor import FrontExtractorOp
from extensions.ops.activation_ops import SoftPlus


class SoftPlusExtractor(FrontExtractorOp):
    op = 'Softplus'
    enabled = True

    @classmethod
    def extract(cls, node):
        SoftPlus.update_node_stat(node, {})
        return cls.enabled
