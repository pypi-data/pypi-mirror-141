# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from mo.front.common.partial_infer.utils import mark_input_bins
from mo.utils.graph import Node
from mo.utils.ir_reader.extender import Extender


class GRUCell_extender(Extender):
    op = 'GRUCell'

    @staticmethod
    def extend(op: Node):
        if not op.has_valid('activations'):
            op['activations'] = None

        mark_input_bins(op, start_port=2)

        op['need_copy_input_blobs'] = True
