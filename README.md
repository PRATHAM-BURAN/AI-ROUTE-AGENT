# 🚚 AI Smart Delivery Route Agent — Pune City Connected Location Graph

An interactive Artificial Intelligence web application built with **Python**, **Streamlit**, and **Plotly**. The application demonstrates how an autonomous delivery robot calculates optimal routes across the **Pune City & PCMC Connected Location Graph** while dynamically detecting and circumventing traffic jams, construction zones, and roadblock hazards.

---

## 🌟 Key Features

1. **Authentic Pune City Connected Graph (36 Locations):**
   - **PCMC & North-West:** Pimpri, Chinchwad, Akurdi, Nigdi, Talegaon, Alandi
   - **West Pune:** Hinjawadi, Wakad, Baner, Balewadi, Aundh, Pashan, Susgaon, Pirangut, Lavale, Bavdhan
   - **Central Pune:** Shivajinagar, Deccan, Pune Railway Station, Erandwane, Kothrud, Swargate
   - **East Pune:** Hadapsar, Magarpatta, Mundhwa, Kharadi, Wagholi, Viman Nagar, Lohegaon, Yerawada
   - **South Pune:** Katraj, Narhe, Warje, Kondhwa, NIBM, Wanowrie

2. **Accurate Road Network & Weighted Graph (56 Corridors):**
   - Graph modeled after the official **Pune City Connected Location Graph** with realistic connectivity and illustrative costs (e.g. Hinjawadi ↔ Wakad: 5, Baner ↔ Balewadi: 4, Shivajinagar ↔ Deccan: 3, Swargate ↔ Hadapsar: 8).
   - Default demonstration route: **Hinjawadi ➔ Hadapsar**.

3. **Three Core AI Pathfinding Algorithms:**
   - **A\* Search:** Informed search using min-heap priority queue and admissible Euclidean lower-bound heuristic ($f(n) = g(n) + h(n)$). Guarantees the lowest total path cost.
   - **Breadth-First Search (BFS):** Uninformed search using FIFO queue. Guarantees finding the route with the minimum number of road hops/edges.
   - **Depth-First Search (DFS):** Uninformed search using LIFO stack. Explores deep branches before backtracking.

4. **Side-by-Side Algorithm Benchmark (BFS vs DFS vs A\*):**
   - Direct comparative table evaluating path cost, number of hops, nodes explored, and run time (ms).
   - Demonstrates why A\* prunes the search space more effectively than blind BFS and DFS.

5. **Dynamic Obstacle & Roadblock Manager:**
   - Block or unblock any of the 56 road segments in real-time.
   - One-click Pune traffic presets (*Clear All*, *Block Central Core*, *River Flood Hazard*, *Random Road*).
   - Graceful fallback notification when road closures isolate destinations.

6. **Modern Dark-Mode Graph Theme:**
   - Interactive Plotly canvas with glowing neon cyan route trajectories, color-coded regional nodes, and `⛔` roadblock indicators.
   - Deploy button removed for clean presentation.
   - Footer attribution for **Pratham** with LinkedIn and GitHub links.

---

## 🏗️ Project Architecture & File Structure

```
ROUTE FINDING AGENT/
├── city_map.py         # Centralized Pune graph: 36 locations, 56 edges & roadblock manager
├── algorithms.py       # Pure Python A*, BFS, DFS implementations & comparative benchmarking
├── app.py              # Modern Streamlit web dashboard & Plotly graph visualization
├── requirements.txt    # Python dependencies (Streamlit, Plotly, Pandas)
└── README.md           # Project documentation, network data & algorithmic theory
```

---

## 📊 Road Network & Starter Edge Weights

| From | Connected To | Illustrative Cost |
| :--- | :--- | :---: |
| **Hinjawadi** | Wakad | 5.0 |
| **Hinjawadi** | Baner | 4.0 |
| **Talegaon** | Hinjawadi | 12.0 |
| **Wakad** | Pimpri | 6.0 |
| **Wakad** | Aundh | 4.0 |
| **Wakad** | Baner | 4.0 |
| **Baner** | Balewadi | 4.0 |
| **Balewadi** | Aundh | 5.0 |
| **Baner** | Aundh | 5.0 |
| **Baner** | Pashan | 6.0 |
| **Susgaon** | Baner | 6.0 |
| **Susgaon** | Pirangut | 7.0 |
| **Pirangut** | Lavale | 8.0 |
| **Pashan** | Aundh | 4.0 |
| **Pashan** | Bavdhan | 6.0 |
| **Bavdhan** | Kothrud | 6.0 |
| **Aundh** | Shivajinagar | 5.0 |
| **Aundh** | Deccan | 5.0 |
| **Shivajinagar** | Deccan | 3.0 |
| **Shivajinagar** | Pune Railway Station | 2.0 |
| **Shivajinagar** | Yerawada | 4.0 |
| **Shivajinagar** | Swargate | 4.0 |
| **Shivajinagar** | Magarpatta | 6.0 |
| **Shivajinagar** | Viman Nagar | 6.0 |
| **Deccan** | Swargate | 4.0 |
| **Deccan** | Kothrud | 7.0 |
| **Kothrud** | Erandwane | 5.0 |
| **Kothrud** | Warje | 5.0 |
| **Erandwane** | Swargate | 4.0 |
| **Swargate** | Hadapsar | 8.0 |
| **Swargate** | Katraj | 8.0 |
| **Swargate** | Kondhwa | 6.0 |
| **Swargate** | Wanowrie | 4.0 |
| **Warje** | Narhe | 7.0 |
| **Narhe** | Katraj | 8.0 |
| **Katraj** | Kondhwa | 6.0 |
| **Kondhwa** | Wanowrie | 4.0 |
| **Kondhwa** | NIBM | 6.0 |
| **Kondhwa** | Hadapsar | 6.0 |
| **Hadapsar** | Mundhwa | 5.0 |
| **Magarpatta** | Mundhwa | 3.0 |
| **Magarpatta** | Hadapsar | 5.0 |
| **Mundhwa** | Kharadi | 4.0 |
| **Kharadi** | Wagholi | 8.0 |
| **Viman Nagar** | Kharadi | 5.0 |
| **Viman Nagar** | Lohegaon | 5.0 |
| **Lohegaon** | Kharadi | 5.0 |
| **Yerawada** | Viman Nagar | 4.0 |
| **Pune Railway Station** | Yerawada | 3.0 |
| **Pimpri** | Chinchwad | 4.0 |
| **Pimpri** | Deccan | 6.0 |
| **Chinchwad** | Akurdi | 3.0 |
| **Chinchwad** | Nigdi | 4.0 |
| **Akurdi** | Nigdi | 4.0 |
| **Akurdi** | Alandi | 12.0 |
| **Akurdi** | Yerawada | 5.0 |

---

## 🧠 Comparison of Search Algorithms (Hinjawadi ➔ Hadapsar)

When planning a delivery route from **Hinjawadi** to **Hadapsar**:

| Algorithm | Discovered Route | Total Cost | Road Hops | Nodes Explored | Optimality |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **A\* Search** | `Hinjawadi` ➔ `Baner` ➔ `Aundh` ➔ `Shivajinagar` ➔ `Magarpatta` ➔ `Hadapsar` | **25.0** | 5 | ~20 | **Optimal Cost** |
| **BFS** | `Hinjawadi` ➔ `Wakad` ➔ `Pimpri` ➔ `Deccan` ➔ `Swargate` ➔ `Hadapsar` | **29.0** | 5 | ~30 | **Fewest Hops** |
| **DFS** | `Hinjawadi` ➔ `Wakad` ➔ `Baner` ➔ `Balewadi` ➔ ... ➔ `Hadapsar` | **87.0** | 17 | ~27 | **Suboptimal (Wandering)** |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9, 3.10, 3.11, or 3.12.

### Step 1: Open Terminal in Project Directory
```powershell
cd "d:/ROUTE FINDING AGENT"
```

### Step 2: Activate Virtual Environment
```powershell
.venv\Scripts\activate
```

### Step 3: Run the Streamlit Application
```powershell
streamlit run app.py
```

The app will immediately open in your browser at:
👉 **`http://localhost:8501`**

---

## 👨‍💻 Author & Credits

Designed & Built with ❤️ by **Pratham**

- **LinkedIn:** [Pratham Buran](https://www.linkedin.com/in/pratham-buran?utm_source=share_via&utm_content=profile&utm_medium=member_android)
- **GitHub:** [PRATHAM-BURAN](https://github.com/PRATHAM-BURAN/)
