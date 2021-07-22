from .base import BaseSatellite


class GF7Satellite(BaseSatellite):
    """
    高分七号遥感卫星
    """

    def pre_parse(self, tar):
        """
        预解析
        """
        if self.sensor_id == 'APD' or self.sensor_id == 'DLC':
            member_image_name = "{}_FP1-1.jpg".format(self.base_name)
            member_xml_name = "{}.xml".format(self.base_name)
        else:
            print('Pre Parse None')
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
        self.meta = self.parse_method_one()
