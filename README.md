# 🛰️ Sentinel-2 Spatial Analysis & Land-Cover Classification

A Python-based remote sensing project using **Sentinel-2 satellite imagery** to derive spectral indicators, perform spatial aggregation with **H3 hexagonal cells**, and classify land cover across a study area in **Kolkata, India**. 🌍📊

The project moves from raw satellite imagery to spectral indices, temporal analysis, spatial feature engineering, and machine-learning-based land-cover classification.

---

## 🎯 Project Objectives

- Work with real Sentinel-2 Level-2A satellite imagery.
- Preprocess and visualize multispectral satellite data.
- Derive:
  - 🌿 **NDVI** for vegetation
  - 💧 **NDWI** for water
  - 🏙️ **NDBI** for built-up characteristics
- Analyse spectral information across multiple observations.
- Represent the study area using **H3 resolution 8** hexagonal cells.
- Aggregate pixel-level information into spatial features.
- Use **ESA WorldCover** as a reference land-cover source.
- Compare **K-Nearest Neighbors (KNN)** and **Random Forest** classifiers.
- Evaluate classification performance using accuracy, precision, recall, F1-score, and confusion matrices.
- Produce an H3-based spatial land-cover prediction map.

---

## 📍 Study Area

The study area is a rectangular **Kolkata, India** AOI approximately bounded by:

- Longitude: **88.25°E to 88.45°E**
- Latitude: **22.50°N to 22.70°N**

The same AOI is used throughout the satellite retrieval, spectral analysis, spatial aggregation, and classification workflow.

---

# 📓 Notebook 1 | Sentinel-2 Data & Preprocessing

> *Problem Statement: How can real Sentinel-2 satellite imagery be accessed, cropped to a defined Kolkata AOI, inspected, and prepared for further remote-sensing analysis using Python?*

### 🔍 What this notebook covers

- Defining the Kolkata Area of Interest (AOI).
- Connecting to the **Microsoft Planetary Computer STAC catalog**.
- Searching for Sentinel-2 Level-2A imagery using date and cloud-cover constraints.
- Selecting and reading Sentinel-2 bands.
- Cropping the imagery to the AOI.
- Inspecting CRS, spatial resolution, and raster dimensions.
- Converting Sentinel-2 values to reflectance.
- Creating a true-colour RGB composite.
- Inspecting the Scene Classification Layer (SCL).

### 🛰️ Main Sentinel-2 bands

| Band | Description | Resolution |
|---|---|---:|
| B02 | Blue | 10 m |
| B03 | Green | 10 m |
| B04 | Red | 10 m |
| B08 | Near Infrared | 10 m |
| B11 | Short-Wave Infrared | 20 m |
| SCL | Scene Classification Layer | 20 m |

---

# 📓 Notebook 2 | Spectral Indices & Temporal Analysis

> *Problem Statement: How can Sentinel-2 spectral bands be transformed into meaningful environmental indicators and used to examine spatial and temporal changes in vegetation, water, and built-up characteristics?*

### 🌱 Spectral indices

**NDVI**

```text
NDVI = (B08 - B04) / (B08 + B04)
```

Used as an indicator of vegetation condition.

**NDWI**

```text
NDWI = (B03 - B08) / (B03 + B08)
```

Used to highlight water-related surface characteristics.

**NDBI**

```text
NDBI = (B11 - B08) / (B11 + B08)
```

Used as an indicator of built-up characteristics.

Since B11 has a native resolution of 20 m while B08 is 10 m, B11 is aligned to the 10 m reference grid before calculating NDBI.

### ⏳ Temporal analysis

Multiple Sentinel-2 observations are used to create a small temporal data cube containing:

- NDVI
- NDWI
- NDBI
- Acquisition dates

NDVI change is then calculated between selected observations to examine spatial patterns of vegetation change.

---

# 📓 Notebook 3 | H3 Spatial Analysis & Machine Learning

> *Problem Statement: How can pixel-level Sentinel-2 information be converted into spatially consistent H3 features and used to classify land cover using supervised machine-learning methods?*

### ⬡ H3 spatial representation

The Kolkata AOI is divided into **H3 resolution 8** hexagonal cells.

Pixel-level information is aggregated to each H3 cell using zonal statistics.

The resulting feature set contains mean values of:

- B02
- B03
- B04
- B08
- B11
- NDVI
- NDWI
- NDBI

This transforms raster-based satellite information into a spatial tabular dataset suitable for machine learning.

---

## 🌍 Reference Land-Cover Labels

**ESA WorldCover 10 m** is used as the reference land-cover source.

WorldCover classes are grouped into four project categories:

| Project Class | Meaning |
|---:|---|
| 1 | 🏙️ Urban |
| 2 | 🌿 Vegetation |
| 3 | 💧 Water |
| 4 | 🟫 Other |

For each H3 cell, the majority WorldCover class is used as the reference label.

> **Important:** These are reference labels derived from WorldCover and should not be interpreted as independent field-validated ground truth.

---

## 🤖 Machine Learning

Two supervised classification models are compared.

### K-Nearest Neighbors

KNN is trained using standardized spectral features because it is distance-based and sensitive to feature scale.

### Random Forest

Random Forest is trained using the spectral features without requiring standardization.

The dataset is divided into training and testing subsets using a stratified split.

---

## 📊 Current Model Results

| Model | Test Accuracy |
|---|---:|
| 🥇 **KNN** | **91.7%** |
| Random Forest | **89.8%** |

### KNN

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Urban | 0.91 | 0.97 | 0.94 |
| Vegetation | 0.94 | 0.86 | 0.90 |
| Water | 0.83 | 0.71 | 0.77 |

### Random Forest

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Urban | 0.94 | 0.91 | 0.92 |
| Vegetation | 0.86 | 0.91 | 0.89 |
| Water | 0.71 | 0.71 | 0.71 |

KNN currently gives the higher overall test accuracy and is used for the final H3 prediction stage.

---

## 🗺️ Spatial Prediction

The selected KNN model is applied across the H3 cells to generate a spatial land-cover classification.

Each predicted H3 cell contains:

- H3 identifier
- Predicted land-cover class
- Predicted land-cover name

The final result is visualized as a hexagonal land-cover classification map.

---

## 🗃️ Repository Structure

```text
sentinel_project/
│
├── notebooks/
│   ├── 01-preprocessing.ipynb
│   ├── 02-indices-temporal.ipynb
│   └── 03-spatial-ml.ipynb
│
├── figures/
│   ├── change in ndvi overtime.png
│   ├── confusion matrices.png
│   ├── h3grid_resolution8.png
│   ├── kolkata sentinel2 rgb.png
│   ├── landcover classification H3 based.png
│   ├── landcover labelling image classification.png
│   ├── median of indices.png
│   └── redband (B04) reflectance.png
│
├── data/
│   ├── kolkata_aoi.gpkg
│   ├── IND_DUG_2026_GRID_L1_R2025A_v1.tif
│   ├── IND_DUG_2026_GRID_L2_R2025A_v1.tif
│   ├── h3_land_cover_predictions.csv
│   └── h3_land_cover_predictions.gpkg
│
├── report/
│   └── # Report updating soon
│
├── utils.py
└── README.md
```

---

## 🧰 Main Technologies & Libraries

- 🐍 Python
- `numpy`
- `pandas`
- `matplotlib`
- `geopandas`
- `rasterio`
- `rasterstats`
- `shapely`
- `h3`
- `pystac-client`
- `planetary-computer`
- `scikit-learn`

Reusable raster and spectral-index functions are maintained in `utils.py`.

---

## 🔬 Methodological Notes

### Spatial aggregation

H3 provides a consistent spatial unit for integrating raster-derived information and machine-learning predictions.

### Resolution alignment

Sentinel-2 bands do not all have the same native resolution. The workflow explicitly aligns 20 m information such as B11 with the 10 m reference grid before combining features.

### Reference labels

WorldCover labels are treated as **reference labels**, rather than independent in-situ ground truth.

### Class distribution

The current classification dataset contains substantially more Urban and Vegetation cells than Water cells. The Water class therefore has fewer test observations, so its class-level metrics should be interpreted cautiously.

---

## ⚠️ Limitations

- The study uses a localized Kolkata AOI.
- WorldCover is used as a reference labeling source rather than field-validated ground truth.
- The Water class has fewer observations than Urban and Vegetation.
- Sentinel-2 observations can be affected by cloud contamination and temporal variability.
- H3 aggregation reduces pixel-level spatial detail.
- Model performance may not generalize to other geographical regions or acquisition periods.

---

## 🚀 Future Work

Possible extensions include:

- Larger and geographically diverse study areas.
- More Sentinel-2 acquisition dates.
- Additional spectral and texture features.
- Improved class balancing.
- Independent validation data.
- Hyperparameter tuning and cross-validation.
- More advanced spatial machine-learning methods.
- Temporal land-cover change analysis.

---

## 📄 Project Report

The project report is **updating soon** and will be added to the `report/` directory. 📝

---

## 👩🏻‍💻 About Me

I am an **MSc Data Science student with a background in Economics**, interested in exploring how data, statistics, machine learning, and geospatial technologies can be combined to understand real-world problems.

My interests include:

- 📊 Data Science & Statistical Analysis
- 🤖 Machine Learning
- 🛰️ Remote Sensing & Geospatial Analytics
- 🌍 Environmental & Spatial Data
- 📈 Data-driven research

This project is part of my exploration of applying computational and statistical methods to spatial and environmental datasets.

---

## 🔗 Connect With Me

I'd love to connect and exchange ideas around data science, machine learning, statistics, and geospatial analytics. 🌱

- 💻 **GitHub:** [Your GitHub Profile](https:/github.com/AbhilashaxData)
- 💼 **LinkedIn:** [Your LinkedIn Profile](www.linkedin.com/in/abhilasha-das-375a95324)

---

## ⭐ Project Status

**Status: Core workflow completed and documentation is being updated.** 🚀

The repository currently contains the analysis notebooks, generated figures, spatial data, reusable utility functions, and model outputs. The project report will be added to the `report/` directory soon.
