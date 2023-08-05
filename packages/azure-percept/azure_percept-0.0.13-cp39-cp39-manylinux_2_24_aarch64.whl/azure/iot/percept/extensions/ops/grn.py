# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from mo.front.common.partial_infer.elemental import copy_shape_infer
from mo.graph.graph import Graph
from mo.ops.op import Op


class GRNOp(Op):
    op = 'GRN'

    def __init__(self, graph: Graph, attrs: dict):
        mandatory_props = {
            'type': __class__.op,
            'op': __class__.op,
            'version': 'opset1',
            'in_ports_count': 1,
            'out_ports_count': 1,
            'infer': copy_shape_infer
        }
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
            'bias'
        ]
