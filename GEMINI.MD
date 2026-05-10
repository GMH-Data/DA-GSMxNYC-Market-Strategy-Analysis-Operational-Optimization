# Project: NYC Taxi Data Analysis

## 1. Project Overview

This project provides a comprehensive overview and analysis environment for the NYC Taxi & Limousine Commission (TLC) Trip Record Data. The core objectives are:

1. **Market Entry Strategy & Operational Optimization**: Phân tích tình hình thị trường taxi NYC để xác định các cơ hội chiến lược và tối ưu hóa vận hành, phục vụ mục tiêu thâm nhập thị trường của **GSM**.
2. **Operational Demand Forecasting**: Dự báo nhu cầu thị trường để tối ưu hóa việc điều phối đội xe (Fleet Dispatching) dựa trên dữ liệu lịch sử bằng mô hình **Prophet**.
3. **Operational Efficiency & Anomaly Warning**: Giám sát hiệu suất và thiết lập hệ thống cảnh báo bất thường trong vận hành bằng **Isolation Forest**, đảm bảo GSM duy trì chất lượng dịch vụ ổn định.

Hệ thống được thiết kế để xử lý hiệu quả các tập dữ liệu khổng lồ (hơn 2.9 tỷ dòng từ trước năm 2019 đến 2026+) bằng các công cụ dữ liệu hiện đại (DuckDB) mà không cần đến các cụm máy tính phân tán.

## 2. Tech Stack

- **Language**: Python 3.9+
- **Data Engine**: DuckDB (for high-performance analytical queries directly on Parquet files)
- **Data Processing**: Pandas, PyArrow
- **Machine Learning**: Prophet (Meta), Scikit-learn (Isolation Forest)
- **Environment**: JupyterLab, Virtual Environment (`.venv` or `uv`)
- **Visualization**: Plotly (Primary), Matplotlib, Seaborn

## 3. Folder Structure

- `Analysis.ipynb`: **[MAIN]** Primary analysis environment and execution flow.
- `forecast_models.ipynb`: File để xây dựng các mô hình dự đoán.
- `Draft/`: Contains `Data.ipynb` as a historical reference and draft logic.
- `Dataset/`: Contains raw Parquet files and `DIM/` directory for dimension tables. **(Ignored by Git)**
- `src/`: Reusable Python modules (e.g., `db_manager.py`) and the `taxi_data.duckdb` database.
- `.agents/rules/`: Custom rules for Agent behavior (Context, Data Model).
- `.vscode/`: Standardized IDE configurations for the team.
- `requirements.txt`: Python dependency list.

## 4. Coding Standards & Modeling

- **Architecture**: **Star Schema** with a central `FACT_TAXI_TRIPS` and multiple `DIM_` tables.
- **Modularity**: Centralized database connection management via `src/db_manager.py`.
- **Formatting**: Enforced via `Ruff` and `pre-commit` hooks.
- **Icons**: TUYỆT ĐỐI KHÔNG sử dụng icon (emoji) trong code, documentation, hay output console.
- **Code Headers**: Ở đầu mỗi cell code bắt buộc phải có comment `# [Số thứ tự] [Tiêu đề mục]` để dễ dàng tìm kiếm và đồng bộ với Markdown.
- **Notebook Editing**: Luôn tạo các file script Python để thực hiện chỉnh sửa Notebook (.ipynb) (lưu ý chỉ chỉnh sửa mới cần) và lưu các script này vào thư mục `Draft/` để theo dõi lịch sử thay đổi.
- **Data Output**: Tất cả các cell code thực hiện tính toán hoặc xử lý dữ liệu đều phải in ra các bảng số liệu (Pandas DataFrame hoặc DuckDB output).
- **Direct Editing**: Đối với các file tài liệu có định dạng `.md` và `.txt`, thực hiện chỉnh sửa nội dung trực tiếp. TUYỆT ĐỐI KHÔNG tạo script Python để chỉnh sửa các định dạng này nhằm tối ưu hóa hiệu suất.
- **Security**: No sensitive data or massive datasets (Parquet/CSV/DB) should be tracked by Git.
- **Language Policy**: TUYỆT ĐỐI KHÔNG sử dụng tiếng Việt trong file `Analysis.ipynb`. Tất cả code, comments và nội dung Markdown trong file này phải được viết bằng tiếng Anh (English).
- **Duplicity Check**: Khi bắt đầu thực hiện một task, TUYỆT ĐỐI KHÔNG chạy ngay code tính toán hoặc xử lý dữ liệu. Thay vào đó, cần truy vấn vào database để kiểm tra xem dữ liệu hoặc kết quả tương tự đã được tính toán và lưu trữ trước đó hay chưa. Chỉ thực hiện tính toán mới khi xác nhận dữ liệu chưa tồn tại.

---

## 5. Dataset Summary

The dataset contains trip records for various types of taxi and for-hire vehicle services in New York City. The data is stored in **Parquet** format.

### Taxi Types Included

- **Yellow Taxi**: Traditional street-hail taxis authorized to pick up passengers anywhere in NYC.
- **Green Taxi**: Street-hail liveries (SHLs) authorized to pick up passengers in northern Manhattan and the outer boroughs.
- **FHV (For-Hire Vehicle)**: Liveries, black cars, and luxury limousines.
- **FHVHV (High Volume For-Hire Vehicle)**: Services like Uber and Lyft that provide more than 10,000 trips per day.

---

## 6. Data Dictionary Details

### Yellow Taxi (`yellow_tripdata_*.parquet`)

| Field Name | Description |
| :--- | :--- |
| `VendorID` | 1 = Creative Mobile Technologies, 2 = Curb Mobility, 6 = Myle, 7 = Helix |
| `tpep_pickup_datetime` | The date and time when the meter was engaged. |
| `tpep_dropoff_datetime`| The date and time when the meter was disengaged. |
| `passenger_count` | The number of passengers in the vehicle. |
| `trip_distance` | The elapsed trip distance in miles. |
| `RatecodeID` | 1=Standard, 2=JFK, 3=Newark, 4=Nassau/Westchester, 5=Negotiated, 6=Group, 99=Unknown |
| `PULocationID` | TLC Taxi Zone in which the taximeter was engaged. |
| `DOLocationID` | TLC Taxi Zone in which the taximeter was disengaged. |
| `payment_type` | 0=Flex, 1=Credit, 2=Cash, 3=No charge, 4=Dispute, 5=Unknown, 6=Void |
| `fare_amount` | The time-and-distance fare calculated by the meter. |
| `tip_amount` | Tip amount (Credit card tips only). |
| `total_amount` | The total amount charged to passengers (excluding cash tips). |

### FHVHV (`fhvhv_tripdata_*.parquet`)

| Field Name | Description |
| :--- | :--- |
| `hvfhs_license_num` | HV0002: Juno, HV0003: Uber, HV0004: Via, HV0005: Lyft |
| `pickup_datetime` | The date and time of the trip pick-up. |
| `dropoff_datetime` | The date and time of the trip drop-off. |
| `PULocationID` | TLC Taxi Zone in which the trip began. |
| `DOLocationID` | TLC Taxi Zone in which the trip ended. |
| `trip_miles` | Total miles for passenger trip. |
| `trip_time` | Total time in seconds for passenger trip. |
| `base_passenger_fare` | Base passenger fare before tolls, tips, taxes, and fees. |
| `driver_pay` | Total driver pay. |

---

## 7. Metadata: Taxi Zones

The `taxi_zone_lookup.csv` contains 265 unique location IDs mapped to **Borough**, **Zone**, and **Service Zone**.

---

## 8. Design System & Color Palette

### A. Core Theme (Modern Dark)

- **Primary Background**: `#0F172A` (Deep Navy/Black)
- **Primary Accent**: `#FF007F` (Neon Pink)
- **Secondary Accent**: `#00F2FF` (Cyan/Aqua)

### B. Taxi Service Mapping

| Service Type | Hex Code | Color Name | Usage |
| :--- | :--- | :--- | :--- |
| **Yellow Taxi** | `#F7B731` | NYC Gold | Yellow Taxi plots |
| **Green Taxi** | `#26DE81` | Boro Green | Green Taxi plots |
| **Uber (HVFHS)**| `#2F3542` | Slate Black | Uber data |
| **Lyft (HVFHS)**| `#FF00BF` | Lyft Pink | Lyft data |

### C. Analytical Indicators

- **Growth (Positive)**: `#20BF6B` (Emerald)
- **Decline (Negative)**: `#EB3B5A` (Alizarin Red)
- **Forecast/Trend**: `#8854D0` (Royal Purple)
- **Mean/Median**: `#45AAF2` (Highlighter Blue)
