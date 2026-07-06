<p align="right">
  <a href="./README.md">🇺🇸 English</a> |
  <a href="./README-ru.md">🇷🇺 Русский</a> |
  <a href="./README-fr.md">🇫🇷 Français</a>
</p>

# Hedgehog RP Stats
> **Main project:** [hedgehog-rp](https://github.com/MaSStiK/hedgehog-rp)

**Chat Statistics** is an analytics platform designed to visualize VK community message statistics for the Hedgehog RP project. The service combines data collection, processing, and presentation tools, making it possible to analyze participant activity and track the community's evolution over time.

Statistics are presented through rankings, charts, graphs, and summary metrics, providing a clear overview of user engagement, communication trends, and community growth.

## ✨ Features
- View participant message statistics
- Rankings of the most active users
- Data visualization with charts and graphs
- Activity analysis across different time periods
- Community-wide summary metrics

## 🔗 Related Projects
- 🦔 [Hedgehog RP](https://github.com/MaSStiK/hedgehog-rp)
- 🌍 [Interactive Map](https://github.com/MaSStiK/map.hedgehog-rp)
- 📺 [Hedgehog Television](https://github.com/MaSStiK/tv.hedgehog-rp)

## 🛠️ Website Technologies
- **HTML, CSS, JavaScript** - Core web technologies
- **Chart.js** - Charts and data visualization

## 🐍 Data Processing Tools
- **Python** - Data processing and aggregation
- **vk_api** - Integration with the VK API
- **pandas** - Data analysis and transformation

## 📦 Data Collection
Data collection scripts are not included in the repository for privacy reasons.

### ⚙️ Script Overview
1. **`fetch_messages.py`** - Exports VK chat messages and actions, storing data by year.
2. **`fetch_entities.py`** - Collects participant information and saves it to `vk_entities.json`.
3. **`stats_report.py`** - Processes collected data and generates `summary_stats.json`.

## 📸 Screenshots
<table>
    <tr>
        <td align="center">
            <img width="1500" alt="screenshot" src="https://github.com/user-attachments/assets/8e044313-1eaa-4076-bbee-e6d3f35bca56" />
            <br>
            <p>Community Statistics Dashboard</p>
        </td>
    </tr>
</table>
