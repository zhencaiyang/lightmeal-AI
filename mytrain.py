# food101_convert.py
import os
import shutil
from pathlib import Path

# ===================== 配置项（修改这里！）=====================
# 1. 你的Food-101原始数据根目录（解压后的文件夹）
FOOD101_RAW_ROOT = r"G:\ultralytics-main\datasets\food-101\food-101"
# 2. 转换后YOLO格式数据的保存路径（自定义）
YOLO_DATA_ROOT = r"G:\ultralytics-main\datasets\food-101\food101_yolo_format"
# 3. 是否只复制少量数据（快速测试：True；完整训练：False）
FAST_TEST = True


# =============================================================


def check_raw_data():
    """检查原始数据是否完整."""
    required_paths = [
        os.path.join(FOOD101_RAW_ROOT, "images"),
        os.path.join(FOOD101_RAW_ROOT, "meta", "train.txt"),
        os.path.join(FOOD101_RAW_ROOT, "meta", "test.txt"),
    ]
    for path in required_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"原始数据缺失：{path}")
    print("✅ 原始数据检查通过！")


def copy_images(txt_path, split_dir, max_num=None):
    """复制指定txt中的图片到目标目录."""
    with open(txt_path, encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            # 拆分 类别/图片ID
            cls_name, img_id = line.split("/")
            # 源图片路径
            src_img = os.path.join(FOOD101_RAW_ROOT, "images", cls_name, f"{img_id}.jpg")
            # 目标目录+路径
            dst_cls_dir = os.path.join(split_dir, cls_name)
            Path(dst_cls_dir).mkdir(parents=True, exist_ok=True)
            dst_img = os.path.join(dst_cls_dir, f"{img_id}.jpg")

            # 复制图片（跳过不存在的）
            if os.path.exists(src_img):
                shutil.copy(src_img, dst_img)

            # 快速测试：限制复制数量
            if FAST_TEST and max_num and idx >= max_num:
                break

    print(f"✅ {split_dir} 复制完成（共{idx + 1}张）")


if __name__ == "__main__":
    try:
        # 1. 检查原始数据
        check_raw_data()

        # 2. 创建YOLO格式根目录
        Path(YOLO_DATA_ROOT).mkdir(parents=True, exist_ok=True)

        # 3. 复制训练集（train）
        train_txt = os.path.join(FOOD101_RAW_ROOT, "meta", "train.txt")
        train_dir = os.path.join(YOLO_DATA_ROOT, "train")
        copy_images(train_txt, train_dir, max_num=80000 if FAST_TEST else None)

        # 4. 复制验证集（val）
        val_txt = os.path.join(FOOD101_RAW_ROOT, "meta", "test.txt")
        val_dir = os.path.join(YOLO_DATA_ROOT, "val")
        copy_images(val_txt, val_dir, max_num=80000 if FAST_TEST else None)

        # 5. 输出结果
        train_cls_num = len(os.listdir(train_dir))
        val_cls_num = len(os.listdir(val_dir))
        print("\n🎉 数据集转换完成！")
        print(f"📁 YOLO格式数据路径：{YOLO_DATA_ROOT}")
        print(f"📊 训练集类别数：{train_cls_num} | 验证集类别数：{val_cls_num}")

    except Exception as e:
        print(f"❌ 转换失败：{e!s}")
