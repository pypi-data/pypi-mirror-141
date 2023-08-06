import torch
import numpy as np

def to_float_tensor(item): return item.float().div_(255.)
def add_colour_dimension(item):
    if item.dim() == 4:
        if item.shape[1] in [1,3]: # batch, channels, size, size
            return item
        elif item.shape[3] in [1,3]:  # batch, size, size, channels
            return item.permute(0,3,1,2)
    if item.dim() == 3:
        if item.shape[0] in [1,3]: # channels, size, size
            return item
        elif item.shape[2] in [1,3]: # size, size, channels
            return item.permute(2,0,1)
        else: return item.unsqueeze(1) # batch, size, size
    else: return item.unsqueeze(0) # size, size

def recursive_np_or(boolean_arrays):
    if len(boolean_arrays) == 1: return boolean_arrays[0]
    return np.logical_or(boolean_arrays[0],recursive_np_or(boolean_arrays[1:]))

def recursive_np_and(boolean_arrays):
    if len(boolean_arrays) == 1: return boolean_arrays[0]
    return np.logical_and(boolean_arrays[0],recursive_np_and(boolean_arrays[1:]))

def noiseify(pytensor,constant):
    noise = torch.randn_like(pytensor)
    noise /= noise.max()
    return pytensor + noise*constant

def oheify(x):
    target_category = torch.argmax(x, dim=1)
    ohe_target = (torch.arange(x.shape[1]).to(x.device) == target_category[:,None])[:,:,None,None].float()
    return target_category, ohe_target

def numpyify(x):
    if isinstance(x,np.ndarray): return x
    elif isinstance(x,list): return np.array(x)
    elif torch.is_tensor(x): return x.detach().cpu().numpy()

def mean_off_diagonal(mat):
    upper_sum = np.triu(mat,1).sum()
    lower_sum = np.tril(mat,-1).sum()
    num_el = np.prod(mat.shape) - mat.shape[0]
    return (upper_sum + lower_sum)/num_el

def cudify(x): return torch.tensor(x,device='cuda')

def print_tensors(*tensors):
    """Only works for one-element tensors"""
    print(*[t.item() for t in tensors])
