from ultralytics import YOLO

# 加载YOLOv8n预训练模型
model = YOLO("yolov8n.pt")

# 开始训练：指定VisDrone数据集配置文件，其他参数和终端一致
results = model.train(
    data="coco8.yaml",  # 你的数据集配置文件路径
    epochs=50,  # 训练轮数
    imgsz=320,  # 输入图片尺寸
    batch=1,  # 批次大小（Windows根据显存调整，8/16均可）
    device=0,  # 使用GPU训练（0为GPU编号，无GPU则写cpu）
)
