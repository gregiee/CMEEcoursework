# install dependencies: (use cu101 because colab has CUDA 10.1)
!pip install -U torch==1.5 torchvision==0.6 -f https://download.pytorch.org/whl/cu101/torch_stable.html 
!pip install pyyaml==5.1 pycocotools>=2.0.1
import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
!gcc --version
# opencv is pre-installed on colab
# install detectron2:
!pip install detectron2==0.1.3 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/index.html

# You may need to restart your runtime prior to this, to let your installation take effect
# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import cv2
import random
from google.colab.patches import cv2_imshow
import torch, torchvision

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import os
import numpy as np
import json
from detectron2.structures import BoxMode
from detectron2.utils.visualizer import ColorMode
from detectron2.data.datasets import register_coco_instances
from detectron2.data import DatasetCatalog, MetadataCatalog, build_detection_test_loader, build_detection_train_loader, DatasetMapper
import detectron2.data.transforms as T
import random

import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

register_coco_instances("iznik_train1", {}, "/content/drive/My Drive/iznik/iznik/ite1/train/train.json", "/content/drive/My Drive/iznik/iznik/ite1/train/images")
register_coco_instances("iznik_val1", {}, "/content/drive/My Drive/iznik/iznik/ite1/val/val.json", "/content/drive/My Drive/iznik/iznik/ite1/val/images")

register_coco_instances("iznik_train2", {}, "/content/drive/My Drive/iznik/iznik/ite2/train/train.json", "/content/drive/My Drive/iznik/iznik/ite2/train/images")
register_coco_instances("iznik_val2", {}, "/content/drive/My Drive/iznik/iznik/ite2/val/val.json", "/content/drive/My Drive/iznik/iznik/ite2/val/images")

register_coco_instances("iznik_train3", {}, "/content/drive/My Drive/iznik/iznik/ite3/train/train.json", "/content/drive/My Drive/iznik/iznik/ite3/train/images")
register_coco_instances("iznik_val3", {}, "/content/drive/My Drive/iznik/iznik/ite3/val/val.json", "/content/drive/My Drive/iznik/iznik/ite3/val/images")

iznik_metadata_t = MetadataCatalog.get("iznik_train")
dataset_dict_t = DatasetCatalog.get("iznik_train")
iznik_metadata_v = MetadataCatalog.get("iznik_val")
dataset_dict_v = DatasetCatalog.get("iznik_val")

for d in dataset_dict_t:
    path = d["file_name"]
    file_name = str(path).split("/")[-1]
    print("-------------")
    print(file_name)
    img = cv2.imread(path)
    visualizer = Visualizer(img[:, :, ::-1], 
                                metadata=iznik_metadata_t, 
                                scale=.5,
                                )
    vis = visualizer.draw_dataset_dict(d)
    # cv2_imshow(vis.get_image()[:, :, ::-1])
    plt.imshow(vis.get_image()[:, :, ::-1])
    plt.savefig(f"/content/drive/My Drive/iznik/iznik/ite2/checkgt/train/{file_name}", dpi=300)

for d in dataset_dict_v:
  path = d["file_name"]
  file_name = str(path).split("/")[-1]
  print("-------------")
  print(file_name)
  img = cv2.imread(path)
  visualizer = Visualizer(img[:, :, ::-1], 
                              metadata=iznik_metadata_v, 
                              scale=.5,
                              )
  vis = visualizer.draw_dataset_dict(d)
  # cv2_imshow(vis.get_image()[:, :, ::-1])
  plt.imshow(vis.get_image()[:, :, ::-1])
  plt.savefig(f"/content/drive/My Drive/iznik/iznik/ite2/checkgt/val/{file_name}", dpi=300)


  from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg, CfgNode

import os
os.chdir("/content/drive/My Drive/iznik/iznik/")
path = os.getcwd()
print(path)
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("iznik_train3",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
# cfg.MODEL.WEIGHTS = "/content/drive/My Drive/iznik/iznik/out_ite2/model_0019999.pth"  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 4
cfg.SOLVER.BASE_LR = 0.020 # pick a good LR
cfg.SOLVER.MAX_ITER = 25000  # 300 iterations seems good enough for this toy dataset; you may need to train longer for a practical dataset
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512   # faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3 
cfg.OUTPUT_DIR = "/content/drive/My Drive/iznik/iznik/out_ite4"
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

from detectron2.data import build_detection_train_loader
from detectron2.data import transforms as T
from detectron2.data import detection_utils as utils
import copy
def custom_mapper(dataset_dict):
    # Implement a mapper, similar to the default DatasetMapper, but with your own customizations
    dataset_dict = copy.deepcopy(dataset_dict)  # it will be modified by code below
    image = utils.read_image(dataset_dict["file_name"], format="BGR")
    transform_list = [T.ResizeShortestEdge(short_edge_length=(640, 672, 704, 736, 768, 800), max_size=1333, sample_style='choice'),
                      T.RandomFlip(horizontal=True, vertical=False),
                      T.RandomRotation(angle=[-180,180], expand=True, center=None, sample_style="range", interp=None),
                      ]
    image, transforms = T.apply_transform_gens(transform_list, image)
    dataset_dict["image"] = torch.as_tensor(image.transpose(2, 0, 1).astype("float32"))

    annos = [
        utils.transform_instance_annotations(obj, transforms, image.shape[:2])
        for obj in dataset_dict.pop("annotations")
    ]
    instances = utils.annotations_to_instances(annos, image.shape[:2])
    dataset_dict["instances"] = utils.filter_empty_instances(instances)
    return dataset_dict


# use this dataloader instead of the default
class CTrainer(DefaultTrainer):
    @classmethod
    def build_test_loader(cls, cfg: CfgNode, dataset_name):
      return build_detection_test_loader(cfg, dataset_name, mapper=custom_mapper)

    @classmethod
    def build_train_loader(cls, cfg: CfgNode):
      return build_detection_train_loader(cfg, mapper=custom_mapper)

      # trainer = CTrainer(cfg) 
trainer = DefaultTrainer(cfg) 
# False if starting from coco, True if starting from finetunned ones, or doing inference using trained weights
trainer.resume_or_load(resume=False)

trainer.train()

# Look at training curves in tensorboard:
%load_ext tensorboard
%reload_ext tensorboard
path = os.getcwd()
print(path)
%cd out_ite4
%tensorboard --logdir .

from detectron2.evaluation import COCOEvaluator, inference_on_dataset, DatasetEvaluator
from detectron2.data import build_detection_test_loader
cfg.MODEL.WEIGHTS = os.path.join("/content/drive/My Drive/iznik/iznik/out_ite4", "model_final.pth")
cfg.OUTPUT_DIR = "/content/drive/My Drive/iznik/iznik/out_ite4"
# cfg.MODEL.ROI_HEADS.IOU_THRESHOLDS = [1] # defualt(trainer.model set to .5), coco deal with various bands of iou, so kinda useless
cfg.MODEL.ROI_HEADS.PROPOSAL_APPEND_GT = True
cfg.DATASETS.TEST = ("iznik_val3")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0  # defualt(trainer.model set to .05)
predictor = DefaultPredictor(cfg)
evaluator = COCOEvaluator("iznik_val3", cfg, False, output_dir=cfg.OUTPUT_DIR)
val_loader = build_detection_test_loader(cfg, "iznik_val3")

inference_on_dataset(predictor.model, val_loader, evaluator)

iznik_metadata_v = MetadataCatalog.get("iznik_val")
dataset_dicts_v = DatasetCatalog.get("iznik_val")

for d in random.sample(rhodos_dict, 3):    
    im = cv2.imread(d["file_name"])
    path = d["file_name"]
    file_name = str(path).split("/")[-1]
    print(file_name)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=rhodos_metadata, 
                   scale=0.3, 
                   instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
    )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2_imshow(v.get_image()[:, :, ::-1])
    # plt.imshow(v.get_image()[:, :, ::-1])
    # plt.savefig(f"/content/drive/My Drive/iznik/iznik/rhodos/img0/{file_name}", dpi=300)

    for d in rhodos_dict:
    im = cv2.imread(d["file_name"])
    path = d["file_name"]
    file_name = str(path).split("/")[-1]
    print(file_name)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=rhodos_metadata, 
                   scale=0.5, 
                   instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
    )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    # cv2_imshow(v.get_image()[:, :, ::-1])
    plt.imshow(v.get_image()[:, :, ::-1])
    plt.savefig(f"/content/drive/My Drive/iznik/iznik/rhodos/img0/{file_name}", dpi=300)