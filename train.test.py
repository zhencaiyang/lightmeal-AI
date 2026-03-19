from ultralytics import YOLO

model =YOLO(r"yolov8n.pt")#打算使用哪一个模型来预测
model.predict(
    source=r"ultralytics/assets",#预测目标文件的位置，这一部分的图片或视频可以进行替换，写0的话是用于预测摄像头（按Q退出）
    save=False,#True=保存一下预测结果
    show=True,#False=不用立刻显示结果
    line_width=8,
)