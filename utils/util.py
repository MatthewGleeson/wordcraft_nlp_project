import torch
import os
from kge.model import KgeModel
from kge.util.io import load_checkpoint

def load_checkpoint_model(checkpoint_fpath):
    checkpoint = load_checkpoint(checkpoint_fpath)
    model = KgeModel.create_from(checkpoint)
    return model