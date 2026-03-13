markdown
# 🎓 MUJ Student Advisor AI
### PS 01: Student Academic Performance Prediction
*IEEE CIS AI Model Quest 2.0*

---

## 📋 Overview
The **MUJ Student Advisor AI** is a machine learning-powered tool that predicts student academic performance and generates personalized intervention plans. By analyzing 15 behavioral, psychological, and environmental factors, it helps educators identify at-risk students early and provide targeted support based on official MUJ guidelines.

**Key Capabilities:**
- 99% accurate predictions across 4 grade tiers
- Real-time analysis with confidence scoring
- Bias-free assessment across demographics
- Actionable success plans for each risk level

---

## ✨ Features

| | |
|---|---|
| **Real-time Prediction** | 4 grade tiers instantly |
| **Confidence Meter** | Visual probability |
| **Success Plans** | Auto-generated |
| **Demo Profiles** | One-click samples |
| **Bias Checks** | Fairness assured |

---

## 🛠️ Tech Stack

| | |
|---|---|
| **Model** | Random Forest |
| **Framework** | Scikit-learn |
| **App** | Streamlit |
| **Viz** | Plotly |

```python
# Model Config
params = {
    'n_estimators': 100,
    'max_depth': 15,
    'min_samples_split': 10
}
```
--- 

## 📊 15 Factors
| | |
|---|---|
| **Category** |	 Factors |
| **Academic** |	 Hours, Attendance, Assignments, Exam, Online |
| **Psychological** | 	Motivation, Stress, Learning Style|
| **Demographic** | 	Gender, Age|
| **Environmental** | 	Internet, Resources, EduTech, Extra, Discussions|

## 📈 Performance
| | |
|---|---|
| **Metric** |	Value|
|**Accuracy**|	99%|
|**Train Size**| 	9,806|
|**Test Size** |	2,111|

## Top Features
| | |
|---|---|
| **Feature** |	Importance|
|**Exam Score** |	82%|
|**Assignments**| 	3.2%|
|**Attendance**|	2.9%|
|**Study Hours**|	2.6%|

## Bias Check
| | |
|---|---|
|**Group** |	Acc|
|**Male**|	99%|
|**Female**	|99%|
|**Has Internet**|	99%|
|**No Internet**|	99%|
---
## 🚀 Quick Start
```bash
git clone https://github.com/Sparsh8998/MUJ-Student-Advisor.git
cd MUJ-Student-Advisor
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```


## 🏆 Results
✅ 99% accuracy

✅ 12k+ patterns modeled

✅ Zero bias

✅ <0.5s prediction
