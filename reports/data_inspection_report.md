# Initial Data Inspection Report
**Source File:** `Data set _insurance_data (1).xlsx`  
**Sheets Count:** 5  
**Sheet Names:** Customers, Policies, Claims, ExternalData, CustomerInteractions  

This report documents the structural inspection of all sheets in the raw dataset.

## Sheet: `Customers`
- **Dimensions:** 50 rows × 7 columns
- **Exact Duplicate Rows:** 0

### Column Overview
| Column Name | Inferred Type | Null Count | Missing % | Unique Count | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CustomerID` | `str` | 0 | 0.0% | 50 | C1000, C1001, C1002 |
| `Name` | `str` | 0 | 0.0% | 50 | Karen Johnson, Sandra Todd, Robin Gar... |
| `Age` | `int64` | 0 | 0.0% | 32 | 36, 41, 33 |
| `Gender` | `str` | 0 | 0.0% | 3 | Non-binary, Male, Male |
| `IncomeBracket` | `str` | 0 | 0.0% | 5 | $40k-$60k, $100k-$150k, $60k-$80k |
| `Occupation` | `str` | 0 | 0.0% | 7 | Artist, Accountant, Technician |
| `MaritalStatus` | `str` | 0 | 0.0% | 4 | Divorced, Single, Widowed |

### Categorical Value Distributions
- **`CustomerID`** (50 unique): {'C1000': 1, 'C1001': 1, 'C1002': 1, 'C1003': 1, 'C1004': 1, 'C1005': 1, 'C1006': 1, 'C1007': 1, 'C1008': 1, 'C1009': 1}
- **`Name`** (50 unique): {'Karen Johnson': 1, 'Sandra Todd': 1, 'Robin Gardner': 1, 'Jennifer Williamson': 1, 'Anthony Pugh': 1, 'Sara Dawson': 1, 'Javier Davis': 1, 'Alexander Waller': 1, 'Isaac Gomez': 1, 'Travis Edwards': 1}
- **`Gender`** (3 unique): {'Non-binary': 19, 'Male': 16, 'Female': 15}
- **`IncomeBracket`** (5 unique): {'$60k-$80k': 14, '$80k-$100k': 11, '$100k-$150k': 10, '$20k-$40k': 9, '$40k-$60k': 6}
- **`Occupation`** (7 unique): {'Artist': 12, 'Accountant': 7, 'Nurse': 7, 'Technician': 6, 'Engineer': 6, 'Teacher': 6, 'Salesperson': 6}
- **`MaritalStatus`** (4 unique): {'Divorced': 17, 'Married': 14, 'Single': 11, 'Widowed': 8}

### Numerical Statistics

```text
             Age
count  50.000000
mean   49.420000
std    16.077732
min    22.000000
25%    35.250000
50%    49.000000
75%    61.000000
max    75.000000
```

## Sheet: `Policies`
- **Dimensions:** 50 rows × 6 columns
- **Exact Duplicate Rows:** 0

### Column Overview
| Column Name | Inferred Type | Null Count | Missing % | Unique Count | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PolicyID` | `str` | 0 | 0.0% | 50 | P2000, P2001, P2002 |
| `CustomerID` | `str` | 0 | 0.0% | 50 | C1000, C1001, C1002 |
| `CoverageType` | `str` | 0 | 0.0% | 4 | Homeowners, Homeowners, Homeowners |
| `SumInsured` | `int64` | 0 | 0.0% | 5 | 100000, 150000, 250000 |
| `PropertyType` | `str` | 0 | 0.0% | 4 | House, Condo, Condo |
| `Address` | `str` | 0 | 0.0% | 50 | 03536 Brandon Bypass, Riceburgh, NV 7... |

### Categorical Value Distributions
- **`PolicyID`** (50 unique): {'P2000': 1, 'P2001': 1, 'P2002': 1, 'P2003': 1, 'P2004': 1, 'P2005': 1, 'P2006': 1, 'P2007': 1, 'P2008': 1, 'P2009': 1}
- **`CustomerID`** (50 unique): {'C1000': 1, 'C1001': 1, 'C1002': 1, 'C1003': 1, 'C1004': 1, 'C1005': 1, 'C1006': 1, 'C1007': 1, 'C1008': 1, 'C1009': 1}
- **`CoverageType`** (4 unique): {'Homeowners': 17, 'Renters': 12, 'Life': 11, 'Auto': 10}
- **`PropertyType`** (4 unique): {'Apartment': 17, 'Townhouse': 16, 'Condo': 12, 'House': 5}
- **`Address`** (50 unique): {'03536 Brandon Bypass, Riceburgh, NV 71240': 1, '4907 Good Junctions, Port Alexanderside, DC 26147': 1, '12243 Roy Lock, North Brittanyfort, MI 44048': 1, '297 Mark Centers Apt. 539, Micheletown, NH 02133': 1, '72235 Sean Field, Dawnview, RI 69695': 1, '74039 Brown Manor, New Briannafurt, SD 13056': 1, '867 Hensley Stream, East Christineside, OK 27031': 1, '43733 Elizabeth View Suite 580, New Rhondaport, VA 48927': 1, 'USS Moore, FPO AE 67838': 1, '490 Chan Road Apt. 257, Lake Samanthaberg, TN 99427': 1}

### Numerical Statistics

```text
          SumInsured
count      50.000000
mean   244000.000000
std    180034.010392
min     50000.000000
25%    100000.000000
50%    150000.000000
75%    500000.000000
max    500000.000000
```

## Sheet: `Claims`
- **Dimensions:** 100 rows × 7 columns
- **Exact Duplicate Rows:** 0

### Column Overview
| Column Name | Inferred Type | Null Count | Missing % | Unique Count | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ClaimID` | `str` | 0 | 0.0% | 100 | CL3000, CL3001, CL3002 |
| `PolicyID` | `str` | 0 | 0.0% | 43 | P2029, P2005, P2006 |
| `DateOfClaim` | `datetime64[us]` | 0 | 0.0% | 96 | 2023-02-23 00:00:00, 2024-04-16 00:00... |
| `Description` | `str` | 0 | 0.0% | 7 | Auto accident, Water damage, Theft |
| `Outcome` | `str` | 0 | 0.0% | 3 | Approved, Denied, Pending |
| `Photos` | `str` | 0 | 0.0% | 100 | photo_1.jpg, photo_2.jpg, photo_3.jpg |
| `Docs` | `str` | 0 | 0.0% | 100 | report_1.pdf, report_2.pdf, report_3.pdf |

### Categorical Value Distributions
- **`ClaimID`** (100 unique): {'CL3000': 1, 'CL3001': 1, 'CL3002': 1, 'CL3003': 1, 'CL3004': 1, 'CL3005': 1, 'CL3006': 1, 'CL3007': 1, 'CL3008': 1, 'CL3009': 1}
- **`PolicyID`** (43 unique): {'P2028': 6, 'P2012': 5, 'P2022': 4, 'P2011': 4, 'P2019': 4, 'P2045': 4, 'P2030': 4, 'P2032': 4, 'P2029': 3, 'P2001': 3}
- **`Description`** (7 unique): {'Theft': 21, 'Fire damage': 20, 'Water damage': 14, 'Vandalism': 14, 'Auto accident': 11, 'Storm damage': 11, 'Flood': 9}
- **`Outcome`** (3 unique): {'Denied': 38, 'Pending': 32, 'Approved': 30}
- **`Photos`** (100 unique): {'photo_1.jpg': 1, 'photo_2.jpg': 1, 'photo_3.jpg': 1, 'photo_4.jpg': 1, 'photo_5.jpg': 1, 'photo_6.jpg': 1, 'photo_7.jpg': 1, 'photo_8.jpg': 1, 'photo_9.jpg': 1, 'photo_10.jpg': 1}
- **`Docs`** (100 unique): {'report_1.pdf': 1, 'report_2.pdf': 1, 'report_3.pdf': 1, 'report_4.pdf': 1, 'report_5.pdf': 1, 'report_6.pdf': 1, 'report_7.pdf': 1, 'report_8.pdf': 1, 'report_9.pdf': 1, 'report_10.pdf': 1}

### Date Range
- **`DateOfClaim`**: Min = `2022-05-18 00:00:00`, Max = `2025-04-08 00:00:00`

## Sheet: `ExternalData`
- **Dimensions:** 8 rows × 4 columns
- **Exact Duplicate Rows:** 0

### Column Overview
| Column Name | Inferred Type | Null Count | Missing % | Unique Count | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Location` | `str` | 0 | 0.0% | 8 | Austin, TX, Miami, FL, Denver, CO |
| `CrimeRate` | `str` | 0 | 0.0% | 3 | Medium, Low, Low |
| `WeatherRisk` | `str` | 0 | 0.0% | 3 | High, Medium, Low |
| `FloodRisk` | `str` | 0 | 0.0% | 3 | Low, Medium, High |

### Categorical Value Distributions
- **`Location`** (8 unique): {'Austin, TX': 1, 'Miami, FL': 1, 'Denver, CO': 1, 'Seattle, WA': 1, 'Boston, MA': 1, 'Phoenix, AZ': 1, 'New York, NY': 1, 'Chicago, IL': 1}
- **`CrimeRate`** (3 unique): {'Medium': 4, 'Low': 3, 'High': 1}
- **`WeatherRisk`** (3 unique): {'High': 5, 'Low': 2, 'Medium': 1}
- **`FloodRisk`** (3 unique): {'High': 4, 'Low': 3, 'Medium': 1}
## Sheet: `CustomerInteractions`
- **Dimensions:** 20 rows × 5 columns
- **Exact Duplicate Rows:** 0

### Column Overview
| Column Name | Inferred Type | Null Count | Missing % | Unique Count | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `InteractionID` | `str` | 0 | 0.0% | 20 | I4000, I4001, I4002 |
| `CustomerID` | `str` | 0 | 0.0% | 16 | C1009, C1031, C1033 |
| `Channel` | `str` | 0 | 0.0% | 3 | Phone, Email, Email |
| `Date` | `datetime64[us]` | 0 | 0.0% | 20 | 2023-11-07 00:00:00, 2024-08-23 00:00... |
| `Summary` | `str` | 0 | 0.0% | 20 | Discuss husband key court view econom... |

### Categorical Value Distributions
- **`InteractionID`** (20 unique): {'I4000': 1, 'I4001': 1, 'I4002': 1, 'I4003': 1, 'I4004': 1, 'I4005': 1, 'I4006': 1, 'I4007': 1, 'I4008': 1, 'I4009': 1}
- **`CustomerID`** (16 unique): {'C1009': 2, 'C1008': 2, 'C1005': 2, 'C1034': 2, 'C1031': 1, 'C1033': 1, 'C1017': 1, 'C1007': 1, 'C1013': 1, 'C1043': 1}
- **`Channel`** (3 unique): {'Email': 9, 'Phone': 6, 'Chat': 5}
- **`Summary`** (20 unique): {'Discuss husband key court view economic process common coach series this add.': 1, 'Air western myself another big visit five lot human power collection key interest site particular.': 1, 'Discussion here cold nation writer should threat make cost.': 1, 'Itself already today person myself build goal ok.': 1, 'Career respond section section hand plant art.': 1, 'Mr of some state yard summer in range must.': 1, 'Certainly paper whatever my maybe sort tough smile example fast director forget.': 1, 'Approach pick process him front organization hold with phone help Mr prevent.': 1, 'Experience oil difficult decide ready avoid occur visit chair that really board owner while.': 1, 'While whose travel room discover sort population suddenly around my wind firm around window wrong.': 1}

### Date Range
- **`Date`**: Min = `2023-05-05 00:00:00`, Max = `2025-04-25 00:00:00`

