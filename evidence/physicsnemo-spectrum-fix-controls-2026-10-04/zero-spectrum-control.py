"""Deliberately invalid spectrum: symmetric output alone must not pass a fix."""
import torch


def power_spectrum(x):
    return torch.zeros(2), torch.zeros(2)
