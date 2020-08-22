import numpy as np
def rotate(V, theta, axis='x'):
  '''Rotate a vector `V` `theta` degrees around axis `axis`'''
  c = np.cos(theta)
  s = np.sin(theta)
  if axis == 'x': return np.dot(np.array([
    [1,   0,  0],
    [0 ,  c,  s],
    [0 , -s,  c]
  ]) , V)
  elif axis == 'y': return np.dot(np.array([
    [c,  0,  -s],
    [0,  1,   0],
    [s,  0,   c]
  ]), V)
  elif axis == 'z': return np.dot(np.array([
    [c, -s,  0 ],
    [s,  c,  0 ],
    [0,  0,  1.],
  ]), V)
    
theta = 0.5*np.pi
v = np.array([[0], [0], [1]])
axis = 'x'
print("Original vector")
print(v)
print("\n") 
print("Rotated vector")
r = rotate(v, theta, axis)
print(r)