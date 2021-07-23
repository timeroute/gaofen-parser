from .base import BaseSatellite


class GF1Satellite(BaseSatellite):
    """
    高分一号遥感卫星
    """

    def exists(self, added_name):
        for name in self.names:
            if added_name in name:
                return True
        return False

    def pre_parse(self, tar):
        """
        预解析
        """
        self.names = tar.getnames()
        if self.sensor_id.startswith('PMS'):
            added_name = 'MSS1' if self.sensor_id == 'PMS1' else 'MSS2'
            if not self.exists(added_name):
                # MSS 不存在时，使用 PAN
                added_name = 'PAN1' if self.sensor_id == 'PMS1' else 'PAN2'
                if not self.exists(added_name):
                    print("MSS 和 PAN 都不存在")
                    return
            self.image_name = "{}-{}.jpg".format(self.base_name, added_name)
            self.xml_name = "{}-{}.xml".format(self.base_name, added_name)
        elif self.sensor_id.startswith('WFV'):
            self.image_name = "{}.jpg".format(self.base_name)
            self.xml_name = "{}.xml".format(self.base_name)
        else:
            print('预解析为空')
            return
        member_image = tar.getmember(self.image_name)
        # image 为解压后的图片文件
        self.image = tar.extractfile(member_image).read()
        member_xml = tar.getmember(self.xml_name)
        # data 为解压并解析后的字典数据
        self.data = self.xmltodict(
            tar.extractfile(member_xml).read())
        self.parse()

    def parse(self):
        """
        解析
        """
        self.meta = self.parse_method_one()
