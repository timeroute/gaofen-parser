"""
遥感卫星基类
"""
import tarfile
import zipfile
from random import sample
import xmltodict
from datetime import datetime
from .constants import RESOLUTION, SATELLITE_ALIAS, SENSOR_ALIAS


class BaseSatellite(object):
    """
    遥感卫星基类
    """

    def __init__(self, name, path) -> None:
        self.file_name = name
        self.file_path = path
        self.ext = 'tar' if name.endswith('.tar.gz') else 'zip'
        self.base_name = name.replace('.tar.gz', '').replace('.zip', '')
        self.get_base_meta()
        self.unzip()

    def get_resolution(self):
        return RESOLUTION[self.satellite_id][self.sensor_id]

    def get_base_meta(self):
        """
        通过 base_name 获取基本元信息
        包含 星源ID 和 传感器ID 两个参数，同时获取 分辨率
        """
        names = self.base_name.split('_')
        self.satellite_id = names[0]
        self.sensor_id = names[1]
        self.resolution = self.get_resolution()

    def unzip(self):
        """
        解压缩
        """
        if self.ext == 'tar':
            with tarfile.open(self.file_path) as tar:
                self.pre_parse(tar)
        else:
            with zipfile.ZipFile(self.file_path, 'r') as zip:
                self.pre_parse(zip)

    def xmltodict(self, content):
        return xmltodict.parse(content)

    def pre_parse(self, tar):
        """
        预解析，将 image 和 xml 文件提取
        """
        self.image_name = "{}.jpg".format(self.base_name)
        member_image = tar.getmember(self.image_name)
        # image 为解压后的图片文件
        self.image = tar.extractfile(member_image)
        self.xml_name = "{}.xml".format(self.base_name)
        member_xml = tar.getmember(self.xml_name)
        # data 为解压并解析后的字典数据
        self.data = self.xmltodict(
            tar.extractfile(member_xml).read())
        tar.close()
        self.parse()

    def parse(self):
        """
        解析，将 xml 内容解析成字典数据
        """
        pass

    def generate_nid(self):
        """
        生成自定义景号
        """
        return "{}-{}-{}-{}".format(
            SATELLITE_ALIAS[self.satellite_id],
            SENSOR_ALIAS[self.sensor_id],
            self.meta['produce_time'].strftime('%Y%M%d'),
            ''.join(sample('qwertyuiopasdfghjklzxcvbnm1234567890', 3))
        )

    def parse_method_one(self):
        """通用解析方法 1

        适用于高分1、2、4、6、7号卫星数据格式

        Returns:
            解析后的参数字典
        """
        meta = self.data['ProductMetaData']
        return {
            'satellite_id': self.satellite_id,
            'sensor_id': self.sensor_id,
            'receive_time': datetime.strptime(meta['ReceiveTime'][:10], '%Y-%m-%d'),
            'scene_id': meta['SceneID'],
            'product_id': meta['ProductID'],
            'product_level': meta['ProductLevel'],
            'product_format': meta['ProductFormat'],
            'produce_time': datetime.strptime(meta['ProduceTime'][:10], '%Y-%m-%d'),
            'bands': meta['Bands'],
            'resolution': self.resolution,
            'cloud_percent': meta['CloudPercent'],
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     [float(meta['BottomRightLongitude']),
                     float(meta['BottomRightLatitude'])],
                     [float(meta['TopRightLongitude']),
                     float(meta['TopRightLatitude'])],
                     [float(meta['TopLeftLongitude']),
                     float(meta['TopLeftLatitude'])],
                     [float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     ]]
            }
        }

    def parse_method_two(self):
        """通用解析方法 2

        适用于高分3号卫星数据格式

        Returns:
            解析后的参数字典
        """
        meta = self.data['product']
        top_left = meta['imageinfo']['corner']['topLeft']
        top_right = meta['imageinfo']['corner']['topRight']
        bottom_left = meta['imageinfo']['corner']['bottomLeft']
        bottom_right = meta['imageinfo']['corner']['bottomRight']
        return {
            'satellite_id': self.satellite_id,
            'sensor_id': self.sensor_id,
            'receive_time': None if meta['ReceiveTime'] == 'NULL' else datetime.strptime(meta['ReceiveTime'][:10], '%Y-%m-%d'),
            'scene_id': meta['sceneID'],
            'product_id': meta['productID'],
            'product_level': meta['productinfo']['productLevel'],
            'product_format': meta['productinfo']['productFormat'],
            'produce_time': datetime.strptime(meta['productinfo']['productGentime'][:10], '%Y-%m-%d'),
            'resolution': self.resolution,
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[float(bottom_left['longitude']),
                     float(bottom_left['latitude'])],
                     [float(bottom_right['longitude']),
                     float(bottom_right['latitude'])],
                     [float(top_right['longitude']),
                     float(top_right['latitude'])],
                     [float(top_left['longitude']),
                     float(top_left['latitude'])],
                     [float(bottom_left['longitude']),
                     float(bottom_left['latitude'])],
                     ]]
            }
        }

    def parse_method_three(self):
        """通用解析方法 3

        适用于高分5号卫星 AHSI 数据格式

        Returns:
            解析后的参数字典
        """
        meta = self.data['ProductMetaData']
        return {
            'satellite_id': self.satellite_id,
            'sensor_id': self.sensor_id,
            'receive_time': datetime.strptime(meta['StartTime'][:10], '%Y-%m-%d'),
            'scene_id': meta['SceneID'],
            'product_id': meta['ProductID'],
            'product_level': meta['ProductLevel'],
            'product_format': meta['ProductFormat'],
            'produce_time': datetime.strptime(meta['ProduceTime'][:10], '%Y-%m-%d'),
            'bands': meta['BandsID'],
            'resolution': self.resolution,
            'cloud_percent': meta['CloudPercent'],
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     [float(meta['BottomRightLongitude']),
                     float(meta['BottomRightLatitude'])],
                     [float(meta['TopRightLongitude']),
                     float(meta['TopRightLatitude'])],
                     [float(meta['TopLeftLongitude']),
                     float(meta['TopLeftLatitude'])],
                     [float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     ]]
            }
        }

    def parse_method_four(self):
        """通用解析方法 4

        适用于高分5号卫星 VIMS 数据格式

        Returns:
            解析后的参数字典
        """
        meta = self.data['ProductMetaData']
        return {
            'satellite_id': self.satellite_id,
            'sensor_id': self.sensor_id,
            'receive_time': datetime.strptime(meta['StartTime'][:10], '%Y-%m-%d'),
            'scene_id': meta['SceneID'],
            'product_id': meta['ProductID'],
            'product_level': meta['ProductLevel'],
            'product_format': meta['ProductFormat'],
            'produce_time': datetime.strptime(meta['ProduceTime'][:10], '%Y-%m-%d'),
            'bands': meta['Bands'],
            'resolution': self.resolution,
            'cloud_percent': meta['CloudPercent'],
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     [float(meta['BottomRightLongitude']),
                     float(meta['BottomRightLatitude'])],
                     [float(meta['TopRightLongitude']),
                     float(meta['TopRightLatitude'])],
                     [float(meta['TopLeftLongitude']),
                     float(meta['TopLeftLatitude'])],
                     [float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     ]]
            }
        }

    def parse_method_five(self):
        """通用解析方法 5

        适用于高景卫星数据格式

        Returns:
            解析后的参数字典
        """
        meta = self.data['ProductMetaData']
        return {
            'satellite_id': self.satellite_id,
            'sensor_id': self.sensor_id,
            'receive_time': datetime.strptime(meta['ReceiveTime'][:10], '%Y-%m-%dT%H:%M:%S'),
            'scene_id': meta['SceneID'],
            'product_id': meta['ProductID'],
            'product_level': meta['ProductLevel'],
            'product_format': meta['ProductFormat'],
            'produce_time': datetime.strptime(meta['ProduceTime'][:10], '%Y-%m-%d'),
            'bands': meta['Bands'],
            'resolution': self.resolution,
            'cloud_percent': meta['CloudPercent'],
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     [float(meta['BottomRightLongitude']),
                     float(meta['BottomRightLatitude'])],
                     [float(meta['TopRightLongitude']),
                     float(meta['TopRightLatitude'])],
                     [float(meta['TopLeftLongitude']),
                     float(meta['TopLeftLatitude'])],
                     [float(meta['BottomLeftLongitude']),
                     float(meta['BottomLeftLatitude'])],
                     ]]
            }
        }
