# README

`1. 不考虑用户分类，目前未考虑训练集与测试集`  
`2. 余留问题：CreateDataGX生成的用户数量不定，可能超过用户记录中的用户数量；每次生成训练集，爬取数据，耗时长，需与软院协商数据来源问题`  
`3. 使用方式: 保持各文件位置不变，运行 推荐与更新 中的 Recommend.py 即可`  
`4. 训练集中CreateData.py，评分矩阵中CreatePoint_csv.py代码由lsm同学完成！训练集中CreateDataGX.py, 用户画像部分由gx同学完成！`

***

9/3:

* 根据软院提供的数据格式和gx同学提供的训练集生成代码对原本代码进行修改，解决文件空行，基金获取不匹配等多个问题，整体初步完成。

***
8/29：

* 减少文件的产生，解决了DataFrame处理时的index重复问题
* 增强模块间的独立性

***
8/27:

* 根据软院方面给出的数据修改文件读写和处理部分代码，提供有购买记录的旧基金和无购买记录的新基金
* 解决爬取过程中的引用问题，解决了内存占用过高及由其引发的bug
* 增加多线程爬取

***

## 训练集

* **GenerateFundList**: 生成基金编号和类型(**Deprecated**)
* **CreateData**: 生成用户购买记录(**Deprecated**)
* **CreateDataGX**: 根据能够获取到属性的旧基金和用户记录生成购买记录

## 爬取属性

* **GenerateAttrs**: 爬取基金属性(**Deprecated**)
* **GenerateEigen**: 数字化属性并使用Z-score标准化，生成基金属性csv
* **Merge**: 生成需要爬取的基金
* **GenerateAttrs_Thread**：多线程爬取基金属性

## 评分矩阵

* **CreatePoint_csv**: 生成用户评分csv
* **ReadPoint_csv**: 标准化评分矩阵，并与基金属性一同生成用户喜好属性csv
* **Standardization**: 标准化评分矩阵

## 推荐及更新

* **Recommend**: 根据新基金属性选择用户进行推荐

## 基金列表及属性

* 各种生成的文件

## 用户画像

* 与新基金推荐无关
