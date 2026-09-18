# Photo Organizer

A Python coursework project exploring web scraping, photo organization, image processing, CSV generation, multithreading, and data visualization.

## Overview

This project demonstrates several Python techniques through a small photo-management workflow.

The project retrieves photo-related information from a web page, organizes files into directories based on photographer and category, processes images, generates CSV data, and visualizes photo statistics.

## Main Components

### Web Scraping

Uses `Requests` and `BeautifulSoup` to retrieve and parse photo-related information from StockSnap.

The extracted information includes:

- Photo titles
- Photographer names
- Photo categories

### File Organization

Creates a directory structure based on photographer and category:

<pre>Photos/
└── Photographer/
    └── Category/
</pre>

### Image Processing

Uses Pillow to resize and compress images.

### CSV Generation

Stores photo information in CSV format, including:

- Title
- Photographer
- Tags
- Image URL

### Multithreading

Uses Python's `threading` module and a `Lock` to demonstrate concurrent CSV processing and synchronized file access.

### Data Visualization

Uses Matplotlib to visualize the number of photographs by category and photographer.

### Technologies

- Python
- Requests
- BeautifulSoup
- Pillow
- Matplotlib
- CSV
- Threading

### Project Context

This project was developed as part of my undergraduate Computer Engineering coursework at Shiraz University of Technology.

### Status

Completed university coursework project.
