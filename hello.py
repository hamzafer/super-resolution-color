import torch
import sys

def check_gpu_usage():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        tensor = torch.rand(3, 3).to(device)
        print(f"Tensor on GPU: {tensor}")
    else:
        print("GPU is not available.")

def check_python_version():
    print(f"Python version: {sys.version}")

def check_cuda():
    if torch.cuda.is_available():
        print(f"CUDA is available. Version: {torch.version.cuda}")
    else:
        print("CUDA is not available.")

def check_cudnn():
    if torch.backends.cudnn.is_available():
        print(f"cuDNN is available. Version: {torch.backends.cudnn.version()}")
    else:
        print("cuDNN is not available.")

def check_torch():
    print(f"PyTorch version: {torch.__version__}")

if __name__ == "__main__":
    check_python_version()
    check_cuda()
    check_cudnn()
    check_torch()
    check_gpu_usage()