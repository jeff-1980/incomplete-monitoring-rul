## 1. H1 sensitivity: best naive chosen from {A1, A2, A3, A6} (A6 = interpolation over 150 cycles, i.e. history-matched)
FD001 k5: best=A6 18.43 vs A5 13.19; d=-3.32; 61/100; p=0.00082; Holm=0.0033
FD001 irr5: best=A6 16.61 vs A5 13.51; d=-2.50; 63/100; p=0.0023; Holm=0.0069
FD002 k5: best=A1 21.03 vs A5 13.29; d=-5.65; 180/259; p=2.8e-14; Holm=2.2e-13
FD002 irr5: best=A1 19.33 vs A5 13.43; d=-4.27; 165/259; p=2.9e-11; Holm=1.7e-10
FD003 k5: best=A6 16.40 vs A5 14.00; d=-1.56; 62/100; p=0.0046; Holm=0.0092
FD003 irr5: best=A6 17.01 vs A5 13.01; d=-2.20; 55/100; p=0.012; Holm=0.012
FD004 k5: best=A6 23.72 vs A5 15.60; d=-5.73; 166/248; p=1.5e-12; Holm=1e-11
FD004 irr5: best=A2 21.59 vs A5 14.14; d=-4.69; 165/248; p=2.6e-10; Holm=1.3e-09

## 2. Seed-level H1: Wilcoxon per seed (no seed averaging), A5 vs pre-registered best naive
FD001 k5 vs A2: per-seed p = 0.00025, 0.0015, 0.00075
FD001 irr5 vs A2: per-seed p = 0.0039, 0.00073, 0.23
FD002 k5 vs A1: per-seed p = 2.4e-09, 4e-12, 1.8e-07
FD002 irr5 vs A1: per-seed p = 4.9e-08, 1.9e-09, 9.6e-06
FD003 k5 vs A2: per-seed p = 0.0056, 0.024, 0.022
FD003 irr5 vs A2: per-seed p = 0.12, 0.0024, 0.022
FD004 k5 vs A2: per-seed p = 9.8e-11, 3.6e-06, 8e-08
FD004 irr5 vs A2: per-seed p = 3.2e-09, 2.1e-07, 1.3e-05

## 3. Out-of-range irr 1–10 (exploratory): A5 vs best naive {A1,A2,A3}
FD001: best=A2; d=-5.80; 62/100; p=0.0012
FD002: best=A1; d=-5.98; 184/259; p=5.7e-14
FD003: best=A2; d=-3.52; 57/100; p=0.03
FD004: best=A2; d=-7.15; 166/248; p=2.1e-12

## 4. PHM score robustness: per seed sum, median over seeds, and worst single engine
FD001 k1 A1: per-seed [474, 646, 730], median 646, max late error per seed [44.8, 52.2, 56.4]
FD001 k1 A2: per-seed [474, 646, 730], median 646, max late error per seed [44.8, 52.2, 56.4]
FD001 k1 A4: per-seed [694, 1109, 1044], median 1044, max late error per seed [50.6, 51.8, 53.4]
FD001 k1 A5: per-seed [413, 560, 401], median 413, max late error per seed [47.3, 45.9, 45.6]
FD001 k1 A6: per-seed [370, 325, 499], median 370, max late error per seed [34.8, 34.6, 45.6]
FD001 k5 A1: per-seed [2691, 1322, 1038], median 1322, max late error per seed [40.5, 39.8, 42.0]
FD001 k5 A2: per-seed [1401, 2399, 1299], median 1401, max late error per seed [56.3, 63.4, 55.1]
FD001 k5 A4: per-seed [416, 387, 428], median 416, max late error per seed [33.8, 37.5, 40.5]
FD001 k5 A5: per-seed [252, 270, 273], median 270, max late error per seed [37.2, 36.8, 30.0]
FD001 k5 A6: per-seed [846, 1627, 1093], median 1093, max late error per seed [48.8, 68.8, 64.6]
FD001 k5 A7: per-seed [378, 368, 367], median 368, max late error per seed [29.4, 38.0, 39.9]
FD001 irr5 A1: per-seed [1483, 770, 896], median 896, max late error per seed [32.2, 36.1, 40.0]
FD001 irr5 A2: per-seed [1511, 1764, 1879], median 1764, max late error per seed [65.7, 61.0, 60.0]
FD001 irr5 A4: per-seed [256, 283, 317], median 283, max late error per seed [31.9, 37.0, 37.6]
FD001 irr5 A5: per-seed [256, 248, 247], median 248, max late error per seed [37.3, 33.4, 26.7]
FD001 irr5 A6: per-seed [524, 638, 433], median 524, max late error per seed [44.0, 50.2, 43.8]
FD002 k1 A1: per-seed [2908, 2927, 2038], median 2908, max late error per seed [67.2, 63.8, 59.2]
FD002 k1 A2: per-seed [2908, 2927, 2038], median 2908, max late error per seed [67.2, 63.8, 59.2]
FD002 k1 A4: per-seed [1715, 1493, 1566], median 1566, max late error per seed [54.9, 53.4, 51.1]
FD002 k1 A5: per-seed [1477, 1219, 1165], median 1219, max late error per seed [55.9, 57.1, 58.1]
FD002 k1 A6: per-seed [2038, 1591, 1277], median 1591, max late error per seed [62.2, 58.6, 56.3]
FD002 k5 A1: per-seed [3653, 4162, 3246], median 3653, max late error per seed [61.5, 62.5, 62.5]
FD002 k5 A2: per-seed [5761, 9035, 6741], median 6741, max late error per seed [65.3, 81.4, 71.2]
FD002 k5 A4: per-seed [1381, 1658, 1613], median 1613, max late error per seed [52.3, 55.3, 53.7]
FD002 k5 A5: per-seed [1019, 766, 908], median 908, max late error per seed [49.3, 43.3, 48.5]
FD002 k5 A6: per-seed [3556, 9004, 14899], median 9004, max late error per seed [64.6, 75.9, 76.4]
FD002 k5 A7: per-seed [1570, 1774, 2493], median 1774, max late error per seed [60.7, 60.3, 62.8]
FD002 irr5 A1: per-seed [3379, 3075, 2456], median 3075, max late error per seed [65.6, 62.4, 63.1]
FD002 irr5 A2: per-seed [6321, 7816, 5933], median 6321, max late error per seed [68.1, 76.4, 66.7]
FD002 irr5 A4: per-seed [1048, 1036, 1315], median 1048, max late error per seed [47.4, 48.4, 55.8]
FD002 irr5 A5: per-seed [1039, 920, 851], median 920, max late error per seed [51.3, 46.4, 44.0]
FD002 irr5 A6: per-seed [2422, 3531, 6740], median 3531, max late error per seed [54.8, 65.8, 63.1]
FD003 k1 A1: per-seed [358, 468, 570], median 468, max late error per seed [45.0, 53.4, 57.3]
FD003 k1 A2: per-seed [358, 468, 570], median 468, max late error per seed [45.0, 53.4, 57.3]
FD003 k1 A4: per-seed [879, 2078, 1792], median 1792, max late error per seed [48.2, 56.5, 57.8]
FD003 k1 A5: per-seed [592, 474, 620], median 592, max late error per seed [53.4, 47.3, 52.1]
FD003 k1 A6: per-seed [393, 555, 355], median 393, max late error per seed [39.4, 57.3, 38.8]
FD003 k5 A1: per-seed [4401, 4210, 4489], median 4401, max late error per seed [62.9, 66.3, 65.2]
FD003 k5 A2: per-seed [511, 872, 835], median 835, max late error per seed [41.2, 51.3, 52.6]
FD003 k5 A4: per-seed [977, 1364, 1127], median 1127, max late error per seed [60.0, 62.3, 60.3]
FD003 k5 A5: per-seed [425, 784, 421], median 425, max late error per seed [50.5, 58.2, 46.5]
FD003 k5 A6: per-seed [1113, 1363, 911], median 1113, max late error per seed [65.2, 67.2, 62.3]
FD003 k5 A7: per-seed [396, 685, 764], median 685, max late error per seed [43.4, 51.5, 58.3]
FD003 irr5 A1: per-seed [1401, 1680, 1662], median 1662, max late error per seed [47.6, 60.6, 57.3]
FD003 irr5 A2: per-seed [1075, 1168, 2141], median 1168, max late error per seed [58.7, 62.0, 71.0]
FD003 irr5 A4: per-seed [363, 619, 537], median 537, max late error per seed [43.2, 50.8, 53.0]
FD003 irr5 A5: per-seed [299, 425, 367], median 367, max late error per seed [37.4, 48.7, 44.1]
FD003 irr5 A6: per-seed [1000, 1096, 1051], median 1051, max late error per seed [57.2, 61.5, 59.7]
FD004 k1 A1: per-seed [2032, 1977, 1843], median 1977, max late error per seed [58.6, 53.4, 55.3]
FD004 k1 A2: per-seed [2032, 1977, 1843], median 1977, max late error per seed [58.6, 53.4, 55.3]
FD004 k1 A4: per-seed [3133, 2551, 4548], median 3133, max late error per seed [65.7, 64.2, 67.3]
FD004 k1 A5: per-seed [2536, 1406, 1709], median 1709, max late error per seed [69.6, 56.1, 63.8]
FD004 k1 A6: per-seed [3364, 2453, 1410], median 2453, max late error per seed [64.9, 68.2, 60.8]
FD004 k5 A1: per-seed [12613, 11994, 12183], median 12183, max late error per seed [62.6, 67.0, 74.7]
FD004 k5 A2: per-seed [11803, 19608, 8194], median 11803, max late error per seed [81.0, 87.7, 76.5]
FD004 k5 A4: per-seed [1868, 2027, 2544], median 2027, max late error per seed [59.6, 58.7, 63.1]
FD004 k5 A5: per-seed [1532, 1576, 31933], median 1576, max late error per seed [57.7, 58.3, 103.3]
FD004 k5 A6: per-seed [47667, 22243, 17104], median 22243, max late error per seed [105.9, 91.0, 90.7]
FD004 k5 A7: per-seed [2015, 2851, 2462], median 2462, max late error per seed [57.4, 63.0, 62.5]
FD004 irr5 A1: per-seed [5367, 6156, 6136], median 6136, max late error per seed [53.8, 75.0, 65.6]
FD004 irr5 A2: per-seed [32531, 39396, 23086], median 32531, max late error per seed [99.6, 101.4, 90.0]
FD004 irr5 A4: per-seed [1371, 1311, 1576], median 1371, max late error per seed [51.8, 47.5, 54.8]
FD004 irr5 A5: per-seed [1085, 1074, 1130], median 1085, max late error per seed [55.0, 49.3, 45.3]
FD004 irr5 A6: per-seed [19808, 4706, 10288], median 10288, max late error per seed [88.3, 67.9, 80.1]

## 5. Bias (mean signed error, + = late/over-estimate) of A5 vs A1/A2 at k5
FD001 A1:-12.89 A2:+6.12 A5:-0.99 A6:+1.93 A7:-0.80
FD002 A1:-1.39 A2:+6.58 A5:+0.39 A6:+10.29 A7:+1.14
FD003 A1:-21.22 A2:+3.81 A5:+1.96 A6:+2.20 A7:+2.61
FD004 A1:-13.19 A2:+7.67 A5:+0.97 A6:+7.30 A7:-0.60
