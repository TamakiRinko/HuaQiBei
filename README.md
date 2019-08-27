# README

`不考虑用户分类，目前未考虑训练集与测试集`  
`训练集中CreateData.py，评分矩阵中CreatePoint_csv.py，CreatePoint_list.py，ReadJudge.py代码由lsm同学完成！`

***
8/27:

* 根据软院方面给出的数据修改文件读写和处理部分代码，提供有购买记录的旧基金和无购买记录的新基金
* 解决爬取过程中的引用问题，解决了内存占用过高及由其引发的bug
* 增加多线程爬取

***

## 训练集

* **GenerateFundList**: 生成基金编号和类型
* **CreateData**: 生成用户购买记录

## 爬取属性

* **GenerateAttrs**: 爬取基金属性
* **GenerateEigen**: 数字化属性并使用Z-score标准化，生成基金属性csv
* **GenerateAttrs_Thread**：多线程爬取基金属性

## 评分矩阵

* **CreatePoint_csv**: 生成用户评分csv
* **ReadPoint_csv**: 标准化评分矩阵，并与基金属性一同生成用户喜好属性csv

## 推荐及更新

* **Recommend**: 根据新基金属性选择用户进行推荐

## 基金列表及属性

* 各种生成的文件
