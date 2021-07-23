from os import replace
from .base import BaseSatellite


class GF3Satellite(BaseSatellite):
    """
    高分三号遥感卫星
    """

    def get_base_meta(self):
        names = self.base_name.split('_')
        self.satellite_id = names[0]
        self.sensor_id = names[2]
        self.resolution = self.get_resolution()

    def pre_parse(self, tar):
        """
        预解析
        """
        self.names = tar.getnames()
        replaced_names = ['HH', 'VV', 'HV', 'VH', 'DH']
        if self.sensor_id in ['SL', 'UFS', 'FSI', 'FSII', 'SS', 'QPSI', 'QPSII', 'NSC', 'WSC', 'WAV', 'GLO', 'EXT']:
            base_names = self.base_name.split('_')
            self.image_name = None
            for name in replaced_names:
                base_names[8] = name
                self.image_name = "{}.jpg".format('_'.join(base_names))
                if self.image_name in self.names:
                    # 该文件存在压缩包里
                    break
            if not self.image_name:
                print("图片文件不存在")
                return
            self.xml_name = "{}.meta.xml".format(self.base_name)
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
        tar.close()
        self.parse()

    def parse(self):
        self.meta = self.parse_method_two()
