<p class="language-switch" align="center">
  <a href="./README.md">🇺🇸 English</a> •
  <a href="./README.ru.md">🇷🇺 Русский</a> •
  <a href="./README.fr.md">🇫🇷 Français</a>
</p>

<div align="center">

# Hedgehog RP Stats

</div>

**Chat Statistics** is an analytics platform for the Hedgehog RP community's VK chat. The service brings together tools for collecting, processing, and visualizing message data to analyze participant activity and track the community's development throughout its history.

Rankings, charts, graphs, and summary metrics help identify the most active participants and track communication trends, community growth, and other key changes.

## ✨ Features

- View participant message statistics
- Rankings of the most active users
- Data visualization with charts and graphs
- Activity analysis across different time periods
- Community-wide summary metrics

## 🔗 Related Projects

- 🦔 [Hedgehog RP](https://github.com/MaSStiK/hedgehog-rp) - main project
- 🌍 [Interactive Online Map](https://github.com/MaSStiK/map.hedgehog-rp)
- 📺 [Hedgehog Television](https://github.com/MaSStiK/tv.hedgehog-rp)

## 🛠️ Technologies and Tools

### Website

- **HTML, CSS, JavaScript** - Core web technologies
- **Chart.js** - Chart creation and data visualization

### Data Processing

- **Python** - Data processing and aggregation
- **vk_api** - Integration with the VK API
- **pandas** - Data analysis and transformation

### Development Tools

- **ChatGPT** - Most of the website was developed with its help.

## 📦 Data Collection

VK data collection scripts are not published in this repository for privacy reasons.

### Script Overview

1. **`fetch_messages.py`** - Exports messages and actions from the VK chat and stores the data by year.
2. **`fetch_entities.py`** - Collects information about chat participants and saves it to `vk_entities.json`.
3. **`stats_report.py`** - Processes the collected data and generates the final `summary_stats.json` file.

<!-- portfolio:hide:start -->

## 📸 Website Screenshots

<table align="center">
    <tr>
        <td align="center">
            <img width="1500" alt="Community Statistics Dashboard" src="https://github.com/user-attachments/assets/8e044313-1eaa-4076-bbee-e6d3f35bca56" />
            <br>
            <p>Community Statistics Dashboard</p>
        </td>
    </tr>
</table>

<!-- portfolio:hide:end -->
