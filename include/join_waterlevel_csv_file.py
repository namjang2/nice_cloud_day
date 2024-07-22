import csv
import pandas as pd

# 데이터 로드
list_data = pd.read_csv("/opt/airflow/data/waterlevel/list.csv", header=0)
associate_data = pd.read_csv("/opt/airflow/data/waterlevel/associate_list.csv", header=0)

# 각 셀의 양쪽 공백 제거
list_data = list_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
associate_data = associate_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# 두 데이터프레임 병합
merged_data = pd.merge(list_data, associate_data, left_on='obs_id', right_on='obs_id')

# attn_level, warn_level, danger_level, rel_river, first_at 열의 빈 값 제거 (NaN 또는 빈 문자열)
merged_data = merged_data.dropna(subset=['attn_level', 'warn_level', 'danger_level', 'rel_river', 'first_at'])
merged_data = merged_data[(merged_data['attn_level'] != '') & (merged_data['warn_level'] != '') & (merged_data['danger_level'] != '') & (merged_data['rel_river'] != '') & (merged_data['first_at'] != '')]

# 결과 저장
output_file_path = '/opt/airflow/data/info/water_level_info.csv'
merged_data.to_csv(output_file_path, index=False, quoting=csv.QUOTE_ALL)

# 'obs_id' 열 추출
obs_id_column = merged_data[['obs_id']]

# 결과 저장 (유효한 obs_id로 업데이트)
output_file_path = '/opt/airflow/data/waterlevel/extracted_id_list.csv'
obs_id_column.to_csv(output_file_path, index=False)

print(f"{merged_data.shape}, {obs_id_column.shape}")
