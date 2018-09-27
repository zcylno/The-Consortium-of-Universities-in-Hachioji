import torch
t = torch.Tensor([[1,2,3,4]])
z = t.gather(1, torch.LongTensor([[0,1, 3,0]]))


print(z)








t = torch.Tensor([[-1.0000,  1.0000, -0.9952,  1.0000],
        [-1.0000,  1.0000, -0.9956,  1.0000]])
        
a = torch.LongTensor([ [1], [1]] )
         
z = t.gather(1, a)


print(z)