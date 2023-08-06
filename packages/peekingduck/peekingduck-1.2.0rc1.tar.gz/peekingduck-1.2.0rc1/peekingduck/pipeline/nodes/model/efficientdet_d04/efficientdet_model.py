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
EfficientDet model with model types: D0-D4
"""

import logging
from typing import Any, Dict, List, Tuple

import numpy as np

from peekingduck.pipeline.nodes.model.efficientdet_d04.efficientdet_files.detector import (
    Detector,
)
from peekingduck.weights_utils import checker, downloader, finder


class EfficientDetModel:
    """EfficientDet model with model types: D0-D4"""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__()

        self.logger = logging.getLogger(__name__)

        # check threshold values
        if not 0 <= config["score_threshold"] <= 1:
            raise ValueError("score_threshold must be in [0, 1]")
        if not 0 <= config["model_type"] <= 4:
            raise ValueError("model_type must be an integer in [0, 4]")

        weights_dir, model_dir = finder.find_paths(
            config["root"], config["weights"], config["weights_parent_dir"]
        )

        # check for efficientdet weights, if none then download into weights folder
        if not checker.has_weights(weights_dir, model_dir):
            self.logger.info("---no weights detected. proceeding to download...---")
            downloader.download_weights(weights_dir, config["weights"]["blob_file"])
            self.logger.info(f"---weights downloaded to {weights_dir}.---")

        self.detect_ids = config["detect_ids"]
        self.logger.info(f"efficientdet model detecting ids: {self.detect_ids}")

        self.detector = Detector(config, model_dir)

    def predict(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """predict the bbox from frame

        returns:
        object_bboxes(np.ndarray): list of bboxes detected
        object_labels(np.ndarray): list of index labels of the
            object detected for the corresponding bbox
        object_scores(np.ndarray): list of confidence scores of the
            object detected for the corresponding bbox
        """
        assert isinstance(frame, np.ndarray)

        # return bboxes, object_bboxes, object_labels, object_scores
        return self.detector.predict_bbox_from_image(frame, self.detect_ids)

    def get_detect_ids(self) -> List[int]:
        """getter function for ids to be detected"""
        return self.detect_ids
