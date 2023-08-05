# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import logging as log

from extensions.middle.ConstSwitchResolver import ConstSwitchEraser
from mo.graph.graph import Graph
from mo.middle.passes.eliminate import remove_op_node_with_data_node
from mo.middle.replacement import MiddleReplacementPattern


class UselessMergeEraser(MiddleReplacementPattern):
    enabled = True

    def run_after(self):
        return [ConstSwitchEraser]

    def run_before(self):
        from extensions.middle.pass_separator import MiddleFinish
        return [MiddleFinish]

    def pattern(self):
        return dict(
            nodes=[('merge', dict(kind='op', op='Merge'))],
            edges=[]
        )

    def replace_pattern(self, graph: Graph, match: dict):
        if len(graph.in_edges(match['merge'].id)) <= 1:
            remove_op_node_with_data_node(graph, match['merge'], list(match['merge'].in_nodes().values())[0])
            log.info("Useles Merge op and data nodes was deleted op='{}'".format(match['merge'].id))
