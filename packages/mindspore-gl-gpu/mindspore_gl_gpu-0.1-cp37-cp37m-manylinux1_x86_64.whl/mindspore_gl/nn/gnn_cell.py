# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""GNN Cell"""
from mindspore.nn import Cell
from ..parser.vcg import translate, set_display_config


class GNNCell(Cell):
    """
    GNN Cell class.

    Construct function will be translated by default.
    """

    def __init__(self):
        super().__init__()
        translate(self, "construct")

    @staticmethod
    def enable_display(screen_width=200):
        """
        Enable display code comparison.

        Args:
            screen_width (int): Determines the screen width on which the code is displayed.
        """
        set_display_config(screen_width, True)

    @staticmethod
    def disable_display():
        """
        Disable display code comparison.
        """
        set_display_config(0, False)
