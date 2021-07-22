from .base import BaseSatellite


class GF1CSatellite(BaseSatellite):
    """
    高分一号C遥感卫星
    """

    def parse(self):
        """
        解析
        """
        self.meta = self.parse_method_one()
