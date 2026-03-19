# food101_train.py
import os

from ultralytics import YOLO

# ===================== 配置项（修改这里！）=====================
# 1. 转换后的YOLO格式数据路径（和脚本1的YOLO_DATA_ROOT一致）
YOLO_DATA_ROOT = r"G:\ultralytics-main\datasets\food-101\food101_yolo_format"
# 2. 训练结果保存路径
TRAIN_RESULT_DIR = r"G:\ultralytics-main\datasets\food-101\food101_train_results"
# 3. 训练参数
EPOCHS = 5  # 训练轮数（快速测试：5；完整训练：20）
BATCH_SIZE = 2  # 批次大小（低配电脑改1）
IMG_SIZE = 128  # 图片尺寸（快速测试：128；完整训练：224）
DEVICE = 0  # 有GPU改"0"，无GPU保留cpu


# =============================================================


def check_yolo_data():
    """检查YOLO格式数据是否完整."""
    required_dirs = [os.path.join(YOLO_DATA_ROOT, "train"), os.path.join(YOLO_DATA_ROOT, "val")]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"YOLO数据缺失：{dir_path}")
    print("✅ YOLO格式数据检查通过！")


if __name__ == "__main__":
    try:
        # 1. 检查数据
        check_yolo_data()

        # 2. 加载YOLOv8分类模型（必须带-cls）
        model = YOLO("yolov8n-cls.pt")
        print("✅ 模型加载完成！")

        # 3. 开始训练
        print("\n🚀 开始训练...")
        results = model.train(
            data=YOLO_DATA_ROOT,
            task="classify",  # 明确指定分类任务
            epochs=EPOCHS,
            batch=BATCH_SIZE,
            imgsz=IMG_SIZE,
            device=DEVICE,
            workers=0,  # Windows必设0，避免多线程报错
            save=True,  # 保存最优模型
            project=TRAIN_RESULT_DIR,
            name="food101_model",  # 模型名称
            verbose=True,  # 显示训练过程
        )

        # 4. 验证模型
        print("\n📊 验证模型精度...")
        metrics = model.val()
        print("✅ 训练完成！")
        print(f"Top1精度（识别正确概率）：{metrics.top1:.2f}")
        print(f"Top5精度（前5猜中概率）：{metrics.top5:.2f}")
        print(f"📁 模型保存路径：{os.path.join(TRAIN_RESULT_DIR, 'food101_model', 'weights', 'best.pt')}")

    except Exception as e:
        print(f"❌ 训练失败：{e!s}")
