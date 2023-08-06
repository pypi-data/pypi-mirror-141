# Copyright 2021 AI Singapore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Displays a tag on bounding box
"""

from typing import Any, Dict

from peekingduck.pipeline.nodes.draw.utils.bbox import draw_tags
from peekingduck.pipeline.nodes.draw.utils.constants import TOMATO
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """Draws tags above bounding boxes.

    The ``draw.tag`` node uses the ``bboxes`` and ``obj_tags`` predictions from
    ``dabble`` nodes and models to draw the tags of the bboxes onto the image.

    Inputs:
        |img|

        |bboxes|

        |obj_tags|

    Outputs:
        |none|

    Configs:
        None.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Draws a tag above each bounding box.

        Args:
            inputs (dict): Dictionary with keys "bboxes", "obj_tags", "img".

        Returns:
            outputs (dict): Dictionary with keys "none".
        """
        draw_tags(inputs["img"], inputs["bboxes"], inputs["obj_tags"], TOMATO)

        return {}
