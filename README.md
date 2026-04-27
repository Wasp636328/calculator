# calculator# 🎓 Student CGPA & Attendance Tracker

> **Smart Academic Performance Monitoring System**  
> Built with Python · Streamlit · Plotly · Pandas

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## ✨ Features

| Feature | Details |
|---|---|
| **Dynamic Subject Entry** | Add / remove subjects on the fly |
| **Marks Calculator** | Internal (50) + External (100) → Total % |
| **Grade Engine** | S / A / B / C / D / E / F with grade points |
| **CGPA** | Credit-weighted cumulative GPA |
| **Attendance Tracker** | Per subject + overall %, with 75% alerts |
| **Required Marks Predictor** | Tells you exactly what you need in finals to reach the next grade |
| **Visual Analytics** | Bar, Pie, Attendance Bar, Radar chart |
| **Export** | Download CSV or TXT report |
| **Dark Premium UI** | Professional dark theme with custom CSS |

---

## 🚀 Quick Start

### Local

```bash
git clone https://github.com/<your-username>/cgpa-tracker.git
cd cgpa-tracker
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

### Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set `app.py` as entry point
4. Deploy ✅

---

## 📁 Project Structure

```
cgpa-tracker/
├── app.py            ← Main application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🧮 Grading Scale

| Marks | Grade | Grade Point |
|-------|-------|-------------|
| 90–100 | S | 10 |
| 80–89  | A | 9  |
| 70–79  | B | 8  |
| 60–69  | C | 7  |
| 50–59  | D | 6  |
| 40–49  | E | 5  |
| < 40   | F | 0  |

**CGPA** = Σ(GP × Credits) / Σ Credits

---

## 🛠 Tech Stack

- **[Streamlit](https://streamlit.io)** — Web UI framework
- **[Plotly](https://plotly.com/python/)** — Interactive charts
- **[Pandas](https://pandas.pydata.org)** — Data processing
- **[NumPy](https://numpy.org)** — Numerical utilities

---

## 🗺 Roadmap

- [ ] Multi-semester history & trend tracking
- [ ] University ERP API integration
- [ ] AI-based grade prediction
- [ ] Smart study planner
- [ ] Exam countdown & notification system

---

## 📄 License

MIT — free to use, modify, and distribute.
