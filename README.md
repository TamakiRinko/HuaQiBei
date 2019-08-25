# 注释

`不考虑用户分类，目前未考虑训练集与测试集`

## 训练集

* **GenerateFundList**: 生成基金编号和类型
* **CreateData**: 生成用户购买记录

## 爬取属性

* **GenerateAttrs**: 爬取基金属性
* **GenerateEigen**: 数字化属性并使用Z-score标准化，生成基金属性csv

## 评分矩阵

* **CreatePoint_csv**: 生成用户评分csv
* **ReadPoint_csv**: 标准化评分矩阵，并与基金属性一同生成用户喜好属性csv

## 推荐及更新

* **Recommend**: 根据新基金属性选择用户进行推荐

## 基金列表及属性

* 各种生成的文件
