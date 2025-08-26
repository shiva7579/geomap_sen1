Sentinel-1 Change Detection Web Application

Overview:
This web application allows users to select a geographic area and date range to access Sentinel-1 satellite imagery and perform change detection analysis. The system provides real-time feedback and processed images highlighting changes between pre-incident and post-incident periods.

Frontend:
Built using Vite for modern frontend development.
MapLibre is used for rendering basemaps and layers.
Users input area and date ranges; valid inputs redirect to the results page, while user get alerted abput invalid inputs.
A span box (default value: 12) allows users to extend the search period, ensuring images are found even if a single date fails and helping reduce speckle noise in the imagery.

Backend:
Developed with Flask, which also hosts the frontend.
Provides real-time updates to users via Server-Sent Events (SSE) during processing.
Fetches Sentinel-1 imagery using the Google Earth Engine (GEE) API.

Preprocessing & Logic:(under development,not added to repository)
Focuses on speckle noise removal and thermal noise reduction, assuming orbital correction and radiometric calibration are already applied by GEE.
Processes only VH and VV bands of the images.
Each band undergoes noise removal, followed by calculation of median images for pre-incident and post-incident periods.
The final output presents four images highlighting change detection between the respective bands.

I am testing different different speckle noise removal alogorithim and chnage detection algorithm to obtain optimum result. its still underdevelopment. To check functinality , please clone this repo.


