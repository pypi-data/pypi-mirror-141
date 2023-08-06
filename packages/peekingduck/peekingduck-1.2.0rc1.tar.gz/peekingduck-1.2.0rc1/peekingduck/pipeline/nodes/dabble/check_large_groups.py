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
Checks if number of objects in a group exceeds a threshold.
"""

from collections import Counter
from typing import Any, Dict, List

from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """Checks which groups have exceeded the group size threshold.

    Inputs:
        |obj_groups|

    Outputs:
        |large_groups|

    Configs:
        group_size_thres (:obj:`int`): **default = 5**. |br|
            Threshold of group size.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, List[int]]) -> Dict[str, List[int]]:
        """Checks which groups have exceeded the group size threshold,
        and returns a list of such groups.
        """
        group_counter = Counter(inputs["obj_groups"])
        large_groups = [
            group
            for group in group_counter
            if group_counter[group] > self.group_size_thres
        ]

        return {"large_groups": large_groups}
