from .base import BaseSatellite


class SV101Satellite(BaseSatellite):
    """
    高景一号01遥感卫星
    """

    def get_base_meta(self):
        pass

    def pre_parse(self, zip):
        """
        预解析
        """
        added_name = 'MUX'
        for name in zip.namelist():
            if name.endswith('.tiff') and added_name in name:
                names = name.split('/')
                tiff_name = names[len(names)-1]
                self.tiff_base_name = tiff_name.replace('.tiff', '')
                base_names = tiff_name.split('_')
                self.satellite_id = base_names[0]
                self.sensor_id = added_name
                self.resolution = self.get_resolution()
                break
        self.image_name = "{}/{}.jpg".format(
            self.base_name, self.tiff_base_name)
        self.xml_name = "{}/{}.xml".format(self.base_name,
                                           self.tiff_base_name)
        # image 为解压后的图片文件
        self.image = zip.open(self.image_name, 'r')
        # data 为解压并解析后的字典数据
        self.data = self.xmltodict(
            zip.read(self.xml_name))
        self.parse()

    def parse(self):
        """
        解析
        """
        self.meta = self.parse_method_one()
