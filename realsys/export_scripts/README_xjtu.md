# XJTU 电池数据集（Zenodo 10963339）循环级导出

来源是 Zenodo 10963339 的 `Battery Dataset.zip`，许可为 CC BY 4.0，md5 已核对一致。这是西安交通大学的电池数据集，对应论文为 *Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis*，引用时请注明。

电池为力神 18650 NCM523，额定容量 2.0 Ah，充放电截止电压 4.2/2.5 V，以 1 Hz 采样，在室温下实验（不控温）。共 6 个批次、55 只电池。批次的协议和各批电池数见 `LISTING.txt`，官方说明是同目录下的两份 PDF。

压缩包里只有 MATLAB `.mat` 原始数据，没有现成的循环级 CSV。下面的表都由 `export_xjtu.py` 直接从 `.mat` 导出：没有做归一化，没有判定寿命终点，也没有剔除任何循环。

## 文件

| 文件 | 内容 |
|---|---|
| `cycles/{批次}_{电池}.csv` | 每只电池一张循环级表，共 55 张 |
| `all_cycles.csv.gz` | 上面 55 张表的合并 |
| `raw_curves/{批次}_{电池}_cycles_1_10_50_100.csv.gz` | 第 1、10、50、100 个循环的原始逐秒曲线（每只电池都有 ≥131 个循环，所以四个循环都在） |
| `temperature_compensation.csv.gz` | 官方另测的室温记录（不充放电的专用通道），6 段，`entry` 为段号 |
| `battery_index.json` | 每只电池的循环数，以及各类循环（按 `cycle_description`）的计数 |
| `LISTING.txt` | 压缩包目录清单（各子目录的文件数、格式、大小）和各来源的电池数 |

## 循环级表的字段

| 字段 | 单位 | 来源 | 说明 |
|---|---|---|---|
| source, batch, battery_id | | 文件名 | battery_id 如 `2C_battery-1` |
| protocol_code, protocol | | 官方说明 | 批次协议，例如 2C、3C、R2.5、R3、RW、Sim_satellite |
| ambient | | 官方说明 | 均为室温（不控温） |
| cycle | | | 从 1 开始，按包内顺序 |
| cycle_description | | `data[i].description` | **该循环的类型**，例如 `2C charge and 1C discharge`，或带 `[test capacity]` 的容量标定循环 |
| charge_capacity_Ah, discharge_capacity_Ah | Ah | `summary` | 包内现成 |
| charge_power_Wh, discharge_power_Wh | Wh | `summary` | 包内现成，字段名虽为 power，实际是能量 |
| charge/discharge_median_voltage, charge/discharge_mean_voltage | V | `summary` | 包内现成 |
| n_samples, duration_min | 个、min | 由原始曲线计算 | 采样点数、循环时长 |
| temp_mean_C, temp_max_C | °C | 由原始曲线计算 | 该循环的电池温度均值和最大值 |

原始曲线的字段为：cycle、system_time（字符串，如 `2022-09-16,15:05:22`）、relative_time_min、voltage_V、current_A（充电为正）、capacity_Ah、power_Wh、temperature_C。

## 使用时要注意

- **容量需要按循环类型筛选。** 只有 Batch-1、2、3 的每个循环都是完整放电，第 1 个循环是 0.5C/0.2C 的初始容量标定。其余批次：
  - Batch-4：放电只到 3.0 V，非标定循环的放电容量不等于电池容量；包内有 133 个左右 `2C charge and 1C discharge [test capacity]` 循环，可作容量序列。
  - Batch-5：随机放电，`discharge_capacity_Ah` 只是放掉的电量；真实容量看 `1C charge and 1C discharge [test capacity]`（每 11 个循环 1 次，每只电池约 17 次）。
  - Batch-6：只有 `[test capacity]` 循环（约每 5–6 个循环 1 次）是容量。
- Batch-3、4 的放电倍率按 0.5/1/2/3/5C 循环切换，相邻循环的放电容量随倍率变化，这不是退化。
- Batch-4、6 的电池最后一个循环往往是容量标定循环，放电容量会比前面的非标定循环高一截（例如 R3_battery-1：1.42 → 1.60）。这是循环类型不同造成的，不是容量回升。
- 温度补偿文件里的时间戳是 MATLAB datetime 对象，scipy 读不出来，所以只导出了温度序列（1 Hz）；各段的起止时间需要在 MATLAB 里读原 `.mat`。
- 原始 `.mat` 文件没有放进项目文件夹（解压后 2.9 GB），需要的话可以从 Zenodo 重新下载。
