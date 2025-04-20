import torch 
from ultralytics import YOLO

model = YOLO('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/best.pt') 
dummy_input = torch.randn(1,  3, 150, 60)  # 输入尺寸需匹配训练配置 
torch.onnx.export(model,  dummy_input, "yolov11.onnx", 
                  opset_version=13,  # OpenCV4.5+需≥11 
                  input_names=['images'],
                  output_names=['output'],
                  dynamic_axes={'images': {0: 'batch'}, 'output': {0: 'batch'}})