# 遥感卫星数据解析

## 依赖

xmltodict

## 说明

本程序为遥感卫星原始数据解析，作为内部使用

### 类名

- GF1Satellite 高分一号数据处理类
- GF2Satellite 高分二号数据处理类
- GF3Satellite 高分三号数据处理类
- GF4Satellite 高分四号数据处理类
- GF5Satellite 高分五号数据处理类
- GF6Satellite 高分六号数据处理类
- GF7Satellite 高分七号数据处理类
- GF1BSatellite 高分一号B数据处理类
- GF1CSatellite 高分一号C数据处理类
- GF1DSatellite 高分一号D数据处理类
- SV101Satellite 高景一号01数据处理类
- SV102Satellite 高景一号02数据处理类
- SV103Satellite 高景一号03数据处理类
- SV104Satellite 高景一号04数据处理类

### 类变量

- file_name 文件名
- file_path 文件路径
- ext 文件后缀名
- satellite_id 星源 ID
- sensor_id 传感器 ID
- resolution 分辨率
- image 图片对象
- meta 解析 xml 后转换成 字典对象
  - satellite_id
  - sensor_id
  - receive_time
  - scene_id
  - product_id
  - product_level
  - product_format
  - produce_time
  - bands
  - resolution
  - cloud_percent
  - geometry Polygon Geometry 格式

## API

### 初始化类

```python

from satellite_parser import GF1Satellite

file_name = 'GF1_PMS1_E114.6_N22.7_20181006_L1A0003680028.tar.gz'
file_path = '/data/GF1_PMS1_E114.6_N22.7_20181006_L1A0003680028.tar.gz'
try:
    satellite = GF1Satellite(file_name, file_path)
    print(satellite.meta)
except Exception as e:
    print(e)
```

### 生成NID

generate_nid

```python

from satellite_parser import GF1Satellite

file_name = 'GF1_PMS1_E114.6_N22.7_20181006_L1A0003680028.tar.gz'
file_path = '/data/GF1_PMS1_E114.6_N22.7_20181006_L1A0003680028.tar.gz'
try:
    satellite = GF1Satellite(file_name, file_path)
    print(satellite.generate_nid())
except Exception as e:
    print(e)
```

## 更新日志

- v0.1 目前仅支持读取高分系列卫星
- v0.2 新增高景卫星处理类
