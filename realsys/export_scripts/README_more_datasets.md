# 四个新增电池数据集的循环级导出（2026-11-15）

本次新增四个数据集，导出格式与 XJTU 那份（见 `README.md`）一致：每只电池一张循环级表，另有一张合并表 `all_cycles.csv.gz`，以及记录每只电池循环数和协议参数的 `battery_index.json`。每个子目录里都附了导出脚本。

所有表都直接从原始文件导出：
- 不做归一化，不判定寿命终点，不删除任何循环；
- 原始文件自带的字段原样保留，例如 Severson 的内阻和温度、HUST 的 RUL 标签；
- 由逐点曲线计算的列与 XJTU 版本相同：充放电能量、电压中位数和均值、采样点数、循环时长；
- **每只电池的协议参数单独成列**，`battery_index.json` 里也有。

| 子目录 | 数据集 | 电池数 | 化学体系，额定容量 | 协议上的差异 | 许可证 |
|---|---|---|---|---|---|
| `mit_severson2019/` | Severson 等 2019，*Nature Energy* 4:383（MIT/Stanford/TRI），data.matr.io | 140 只（3 批，论文用了其中 124 只） | LFP/石墨 A123 APR18650M1A，1.1 Ah | 两段快充 C1(SOC%)-C2；放电统一为 4C；30 °C | CC BY 4.0 |
| `attia2020/` | Attia 等 2020，*Nature* 578:397（闭环优化快充），data.matr.io | 233 只：验证批（2019-01-24）45 只循环到失效，4 个 OED 批 188 只只循环 100–120 次 | 同上 | 四段快充 CC1-CC2-CC3-CC4（每段 20% SOC，0–80%） | CC BY 4.0 |
| `tongji/` | Zhu 等 2022，*Nature Communications* 13:2261（同济），Zenodo 6405084 | 130 只 | NCA 3.5 Ah（66 只）、NCM 3.5 Ah（55 只）、NCM+NCA 2.5 Ah（9 只） | 温度 25/35/45 °C，充电 0.25/0.5/1C，放电 1/2/4C | CC BY 4.0 |
| `hust_ma2022/` | Ma 等 2022，*Energy Environ. Sci.* 15:4083（华中科大），Mendeley 10.17632/nsc7hnsg4s.2 | 77 只 | LFP/石墨，1.1 Ah | 充电相同（5C）；放电为四段，各电池不同；30 °C | CC BY 4.0 |

使用时请引用原论文。原始文件都核对过校验值：Zenodo 用 md5，Mendeley 用 sha256。原始文件太大，没有放进项目文件夹（.mat 共约 9 GB，同济的 CSV 约 5.6 GB），需要时可以重新下载。

## 各数据集的协议列

- **Severson / Attia**：
  - `protocol_code` 是原文件里的 `policy_readable`。
  - 两段快充时有 `charge_C1`、`charge_switch_soc_pct`、`charge_C2` 三列；四段快充时有 `CC1`–`CC4` 四列。
  - 不论哪种，都在 80% SOC 之后转 1C CC-CV 到 3.6 V，放电为 4C 到 2.0 V。
  - 原文件给出的寿命在 `battery_index.json` 的 `cycle_life_official` 里。
- **同济**：
  - 协议从文件名 `CY{温度}-{充电倍率}_{放电倍率}-#{编号}` 解析而来，对应 `ambient_C`、`charge_rate_C`、`discharge_rate_C` 三列。
  - 另有实测的充放电电流中位数。注意充电电流的中位数包含 CV 段，会低于标称值。
- **HUST**：
  - 每只电池的放电分段电流（C）和每段放出的电量是在第 2 个循环上实测的，对应 `discharge_stage_C` 和 `discharge_stage_Ah_cycle2` 两列。论文中的协议表不在数据文件里。
  - `discharge_capacity_Ah` 用的是文件自带的每循环 `dq`。
  - `rul_label` 是文件自带的 RUL。

## 已知问题，使用前请看

- **Severson 2017-06-30 批**：
  - c7、c8、c9、c15、c16 的 policy 字符串在原文件里就被截断了，例如 `80%)-3.6C`，所以协议列为空。这 5 只是 2017-05-12 批中部分电池的续测，按 Severson 原代码的做法，应该和第一批对应的电池拼接起来使用。
  - c12 的 policy 被截断成 `4C(31%)-5`，C2 那一列不可靠。
  - 论文剔除了部分异常电池，这里没有剔除。
- **Severson / Attia**：每张表第一行（`cycle` 为 0 或 1）是原文件 summary 里的占位行，容量为 0，保留原样。2018-04-12 批的 policy 带 `-newstructure` 后缀，保留原样。
- **Attia 的 OED 批**：只循环了 100–120 次，没有寿命终点，只适合做早期预测类的研究。论文用来验证的是 2019-01-24 批。
- **同济**：
  - 少数电池的 `v_min` 低于截止电压，甚至为 0，例如 NCA CY25-025_1-#2、NCM+NCA CY25-05_4-#2。这是原始记录里的单点异常，没有处理。
  - 没有电池温度列，只有箱温（`ambient_C`）。
- **HUST**：原文件是 Python pickle 格式。导出时用的是受限的反序列化器，只允许 numpy 和 pandas 的类。

## 总包

`battery_all_20261115.zip` 包含 XJTU 和上面四个数据集的全部循环级表、索引、说明和导出脚本，不含原始文件。在本机下载这一个文件就能一次取齐。
