# Project: NYC Taxi Data Analysis

## 1. Project Overview
This project provides a comprehensive overview and analysis environment for the NYC Taxi & Limousine Commission (TLC) Trip Record Data. The core objectives are:
1. **Business Analysis**: Phân tích hoạt động kinh doanh của taxi để đánh giá mức độ tăng trưởng qua các năm.
2. **Business Forecasting**: Dự báo tình hình kinh doanh trong tương lai dựa trên dữ liệu lịch sử.
3. **Anomaly Warning System**: Thiết lập các chỉ số (indicators) để đưa ra cảnh báo (warning) kịp thời, và dùng tập dữ liệu `2026_Plus` để test thử nghiệm mô hình cảnh báo.

Hệ thống được thiết kế để xử lý hiệu quả các tập dữ liệu khổng lồ (từ trước năm 2019 đến 2026+) bằng các công cụ dữ liệu hiện đại mà không cần đến các cụm máy tính phân tán.

## 2. Tech Stack
- **Language**: Python 3.9+
- **Data Engine**: DuckDB (for high-performance analytical queries directly on Parquet files)
- **Data Processing**: Pandas, PyArrow
- **Environment**: JupyterLab, Virtual Environment (`.venv` or `uv`)
- **Visualization**: Matplotlib, Seaborn, Plotly

## 3. Folder Structure
- `Dataset/`: Contains the raw Parquet files (Yellow, Green, FHV, FHVHV) and metadata (`taxi_zone_lookup.csv`). **(Ignored by Git)**
- `src/`: Reusable Python modules and scripts (e.g., `db_manager.py` for database connection).
- `notebooks/`: Jupyter Notebooks for exploratory data analysis (EDA).
- `output/`: Generated plots, reports, and processed data.
- `.vscode/`: Standardized IDE configurations for the team.
- `requirements.txt`: Python dependency list.
- `setup_env.ps1`: Automated script to initialize the virtual environment.

## 4. Coding Standards
- **Architecture**: Modular scripts with centralized database connection management (`src/db_manager.py`).
- **Formatting**: Code formatting and linting are enforced via `Ruff`.
- **Security**: No sensitive data or massive datasets (Parquet/CSV) should be tracked by Git.
- **Editor Consistency**: Enforced via `.editorconfig`.

---

## 5. Dataset Summary

The dataset contains trip records for various types of taxi and for-hire vehicle services in New York City. The data is stored in **Parquet** format.

### Taxi Types Included:
- **Yellow Taxi**: Traditional street-hail taxis authorized to pick up passengers anywhere in NYC.
- **Green Taxi**: Street-hail liveries (SHLs) authorized to pick up passengers in northern Manhattan and the outer boroughs.
- **FHV (For-Hire Vehicle)**: Liveries, black cars, and luxury limousines.
- **FHVHV (High Volume For-Hire Vehicle)**: Services like Uber and Lyft that provide more than 10,000 trips per day.

---

## 6. Data Dictionary Details

### Yellow Taxi (`yellow_tripdata_*.parquet`)
| Field Name | Description |
| :--- | :--- |
| `VendorID` | A code indicating the TPEP provider that provided the record.<br>1 = Creative Mobile Technologies, LLC<br>2 = Curb Mobility, LLC<br>6 = Myle Technologies Inc<br>7 = Helix |
| `tpep_pickup_datetime` | The date and time when the meter was engaged. |
| `tpep_dropoff_datetime`| The date and time when the meter was disengaged. |
| `passenger_count` | The number of passengers in the vehicle. |
| `trip_distance` | The elapsed trip distance in miles reported by the taximeter. |
| `RatecodeID` | The final rate code in effect at the end of the trip.<br>1 = Standard rate<br>2 = JFK<br>3 = Newark<br>4 = Nassau or Westchester<br>5 = Negotiated fare<br>6 = Group ride<br>99 = Null/unknown |
| `store_and_fwd_flag` | This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka "store and forward," because the vehicle did not have a connection to the server.<br>Y = store and forward trip<br>N = not a store and forward trip |
| `PULocationID` | TLC Taxi Zone in which the taximeter was engaged. |
| `DOLocationID` | TLC Taxi Zone in which the taximeter was disengaged. |
| `payment_type` | A numeric code signifying how the passenger paid for the trip.<br>0 = Flex Fare trip<br>1 = Credit card<br>2 = Cash<br>3 = No charge<br>4 = Dispute<br>5 = Unknown<br>6 = Voided trip |
| `fare_amount` | The time-and-distance fare calculated by the meter. For additional information on the following columns, see https://www.nyc.gov/site/tlc/passengers/taxi-fare.page |
| `extra` | Miscellaneous extras and surcharges. |
| `mta_tax` | Tax that is automatically triggered based on the metered rate in use. |
| `tip_amount` | Tip amount – This field is automatically populated for credit card tips. Cash tips are not included. |
| `tolls_amount` | Total amount of all tolls paid in trip. |
| `improvement_surcharge` | Improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015. |
| `total_amount` | The total amount charged to passengers. Does not include cash tips. |
| `congestion_surcharge` | Total amount collected in trip for NYS congestion surcharge. |
| `airport_fee` | For pick up only at LaGuardia and John F. Kennedy Airports. |
| `cbd_congestion_fee` | Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025. |

### Green Taxi (`green_tripdata_*.parquet`)
| Field Name | Description |
| :--- | :--- |
| `VendorID` | A code indicating the LPEP provider that provided the record.<br>1 = Creative Mobile Technologies, LLC<br>2 = Curb Mobility, LLC<br>6 = Myle Technologies Inc |
| `lpep_pickup_datetime` | The date and time when the meter was engaged. |
| `lpep_dropoff_datetime`| The date and time when the meter was disengaged. |
| `store_and_fwd_flag` | This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka "store and forward," because the vehicle did not have a connection to the server. |
| `RatecodeID` | The final rate code in effect at the end of the trip.<br>1 = Standard rate<br>2 = JFK<br>3 = Newark<br>4 = Nassau or Westchester<br>5 = Negotiated fare<br>6 = Group ride<br>99 = Null/unknown |
| `PULocationID` | TLC Taxi Zone in which the taximeter was engaged. |
| `DOLocationID` | TLC Taxi Zone in which the taximeter was disengaged. |
| `passenger_count` | The number of passengers in the vehicle. |
| `trip_distance` | The elapsed trip distance in miles reported by the taximeter. |
| `fare_amount` | The time-and-distance fare calculated by the meter. For additional information on the following columns, see https://www.nyc.gov/site/tlc/passengers/taxi-fare.page |
| `extra` | Miscellaneous extras and surcharges. |
| `mta_tax` | Tax that is automatically triggered based on the metered rate in use. |
| `tip_amount` | Tip amount – This field is automatically populated for credit card tips. Cash tips are not included. |
| `tolls_amount` | Total amount of all tolls paid in trip. |
| `improvement_surcharge` | Improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015. |
| `total_amount` | The total amount charged to passengers. Does not include cash tips. |
| `payment_type` | A numeric code signifying how the passenger paid for the trip.<br>0 = Flex Fare trip<br>1 = Credit card<br>2 = Cash<br>3 = No charge<br>4 = Dispute<br>5 = Unknown<br>6 = Voided trip |
| `trip_type` | A code indicating whether the trip was a street-hail or a dispatch that is automatically assigned based on the metered rate in use but can be altered by the driver.<br>1 = Street-hail<br>2 = Dispatch |
| `congestion_surcharge` | Total amount collected in trip for NYS congestion surcharge. |
| `cbd_congestion_fee` | Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025. |

### FHV (`fhv_tripdata_*.parquet`)
| Field Name | Description |
| :--- | :--- |
| `dispatching_base_num` | The TLC Base License Number of the base that dispatched the trip. |
| `pickup_datetime` | The date and time of the trip pick-up. |
| `dropOff_datetime` | The date and time of the trip dropoff. |
| `PUlocationID` | TLC Taxi Zone in which the trip began. |
| `DOlocationID` | TLC Taxi Zone in which the trip ended. |
| `SR_Flag` | Indicates if the trip was a part of a shared ride chain offered by a High Volume FHV company (e.g. Uber Pool, Lyft Line). For shared trips, the value is 1. For non-shared rides, this field is null.<br><br>NOTE: For most High Volume FHV companies, only shared rides that were requested AND matched to another shared-ride request over the course of the journey are flagged. However, Lyft (base license numbers B02510 + B02844) also flags rides for which a shared ride was requested but another passenger was not successfully matched to share the trip—therefore, trips records with SR_Flag=1 from those two bases could indicate EITHER a first trip in a shared trip chain OR a trip for which a shared ride was requested but never matched. Users should anticipate an overcount of successfully shared trips completed by Lyft. |
| `Affiliated_base_number` | Base number of the base with which the vehicle is affiliated. This must be provided even if the affiliated base is the same as the dispatching base. |

### FHVHV (`fhvhv_tripdata_*.parquet`)
| Field Name | Description |
| :--- | :--- |
| `hvfhs_license_num` | The TLC license number of the HVFHS base or business.<br>As of September 2019, the HVFHS licensees are the following:<br>• HV0002: Juno<br>• HV0003: Uber<br>• HV0004: Via<br>• HV0005: Lyft |
| `dispatching_base_num` | The TLC Base License Number of the base that dispatched the trip. |
| `originating_base_num` | Base number of the base that received the original trip request. |
| `request_datetime` | Date/time when passenger requested to be picked up. |
| `on_scene_datetime` | Date/time when driver arrived at the pick-up location (Accessible Vehicles only). |
| `pickup_datetime` | The date and time of the trip pick-up. |
| `dropoff_datetime` | The date and time of the trip drop-off. |
| `PULocationID` | TLC Taxi Zone in which the trip began. |
| `DOLocationID` | TLC Taxi Zone in which the trip ended. |
| `trip_miles` | Total miles for passenger trip. |
| `trip_time` | Total time in seconds for passenger trip. |
| `base_passenger_fare` | Base passenger fare before tolls, tips, taxes, and fees. |
| `tolls` | Total amount of all tolls paid in trip. |
| `bcf` | Total amount collected in trip for Black Car Fund. |
| `sales_tax` | Total amount collected in trip for NYS sales tax. |
| `congestion_surcharge` | Total amount collected in trip for NYS congestion surcharge. |
| `airport_fee` | $2.50 for both drop off and pick up at LaGuardia, Newark, and John F. Kennedy airports. |
| `tips` | Total amount of tips received from passenger. |
| `driver_pay` | Total driver pay (not including tolls or tips and net of commission, surcharges, or taxes). |
| `shared_request_flag` | Did the passenger agree to a shared/pooled ride, regardless of whether they were matched? (Y/N) |
| `shared_match_flag` | Did the passenger share the vehicle with another passenger who booked separately at any point during the trip? (Y/N) |
| `access_a_ride_flag` | Was the trip administered on behalf of the Metropolitan Transportation Authority (MTA)? (Y/N) |
| `wav_request_flag` | Did the passenger request a wheelchair-accessible vehicle (WAV)? (Y/N) |
| `wav_match_flag` | Did the trip occur in a wheelchair-accessible vehicle (WAV)? (Y/N) |
| `cbd_congestion_fee` | Per-trip charge for MTA's Congestion Relief Zone starting Jan. 5, 2025. |

---

## 7. Metadata: Taxi Zones
The `taxi_zone_lookup.csv` contains 265 unique location IDs mapped to:
- **Borough**: EWR, Queens, Bronx, Manhattan, Staten Island, Brooklyn.
- **Zone**: Specific neighborhoods (e.g., Alphabet City, JFK Airport).
- **Service Zone**: Yellow Zone, Boro Zone, Airports, EWR.

---

## 8. Design System & Color Palette

To ensure consistency across visualizations (Plotly, Matplotlib, Seaborn), the following color palette is used:

### A. Core Theme (Modern Dark)
- **Primary Background**: `#0F172A` (Deep Navy/Black)
- **Primary Accent**: `#FF007F` (Neon Pink) - Used for highlights and major trends.
- **Secondary Accent**: `#00F2FF` (Cyan/Aqua) - Used for secondary data series.

### B. Taxi Service Mapping
| Service Type | Hex Code | Color Name | Usage |
| :--- | :--- | :--- | :--- |
| **Yellow Taxi** | `#F7B731` | NYC Gold | All Yellow Taxi related plots |
| **Green Taxi** | `#26DE81` | Boro Green | All Green Taxi related plots |
| **Uber (HVFHS)**| `#2F3542` | Slate Black | Uber specific data |
| **Lyft (HVFHS)**| `#FF00BF` | Lyft Pink | Lyft specific data |
| **FHV (Other)** | `#A5B1C2` | Silver Grey | Standard FHV/Base data |

### C. Analytical Indicators
- **Growth (Positive)**: `#20BF6B` (Emerald)
- **Decline (Negative)**: `#EB3B5A` (Alizarin Red)
- **Forecast/Trend**: `#8854D0` (Royal Purple)
- **Mean/Median**: `#45AAF2` (Highlighter Blue)
