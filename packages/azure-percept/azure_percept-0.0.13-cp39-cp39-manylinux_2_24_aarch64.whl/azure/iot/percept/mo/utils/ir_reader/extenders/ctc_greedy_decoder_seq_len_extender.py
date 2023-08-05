# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from mo.middle.passes.convert_data_type import destination_type_to_np_data_type
from mo.utils.graph import Node
from mo.utils.ir_reader.extender import Extender


class CTCGreedyDecoderSeqLenExtender(Extender):
    op = 'CTCGreedyDecoderSeqLen'

    @staticmethod
    def extend(op: Node):
        if op.has_valid('classes_index_type'):
            op['classes_index_type'] = destination_type_to_np_data_type(op.classes_index_type)
        if op.has_valid('sequence_length_type'):
            op['sequence_length_type'] = destination_type_to_np_data_type(op.sequence_length_type)
