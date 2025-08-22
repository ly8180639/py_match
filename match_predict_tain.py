# 在 match_predict.py 文件中添加基于PyTorch的神经网络模型
import logging

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from match_predict_dataset import CustomDataLoader
from src.match.db.session import SessionLocal


class MatchDataset(Dataset):
    """
    自定义数据集类
    """
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features.values)
        self.labels = torch.LongTensor(labels.values.flatten())

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

class MatchResultNet(nn.Module):
    """
    比赛结果预测神经网络 (PyTorch版本)
    """
    def __init__(self, input_size, hidden_sizes=[128, 64, 32, 16], num_classes=3):
        """
        初始化网络结构

        Args:
            input_size: 输入特征维度
            hidden_sizes: 隐藏层大小列表
            num_classes: 分类数量
        """
        super(MatchResultNet, self).__init__()

        # 创建网络层
        layers = []
        prev_size = input_size

        # 添加隐藏层
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.BatchNorm1d(hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.3))
            prev_size = hidden_size

        # 输出层
        layers.append(nn.Linear(prev_size, num_classes))

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        """
        前向传播
        """
        return self.network(x)

class PyTorchMatchPredictor:
    """
    基于PyTorch的比赛结果预测器
    """

    def __init__(self, input_dim, device=None):
        """
        初始化预测器

        Args:
            input_dim: 输入特征维度
            device: 计算设备 (CPU或GPU)
        """
        self.input_dim = input_dim
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler = StandardScaler()
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []

    def build_model(self, hidden_sizes=[128, 64, 32, 16], num_classes=3):
        """
        构建神经网络模型

        Args:
            hidden_sizes: 隐藏层大小列表
            num_classes: 分类数量
        """
        self.model = MatchResultNet(self.input_dim, hidden_sizes, num_classes)
        self.model.to(self.device)
        return self.model

    def train(self, X_train, y_train, X_val=None, y_val=None,
              epochs=100, batch_size=32, learning_rate=0.001):
        """
        训练模型

        Args:
            X_train: 训练特征
            y_train: 训练标签
            X_val: 验证特征
            y_val: 验证标签
            epochs: 训练轮数
            batch_size: 批次大小
            learning_rate: 学习率
        """
        # 数据标准化
        X_train_scaled = self.scaler.fit_transform(X_train)

        # 创建数据集和数据加载器
        train_dataset = MatchDataset(X_train_scaled, y_train)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        val_loader = None
        if X_val is not None and y_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            val_dataset = MatchDataset(X_val_scaled, y_val)
            val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        # 定义损失函数和优化器
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)

        # 训练循环
        best_val_loss = float('inf')
        patience_counter = 0
        patience = 10

        for epoch in range(epochs):
            # 训练阶段
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0

            for features, labels in train_loader:
                features, labels = features.to(self.device), labels.to(self.device)

                # 前向传播
                optimizer.zero_grad()
                outputs = self.model(features)
                loss = criterion(outputs, labels)

                # 反向传播
                loss.backward()
                optimizer.step()

                # 统计
                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                train_total += labels.size(0)
                train_correct += (predicted == labels).sum().item()

            avg_train_loss = train_loss / len(train_loader)
            train_accuracy = 100 * train_correct / train_total
            self.train_losses.append(avg_train_loss)
            self.train_accuracies.append(train_accuracy)

            # 验证阶段
            val_loss, val_accuracy = 0.0, 0.0
            if val_loader:
                val_loss, val_accuracy = self._validate(val_loader, criterion)
                self.val_losses.append(val_loss)
                self.val_accuracies.append(val_accuracy)

                # 学习率调度
                scheduler.step(val_loss)

                # 早停机制
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    patience_counter = 0
                    # 保存最佳模型
                    torch.save(self.model.state_dict(), 'best_model.pth')
                else:
                    patience_counter += 1

                if patience_counter >= patience:
                    print(f"Early stopping at epoch {epoch+1}")
                    # 加载最佳模型
                    self.model.load_state_dict(torch.load('best_model.pth'))
                    break

            # 打印进度
            if (epoch + 1) % 10 == 0:
                if val_loader:
                    print(f'Epoch [{epoch+1}/{epochs}], '
                          f'Train Loss: {avg_train_loss:.4f}, '
                          f'Train Acc: {train_accuracy:.2f}%, '
                          f'Val Loss: {val_loss:.4f}, '
                          f'Val Acc: {val_accuracy:.2f}%')
                else:
                    print(f'Epoch [{epoch+1}/{epochs}], '
                          f'Train Loss: {avg_train_loss:.4f}, '
                          f'Train Acc: {train_accuracy:.2f}%')

    def _validate(self, val_loader, criterion):
        """
        验证模型

        Args:
            val_loader: 验证数据加载器
            criterion: 损失函数

        Returns:
            验证损失和准确率
        """
        self.model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for features, labels in val_loader:
                features, labels = features.to(self.device), labels.to(self.device)
                outputs = self.model(features)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = 100 * val_correct / val_total
        return avg_val_loss, val_accuracy

    def predict(self, X):
        """
        预测结果

        Args:
            X: 特征数据

        Returns:
            预测概率
        """
        self.model.eval()
        X_scaled = self.scaler.transform(X)
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)

        with torch.no_grad():
            outputs = self.model(X_tensor)
            probabilities = F.softmax(outputs, dim=1)
            return probabilities.cpu().numpy()

    def predict_classes(self, X):
        """
        预测类别

        Args:
            X: 特征数据

        Returns:
            预测类别
        """
        probabilities = self.predict(X)
        return np.argmax(probabilities, axis=1)

    def evaluate(self, X_test, y_test):
        """
        评估模型

        Args:
            X_test: 测试特征
            y_test: 测试标签
        """
        # 预测
        y_pred = self.predict_classes(X_test)

        # 计算准确率
        accuracy = np.mean(y_pred == y_test.values.flatten())
        print(f"测试集准确率: {accuracy:.4f}")

        # 分类报告
        print("\n分类报告:")
        print(classification_report(y_test, y_pred,
                                  target_names=['负(0)', '平(1)', '胜(3)']))

        # 混淆矩阵
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['负(0)', '平(1)', '胜(3)'],
                    yticklabels=['负(0)', '平(1)', '胜(3)'])
        plt.title('混淆矩阵')
        plt.xlabel('预测标签')
        plt.ylabel('真实标签')
        plt.show()

        return accuracy

    def plot_training_history(self):
        """
        绘制训练历史
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # 损失曲线
        ax1.plot(self.train_losses, label='训练损失')
        if self.val_losses:
            ax1.plot(self.val_losses, label='验证损失')
        ax1.set_title('模型损失')
        ax1.set_xlabel('轮数')
        ax1.set_ylabel('损失')
        ax1.legend()

        # 准确率曲线
        ax1.plot(self.train_accuracies, label='训练准确率')
        if self.val_accuracies:
            ax1.plot(self.val_accuracies, label='验证准确率')
        ax1.set_title('模型准确率')
        ax1.set_xlabel('轮数')
        ax1.set_ylabel('准确率')
        ax1.legend()

        plt.tight_layout()
        plt.show()

    def save_model(self, filepath):
        """
        保存模型

        Args:
            filepath: 模型保存路径
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'scaler': self.scaler,
            'input_dim': self.input_dim
        }, filepath)
        print(f"模型已保存到: {filepath}")

    def load_model(self, filepath):
        """
        加载模型

        Args:
            filepath: 模型保存路径
        """
        checkpoint = torch.load(filepath)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.scaler = checkpoint['scaler']
        self.input_dim = checkpoint['input_dim']
        self.model.to(self.device)
        print(f"模型已从 {filepath} 加载")

# 在 __main__ 部分替换为PyTorch训练代码
if __name__ == '__main__':
    """
    预测比赛结果 (PyTorch版本)
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    db=SessionLocal()
    loader = CustomDataLoader(db)

    # 获取特征和标签
    X, y = loader.get_features_and_labels(60000)

    # 分割数据集：5万为训练数据，1万为测试数据
    from sklearn.model_selection import train_test_split

    # 分割数据集 (80% 训练, 20% 测试)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.17,  # 12000测试, 48000训练
        random_state=42,
        stratify=y
    )

    # 再从训练集中分出验证集 (从训练集中再分出10%作为验证集)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train,
        test_size=0.1,
        # random_state=42,
        stratify=y_train
    )

    print(f"训练集大小: {X_train.shape[0]}")
    print(f"验证集大小: {X_val.shape[0]}")
    print(f"测试集大小: {X_test.shape[0]}")
    print(f"特征维度: {X_train.shape[1]}")

    # 创建并训练模型
    predictor = PyTorchMatchPredictor(input_dim=X_train.shape[1])
    model = predictor.build_model()

    # 显示模型结构
    print("模型结构:")
    print(model)

    # 训练模型
    print("开始训练模型...")
    predictor.train(
        X_train, y_train,
        X_val, y_val,
        epochs=50,
        batch_size=32,
        learning_rate=0.001
    )

    # 绘制训练历史
    predictor.plot_training_history()

    # 评估模型
    print("评估模型...")
    predictor.evaluate(X_test, y_test)

    # 保存模型
    predictor.save_model("match_result_predictor_pytorch.pth")
