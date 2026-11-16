## (1) Padding: share of test engines whose 30-record window is not filled by measured records
FD001: n=100, length min/median 31/133; padded at k=1: 0%; at k=5: 58% (median records 27); irr1-5: 25%; at k=5 the 30-cycle interpolated window of A2 contains median 6 measured records; A6/A8 150-cycle window median 27 records
FD002: n=259, length min/median 21/132; padded at k=1: 2%; at k=5: 57% (median records 27); irr1-5: 30%; at k=5 the 30-cycle interpolated window of A2 contains median 6 measured records; A6/A8 150-cycle window median 27 records
FD003: n=100, length min/median 38/148; padded at k=1: 0%; at k=5: 47% (median records 30); irr1-5: 16%; at k=5 the 30-cycle interpolated window of A2 contains median 6 measured records; A6/A8 150-cycle window median 30 records
FD004: n=248, length min/median 19/153; padded at k=1: 4%; at k=5: 46% (median records 30); irr1-5: 19%; at k=5 the 30-cycle interpolated window of A2 contains median 6 measured records; A6/A8 150-cycle window median 30 records

## (2) End-of-life accuracy: RMSE and bias on test engines with true RUL <= 50 (case 1 same-run batch, 5 seeds; case 2, 5 seeds)
FD001: 33 engines with RUL <= 50
  case1 k1: A1 6.2 (+2.4); A2 6.2 (+2.4); A6 7.2 (+2.3); A5 7.1 (+4.3); A8 4.5 (+0.1); B1_GRUD 7.0 (+3.8)
  case1 k5: A1 12.0 (-9.0); A2 12.9 (+6.2); A6 12.1 (+3.9); A5 6.7 (+3.4); A8 7.3 (+2.8); B1_GRUD 7.7 (+3.0)
  case1 irr5: A1 10.6 (-7.3); A2 9.6 (+4.1); A6 8.6 (+3.0); A5 6.3 (+1.8); A8 5.6 (+1.7); B1_GRUD 7.4 (+2.0)
  case2 full: A1 6.2 (+2.4); A2 6.2 (+2.4); B2 5.7 (+0.9); C8 5.4 (+1.1); A6L 7.2 (+2.3)
  case2 h10: A1 32.0 (+18.7); A2 27.6 (-1.5); B2 13.8 (+5.6); C8 19.0 (+9.3); A6L 45.2 (+27.1)
  case2 h5: A1 25.4 (+14.9); A2 30.5 (+10.9); B2 13.2 (+5.5); C8 15.1 (+7.1); A6L 36.0 (+17.2)
FD002: 88 engines with RUL <= 50
  case1 k1: A1 7.6 (+0.7); A2 7.6 (+0.7); A6 7.2 (+1.6); A5 7.7 (+1.8); A8 5.5 (-0.8); B1_GRUD 7.9 (+2.8)
  case1 k5: A1 12.1 (-3.8); A2 15.3 (+5.8); A6 23.1 (+13.5); A5 5.7 (+2.0); A8 6.1 (+1.7); B1_GRUD 6.3 (+2.5)
  case1 irr5: A1 9.3 (-5.4); A2 13.4 (+4.2); A6 16.3 (+7.9); A5 6.2 (+1.8); A8 5.7 (+1.4); B1_GRUD 6.3 (+2.2)
  case2 full: A1 7.6 (+0.7); A2 7.6 (+0.7); B2 9.0 (+2.7); C8 5.4 (+0.7); A6L 7.2 (+1.6)
  case2 h10: A1 24.2 (+11.0); A2 16.4 (-7.5); B2 13.4 (+4.8); C8 11.6 (+3.0); A6L 43.9 (+24.5)
  case2 h5: A1 22.3 (+9.2); A2 16.7 (+8.3); B2 12.5 (+4.4); C8 12.3 (+2.9); A6L 35.4 (+14.8)
FD003: 29 engines with RUL <= 50
  case1 k1: A1 4.8 (-0.4); A2 4.8 (-0.4); A6 5.0 (+1.2); A5 6.6 (+3.9); A8 5.5 (+1.5); B1_GRUD 6.1 (+2.6)
  case1 k5: A1 30.8 (-28.3); A2 7.5 (+0.2); A6 5.9 (-0.1); A5 5.2 (+1.4); A8 5.4 (+0.6); B1_GRUD 6.1 (+0.7)
  case1 irr5: A1 21.9 (-19.7); A2 5.7 (+1.2); A6 7.6 (+1.5); A5 5.1 (+2.1); A8 6.7 (+1.6); B1_GRUD 5.7 (+1.1)
  case2 full: A1 4.8 (-0.4); A2 4.8 (-0.4); B2 6.9 (-2.8); C8 5.1 (+1.2); A6L 5.0 (+1.2)
  case2 h10: A1 35.8 (+25.1); A2 33.0 (-21.8); B2 17.1 (+6.2); C8 22.0 (+11.0); A6L 61.9 (+48.6)
  case2 h5: A1 41.7 (+31.2); A2 39.1 (-22.5); B2 17.9 (+7.1); C8 21.3 (+11.7); A6L 54.3 (+38.9)
FD004: 80 engines with RUL <= 50
  case1 k1: A1 12.0 (+5.4); A2 12.0 (+5.4); A6 11.5 (+4.7); A5 11.0 (+6.0); A8 6.2 (+1.7); B1_GRUD 11.9 (+6.6)
  case1 k5: A1 19.9 (-8.0); A2 22.9 (+10.9); A6 23.4 (+11.6); A5 10.0 (+5.2); A8 12.4 (+5.4); B1_GRUD 9.9 (+5.2)
  case1 irr5: A1 14.6 (-6.2); A2 21.6 (+9.1); A6 18.4 (+8.4); A5 9.5 (+4.8); A8 9.4 (+4.2); B1_GRUD 10.0 (+4.4)
  case2 full: A1 12.0 (+5.4); A2 12.0 (+5.4); B2 10.5 (+3.9); C8 8.3 (+2.8); A6L 11.5 (+4.7)
  case2 h10: A1 31.6 (+18.4); A2 21.5 (-4.8); B2 15.9 (+7.7); C8 16.7 (+8.7); A6L 45.5 (+27.5)
  case2 h5: A1 30.7 (+17.0); A2 27.7 (+13.7); B2 16.4 (+8.0); C8 18.7 (+8.2); A6L 40.8 (+21.4)

## (3) Case 2: bias, PHM median over seeds, largest late error (all test engines)
FD001 A1: full: bias +2.2, PHM med 609, max late 55 | h10: bias +14.7, PHM med 40441, max late 103 | h5: bias +16.4, PHM med 17713, max late 97
FD001 A2: full: bias +2.2, PHM med 609, max late 55 | h10: bias +10.0, PHM med 8438, max late 91 | h5: bias +16.1, PHM med 17432, max late 90
FD001 B2: full: bias +1.4, PHM med 412, max late 50 | h10: bias +3.2, PHM med 1168, max late 65 | h5: bias +4.0, PHM med 933, max late 59
FD001 C8: full: bias -0.1, PHM med 323, max late 44 | h10: bias +6.8, PHM med 2346, max late 75 | h5: bias +7.7, PHM med 1437, max late 65
FD001 A6L: full: bias +1.4, PHM med 454, max late 48 | h10: bias +23.1, PHM med 82351, max late 109 | h5: bias +20.2, PHM med 15998, max late 105
FD002 A1: full: bias -0.1, PHM med 2363, max late 67 | h10: bias +11.9, PHM med 53383, max late 117 | h5: bias +11.5, PHM med 37045, max late 106
FD002 A2: full: bias -0.1, PHM med 2362, max late 67 | h10: bias +1.4, PHM med 8128, max late 86 | h5: bias +10.0, PHM med 8392, max late 83
FD002 B2: full: bias -0.3, PHM med 3258, max late 74 | h10: bias +0.5, PHM med 3859, max late 98 | h5: bias +1.0, PHM med 3189, max late 74
FD002 C8: full: bias -1.9, PHM med 1143, max late 60 | h10: bias +0.8, PHM med 4507, max late 87 | h5: bias +1.8, PHM med 2406, max late 68
FD002 A6L: full: bias +0.7, PHM med 1551, max late 58 | h10: bias +22.2, PHM med 143793, max late 111 | h5: bias +18.6, PHM med 83848, max late 102
FD003 A1: full: bias +3.6, PHM med 458, max late 61 | h10: bias +22.1, PHM med 19183, max late 89 | h5: bias +26.5, PHM med 22164, max late 90
FD003 A2: full: bias +3.6, PHM med 458, max late 61 | h10: bias -16.1, PHM med 15814, max late 92 | h5: bias -2.3, PHM med 11285, max late 95
FD003 B2: full: bias +3.3, PHM med 417, max late 58 | h10: bias +7.4, PHM med 2111, max late 72 | h5: bias +7.5, PHM med 2448, max late 71
FD003 C8: full: bias +3.3, PHM med 338, max late 55 | h10: bias +11.2, PHM med 5468, max late 81 | h5: bias +11.9, PHM med 4319, max late 78
FD003 A6L: full: bias +3.1, PHM med 404, max late 43 | h10: bias +34.2, PHM med 147450, max late 135 | h5: bias +30.8, PHM med 83553, max late 109
FD004 A1: full: bias +1.4, PHM med 2033, max late 85 | h10: bias +12.9, PHM med 43132, max late 101 | h5: bias +13.3, PHM med 31658, max late 100
FD004 A2: full: bias +1.1, PHM med 2600, max late 85 | h10: bias -5.6, PHM med 10335, max late 75 | h5: bias +8.5, PHM med 10830, max late 84
FD004 B2: full: bias +0.5, PHM med 1658, max late 66 | h10: bias +1.9, PHM med 4507, max late 75 | h5: bias +2.7, PHM med 4588, max late 75
FD004 C8: full: bias +0.3, PHM med 1279, max late 60 | h10: bias +4.1, PHM med 4507, max late 82 | h5: bias +5.2, PHM med 6460, max late 88
FD004 A6L: full: bias +0.7, PHM med 1798, max late 67 | h10: bias +20.9, PHM med 139684, max late 111 | h5: bias +18.2, PHM med 107286, max late 109

## (4) Identity: case-2 dense (A1, full history) vs post-review A1 (k=1); A6L (full) vs post-review A6 (k=1)
FD001: max |A1 diff| 0.0000; max |A6L-A6| 0.0000
FD002: max |A1 diff| 0.0000; max |A6L-A6| 0.0000
FD003: max |A1 diff| 0.0000; max |A6L-A6| 0.0000
FD004: max |A1 diff| 0.0000; max |A6L-A6| 0.0000

## (5) Grouped (twins merged) N-CMAPSS per-arm means (mean over units of seed-averaged unit RMSE)
Q3 首次 irr5/A1=11.07 irr5/A2=9.87 irr5/A3=10.05 irr5/A4=8.39 irr5/A5=7.96 irr5/A6=14.96 k1/A1=8.09 k1/A2=8.09 k1/A3=8.09 k1/A4=7.87 k1/A5=7.74 k1/A6=9.38 k5/A1=12.31 k5/A2=10.34 k5/A3=11.64 k5/A4=7.69 k5/A5=7.88 k5/A6=16.34 k5/A7=8.42
Q3 A8 irr5/A1=11.07 irr5/A2=9.87 irr5/A3=10.05 irr5/A5=7.83 irr5/A8=7.64 irr5/B1_GRUD=7.98 k1/A1=8.09 k1/A2=8.09 k1/A3=8.09 k1/A5=7.64 k1/A8=7.98 k1/B1_GRUD=8.57 k5/A1=12.31 k5/A2=10.34 k5/A3=11.64 k5/A5=7.77 k5/A8=8.15 k5/B1_GRUD=7.89
Q6 full/A1=8.19 full/A2=8.19 full/A6L=9.51 full/B2=8.10 full/B3=7.77 full/C8=7.78 h3/A1=11.40 h3/A2=20.65 h3/A6L=18.19 h3/B2=8.53 h3/B3=8.54 h3/B4=7.97 h3/C8=9.80 h5/A1=10.15 h5/A2=15.45 h5/A6L=17.84 h5/B2=8.15 h5/B3=8.09 h5/B4=8.14 h5/C8=9.32
