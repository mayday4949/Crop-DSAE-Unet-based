# Importing PyTorch and checking its version

import sys
import torch
import torch.cuda as cuda
print(torch.__version__)
print(cuda.is_available())

device = torch.device('cuda')

d = torch.tensor([1,2,3], dtype = torch.float32, 
                 device = device, requires_grad = True)

print(d.shape)
print(d.dtype)
print(d.device)
print(d.requires_grad)
# Output:Python版本
print(sys.version)