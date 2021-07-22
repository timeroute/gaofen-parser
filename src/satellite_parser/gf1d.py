from .base import BaseSatellite


class GF1DSatellite(BaseSatellite):
    """
    高分一号D遥感卫星
    """

    def parse(self):
        """
        解析
        """
        self.meta = self.parse_method_one()
