import pytest
from src.main import plot_to_image
import matplotlib.pyplot as plt

def test_plot_to_image():
    plt.plot([1, 2, 3], [4, 5, 6], label='Test Line')
    title = "Test Plot"
    market_cap = 100.5
    
    image = plot_to_image(plt, title, market_cap)
    
    assert image is not None
    assert image.format == 'PNG'
    assert image.size != (0, 0)
