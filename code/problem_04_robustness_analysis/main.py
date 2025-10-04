# -*- coding: utf-8 -*-
from src.sensitivity_analysis import sensitivity_analysis
from src.plot_utils import plot_comparison

if __name__ == "__main__":
    results = sensitivity_analysis()
    plot_comparison(results)
