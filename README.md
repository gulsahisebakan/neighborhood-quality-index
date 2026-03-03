# 🏙️ Neighborhood Quality-of-Life Index

> An interactive data analytics tool that scores and ranks neighborhoods across safety, schools, transit, air quality, walkability and green space — with a configurable weighting system and real map visualization.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red?logo=streamlit)
![Folium](https://img.shields.io/badge/Folium-Maps-green?logo=leaflet)
![Plotly](https://img.shields.io/badge/Plotly-6.6-darkblue?logo=plotly)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

This project builds a neighborhood livability scoring engine. It generates realistic multi-factor data for 15 neighborhoods, calculates composite livability scores using a configurable weighted model, and presents everything in an interactive Streamlit dashboard with a real Folium map.

This mirrors the kind of analysis done by real estate platforms like Zillow and Redfin, urban planning departments, and city governments every day.

---

## 🧠 How It Works

### 1. `generate_data.py` — Data Generation
- Generates 15 neighborhoods with realistic scores across 6 factors
- Factors: Crime Safety, School Quality, Transit Access, Air Quality, Walkability, Green Space
- Calculates composite livability scores using default weights
- Saves output to `neighborhoods.csv`

### 2. `dashboard.py` — Interactive Streamlit Dashboard
- **Interactive Folium map** — colored circles represent livability scores, click for details
- **Configurable weight sliders** — adjust how much each factor matters, rankings update instantly
- **Livability rankings** bar chart with red→green color gradient
- **Radar chart** — visual factor profile for any selected neighborhood
- **Head-to-head comparison** — compare any two neighborhoods across all factors with winner column
- **Full data table** with all scores and median home prices

---

## 📊 Key Features

| Feature | Description |
|---------|-------------|
| 🗺️ Interactive Map | Real geographic map with color-coded neighborhood circles |
| ⚖️ Weight Customizer | Adjust factor importance — rankings update in real time |
| 📡 Radar Chart | Visual factor profile for any neighborhood |
| ⚖️ Comparison Tool | Side-by-side neighborhood comparison with winner highlights |
| 🏠 Home Price | Median home price correlated with livability score |

---

## 🛠️ Technology Stack

| Tool | Purpose |
|------|---------|
| **Python 3.14** | Core programming language |
| **Pandas & NumPy** | Data generation and transformation |
| **Streamlit** | Interactive dashboard framework |
| **Folium** | Interactive map visualization |
| **Plotly** | Charts — bar, radar, comparison |
| **streamlit-folium** | Embeds Folium maps in Streamlit |

---

## ⚙️ Installation & Setup
```bash
# 1. Clone the repository
git clone https://github.com/gulsahisebakan/neighborhood-quality-index.git
cd neighborhood-quality-index

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate neighborhood data
python generate_data.py

# 5. Launch the dashboard
python -m streamlit run dashboard.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure
```
neighborhood-quality-index/
├── generate_data.py      # Generates neighborhood scores dataset
├── dashboard.py          # Interactive Streamlit + Folium dashboard
├── neighborhoods.csv     # Generated neighborhood data
├── requirements.txt      # Dependencies
└── README.md
```

---

## 💡 What I Learned

- Building configurable **weighted scoring models**
- **Geospatial data visualization** with Folium and interactive maps
- Creating **radar charts** for multi-dimensional data profiling
- Designing **user-configurable analytics tools** with real-time updates
- Combining multiple chart types into a cohesive analytical dashboard

---

## 🔮 Future Improvements

- [ ] Connect to real public datasets (Census, EPA, crime APIs)
- [ ] Add more cities beyond Chicago
- [ ] Include rent price trends over time
- [ ] Add a "Find My Perfect Neighborhood" quiz feature
- [ ] Deploy to Streamlit Cloud

---

## 📄 License
MIT License
