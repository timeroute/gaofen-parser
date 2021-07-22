from .base import BaseSatellite


class GF1BSatellite(BaseSatellite):
    """
    高分一号B遥感卫星
    """

    def parse(self):
        """
        解析
        """
        self.meta = self.parse_method_one()
