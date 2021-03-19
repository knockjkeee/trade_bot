import ctypes
import clr

lib = ctypes.cdll.LoadLibrary("dll/txmlconnector64.dll")
print(lib)