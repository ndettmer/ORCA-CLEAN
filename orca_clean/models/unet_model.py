"""
Module: unet_model.py
Authors: Christian Bergler
Institution: Friedrich-Alexander-University Erlangen-Nuremberg, Department of Computer Science, Pattern Recognition Lab
Last Access: 06.02.2021
"""

"""
Code from https://github.com/milesial/Pytorch-UNet
Code modified compared to https://github.com/milesial/Pytorch-UNet
Access Data: 06.02.2021, Last Access Date: 06.02.2021
Full assembly of the parts to form the complete network
"""
from .unet_parts import *

""" Unet-model  """
class UNet(nn.Module):
    def __init__(self, n_channels, n_classes, bilinear=True):
        super(UNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.bilinear = bilinear

        self.inc = DoubleConv(n_channels, 64)

        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        self.down4 = Down(512, 1024)

        self.up1 = Up(1024, 512, bilinear)
        self.up2 = Up(512, 256, bilinear)
        self.up3 = Up(256, 128, bilinear)
        self.up4 = Up(128, 64, bilinear)
        self.outc = OutConv(64, n_classes)

    def forward(self, x):
        #downsampling
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        # bottleneck
        x5 = self.down4(x4)

        #upsampling
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.outc(x)

        #activation function
        return torch.sigmoid(x)

    def transfer_freeze(self, layers=None):
        if layers is None:
            layers = []

        if 'inc' in layers:
            for p in self.inc.parameters():
                p.requires_grad = False

        if 'down1' in layers:
            for p in self.down1.parameters():
                p.requires_grad = False

        if 'down2' in layers:
            for p in self.down2.parameters():
                p.requires_grad = False

        if 'down3' in layers:
            for p in self.down3.parameters():
                p.requires_grad = False

        if 'down4' in layers:
            for p in self.down4.parameters():
                p.requires_grad = False

        if 'up1' in layers:
            for p in self.up1.parameters():
                p.requires_grad = False

        if 'up2' in layers:
            for p in self.up2.parameters():
                p.requires_grad = False

        if 'up3' in layers:
            for p in self.up3.parameters():
                p.requires_grad = False

        if 'up4' in layers:
            for p in self.up4.parameters():
                p.requires_grad = False

        if 'outc' in layers:
            for p in self.outc.parameters():
                p.requires_grad = False
