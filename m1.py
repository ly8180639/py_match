import torch

print(torch.__version__)          # 输出 PyTorch 版本

print(torch.cuda.is_available())  # 应返回 True

print(torch.cuda.get_device_name(0))  # 输出 GPU 型号