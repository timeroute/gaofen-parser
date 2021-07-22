from .base import BaseSatellite


class GF5Satellite(BaseSatellite):
    """
    高分五号遥感卫星
    """

    def pre_parse(self, tar):
        """
        预解析
        """
        if self.sensor_id == 'AHSI':
            member_image_name = "{}/{}.Browse.jpg".format(
                self.base_name, self.base_name)
            member_xml_name = "{}/{}.Meta.xml".format(
                self.base_name, self.base_name)
        elif self.sensor_id == 'VIMS':
            member_image_name = "{}.jpg".format(self.base_name)
            member_xml_name = "{}.XML".format(self.base_name)
        else:
            print('预解析为空')
            return
        member_image = tar.getmember(member_image_name)
        # image 为解压后的图片文件
        self.image = tar.extractfile(member_image)
        member_xml = tar.getmember(member_xml_name)
        # data 为解压并解析后的字典数据
        self.data = self.xmltodict(
            tar.extractfile(member_xml).read())
        self.parse()

    def parse(self):
        if self.sensor_id == 'VIMS':
            self.meta = self.parse_method_four()
        elif self.sensor_id == 'AHSI':
            self.meta = self.parse_method_three()
