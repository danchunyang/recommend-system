# recommend-system
This is a book recommendation system based on Douban reviews
系统架构设计

1.数据层：数据在 HDFS（分布式文件系统）中的存储

2.算法层：建立图书推荐模型，数据层面给出推荐结果

3.逻辑层：数据层面推荐结果转换成前台显示格式、收集用户行为数据

4.应用层：显示图书、用户数据，与用户交互，反馈推荐结果

