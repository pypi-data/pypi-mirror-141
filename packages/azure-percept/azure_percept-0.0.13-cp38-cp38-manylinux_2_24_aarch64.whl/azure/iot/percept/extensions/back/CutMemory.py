# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from extensions.ops.parameter import Parameter
from mo.back.replacement import BackReplacementPattern
from mo.graph.graph import Graph
from mo.ops.crop import Crop
from mo.utils.logger import log


class CutMemoryInput(BackReplacementPattern):
    """
    Cut Memory layers and have inputs/outputs in graph instead of them
    """
    enabled = True
    graph_condition = [lambda graph: graph.graph['fw'] == "kaldi" and graph.graph['cmd_params'].remove_memory]
    force_clean_up = True

    @staticmethod
    def pattern():
        return dict(
            nodes=[
                ('op', dict(kind='op', op='ReadValue'))],
            edges=[]
        )

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        node = match['op']
        node_id = node['variable_id']

        i = 0
        node.in_port(0).disconnect()
        for dest in node.out_port(0).get_destinations():
            new_in = Parameter(graph, {'name': "Parameter_"+str(i)+"_for_"+node_id,
                                       'shape': dest.data.get_shape()}).create_node()
            i += 1
            dest.disconnect()
            new_in.out_port(0).connect(dest)
            log.error("Add input/output mapped {} -> {} ".format(new_in.name, "Result_for_"+node_id),
                      extra={'is_warning': True})


class CutMemoryOutput(BackReplacementPattern):
    """
    Cut Memory layers and have inputs/outputs in graph instead of them
    """
    enabled = True
    graph_condition = [lambda graph: graph.graph['fw'] == "kaldi" and graph.graph['cmd_params'].remove_memory]
    force_clean_up = True

    @staticmethod
    def pattern():
        return dict(
            nodes=[
                ('op', dict(kind='op', op='Assign'))],
            edges=[]
        )

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        node = match['op']
        node_id = node['variable_id']

        out_node_port = node.out_port(0).get_destination()
        in_node_port = node.in_port(0).get_source()
        node.in_port(0).disconnect()
        node.out_port(0).disconnect()
        crop = Crop(graph, {'name': 'Result_for_'+node_id, 'dim': np.array([1]), 'offset': np.array([0]),
                            'axis': np.array([0])}).create_node()
        in_node_port.connect(crop.in_port(0))
        crop.out_port(0).connect(out_node_port)
