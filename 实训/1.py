import importlib
import subprocess
import sys

# 定义需要检查的依赖库列表
required_libraries = ['paddlepaddle', 'numpy', 'matplotlib', 'ipykernel']

# 检查并安装缺失的库
for library in required_libraries:
    try:
        importlib.import_module(library)
        print(f"{library} 已经安装。")
    except ImportError:
        print(f"{library} 未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(f"{library} 安装成功。")
        except subprocess.CalledProcessError as e:
            print(f"安装 {library} 时出错: {e}")

import paddle
from paddle.vision.transforms import Compose, Normalize, RandomHorizontalFlip
from paddle.metric import Accuracy
import numpy as np
import matplotlib.pyplot as plt
from paddle.io import DataLoader

# 移除RandomErasing，仅保留水平翻转
train_transform = Compose([
    Normalize(mean=[127.5], std=[127.5], data_format='CHW'),
    RandomHorizontalFlip(prob=0.4)
])
test_transform = Compose([Normalize(mean=[127.5], std=[127.5], data_format='CHW')])

# 导入数据
from paddle.vision.datasets import FashionMNIST
train_dataset = FashionMNIST(mode='train', transform=train_transform)
test_dataset = FashionMNIST(mode='test', transform=test_transform)

# 构建dataloader，打乱训练集
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True, num_workers=0)
test_loader = DataLoader(test_dataset, batch_size=256, shuffle=False, num_workers=0)

# 设置标签含义，对应数据集中的类别序号
label_list = ['t-shirt', 'trouser', 'pullover', 'dress', 'coat','sandal','shirt','sneaker', 'bag', 'ankleboot']

# 查看数据集中的图片
train_data0, train_label_0 = train_dataset[5][0], train_dataset[5][1]
train_data0 = train_data0.reshape([28, 28])
plt.figure(figsize=(2, 2))
plt.imshow(train_data0)
plt.show()
print('train_data0 label is:' + str(label_list[train_label_0[0]]))

# 三层MLP，极低Dropout，保留BN
class MultilayerPreceptron(paddle.nn.Layer):
    def __init__(self):
        super(MultilayerPreceptron, self).__init__()
        self.h1 = paddle.nn.Linear(784, 512)
        self.bn1 = paddle.nn.BatchNorm1D(512)
        self.relu1 = paddle.nn.ReLU()
        self.drop1 = paddle.nn.Dropout(0.1)

        self.h2 = paddle.nn.Linear(512, 256)
        self.bn2 = paddle.nn.BatchNorm1D(256)
        self.relu2 = paddle.nn.ReLU()
        self.drop2 = paddle.nn.Dropout(0.1)

        self.h3 = paddle.nn.Linear(256, 128)
        self.bn3 = paddle.nn.BatchNorm1D(128)
        self.relu3 = paddle.nn.ReLU()
        self.drop3 = paddle.nn.Dropout(0.1)
        self.out = paddle.nn.Linear(128, 10)

    def forward(self, x):
        x = paddle.flatten(x, start_axis=1, stop_axis=-1)
        x = self.drop1(self.relu1(self.bn1(self.h1(x))))
        x = self.drop2(self.relu2(self.bn2(self.h2(x))))
        x = self.drop3(self.relu3(self.bn3(self.h3(x))))
        x = self.out(x)
        return x

# 实例化模型
model = paddle.Model(MultilayerPreceptron())

# 超参优化
EPOCH_NUM = 50
base_lr = 0.001
# 权重衰减进一步降低
optim = paddle.optimizer.Adam(
    learning_rate=base_lr,
    parameters=model.parameters(),
    weight_decay=5e-5
)

# 模型配置
model.prepare(
    optim,
    paddle.nn.CrossEntropyLoss(),
    Accuracy()
)

# 训练
model.fit(
    train_loader,
    test_loader,
    epochs=EPOCH_NUM,
    verbose=1
)

# 保存训练好的模型
model.save('work', training=True)

# 模型评估
eval_result = model.evaluate(test_loader, verbose=1)
print("测试集完整评估结果：", eval_result)

# 模型预测
test_result = model.predict(test_dataset, batch_size=1)
for i in range(0, 5):
    index = np.argmax(test_result[0][i][0])
    print(f"第{i+1}张预测类别：{label_list[index]}")

# 可视化前5张图
plt.figure(figsize=(15, 3))
for i in range(5):
    img, label = test_dataset[i]
    pred_label = np.argmax(test_result[0][i][0])
    plt.subplot(1, 5, i+1)
    plt.imshow(img[0], cmap='gray')
    plt.axis('off')
    plt.title(f'True:{label_list[label[0]]}\nPred:{label_list[pred_label]}', fontsize=9)
plt.tight_layout()
plt.show()