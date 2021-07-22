from .base import BaseSatellite


class GF4Satellite(BaseSatellite):
    """
    高分四号遥感卫星
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
        if self.sensor_id == 'IRS':
            self.image_name = "{}.jpg".format(self.base_name)
            self.xml_name = "{}.xml".format(self.base_name)
        elif self.sensor_id == 'PMI':
            added_name = 'PMS'
            if not self.exists(added_name):
                added_name = 'IRS'
                if not self.exists(added_name):
                    print("PMS 和 IRS 都不存在")
                    return
            self.image_name = "{}.jpg".format(
                self.base_name.replace("PMI", added_name))
            self.xml_name = "{}.xml".format(
                self.base_name.replace("PMI", added_name))
        else:
            print('预解析为空')
            return
        member_image = tar.getmember(self.image_name)
        # image 为解压后的图片文件
        self.image = tar.extractfile(member_image)
        member_xml = tar.getmember(self.xml_name)
        # data 为解压并解析后的字典数据
        self.data = self.xmltodict(
            tar.extractfile(member_xml).read())
        self.parse()

    def parse(self):
        self.meta = self.parse_method_one()
