# ImageCaptioner

## 缘起

手机里存了大量的照片，是一个美好的回忆，值得保存。但时间久了，可能很难回忆起当时的心境和情绪状态，因此为照片添加文字说明是很有必要的。我想到的方法有：更改文件名，但不适合太长或者有特殊符号的描述；在照片上直接标注文字，但会损失照片的完整性，不适合后期的应用；用一个表格记录每张照片对应的内容，但操作麻烦，需要手动输入文件路径，照片一旦移动，还需要更新表格。

## 我的需求

1. 可视化界面，可以在查看照片的同时，输入文字说明
2. 在照片下方添加一个区域，显示图片内容
3. 操作简单，用户除了输入文字内容外，无需进行其他操作

## 我的思路

1. 设计界面布局，首先实现照片查看器的功能
2. 用一个函数将输入的文字转成图片
3. 将文字标注与原始图片进行纵向拼接，得到标注后的图片
4. 为适应不同的图片大小，要能更改字号大小（单位：像素）和字体颜色
5. 为适应不同的显示器大小，要能更改图片的显示宽度
6. 代码要简单，所以基于Python实现，可以充分利用第三方库的功能

## 实现效果

软件界面

![image](https://github.com/nwuLiucy/ImageCaptioner/assets/53895985/24e6da3f-927d-4b68-af9b-c0b431d63bd5)

标注后的效果，可以调节字号和字体颜色

![2703654249_A_cat_with_a_scarf_sits_next_to_a_radiator_on_artstation_HQ](https://github.com/nwuLiucy/ImageCaptioner/assets/53895985/00b4b833-e137-4204-bd25-2e2b9835e313)

![2703654249_A_cat_with_a_scarf_sits_next_to_a_radiator_on_artstation_HQ](https://github.com/nwuLiucy/ImageCaptioner/assets/53895985/d5ac2391-fe5c-45e7-b98d-57a56de8e227)

