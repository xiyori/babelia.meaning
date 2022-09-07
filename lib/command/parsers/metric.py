from .base import BaseParser
from lib.math_utils import metrics


class MetricParser(BaseParser):
    def __init__(self):
        super(MetricParser, self).__init__(
            name="metric",
            mapping={"l1": metrics.L1Metric(),
                     "l2": metrics.L2Metric(),
                     "linf": metrics.LInfMetric(),
                     "cos": metrics.CosMetric()},
            default=metrics.L2Metric(),
            shortened=False
        )
