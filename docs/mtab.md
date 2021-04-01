MTab: Tabular Data Annotation
===========
---

### Features:
- Semantic Annotation with knowledge graphs: Wikidata, Wikipedia, DBpedia
    - Annotate table cells with entities
    - Annotate table attributes (columns) with entity types, or classes. Currently, the tool supports table attributes as table columns. 
    - Annotate the relation between table attributes (columns) with properties (relations, or predicates). 
- Structure Annotation: 
  - Table type prediction: matrix, relational, layout (under development)
  - Header detection
  - Core attribute (subject column, or primary key) detection
  - basic stats including number of rows, columns, cells.
  - data types (under development)
  - languages (under development)
- Good for table interpretation, data integration, and knowledge discovery.

### Interface:
https://mtab.app/mtab

### API URL:
https://mtab.app/api/v1/mtab

### Usage: 
Users can send table files (in CSV, Excel, TSV format) to the tool and get the annotations.

**Note: We do not keep your data. After processing your tables, we will delete your data immediately.**


### Annotate a table:
Annotate a table in the Excel format [0AJSJYAL.xltx](https://github.com/phucty/mtab_tool/blob/master/interface/static/others/0AJSJYAL.xltx)

```bash
% curl -X POST -F file=@"YOUR_FILE_LOCATION/0AJSJYAL.xltx" https://mtab.app/api/v1/mtab
```

Expected Answer:
```json
{
  "n_tables": 1,
  "status": "Success",
  "tables": [
    {
      "name": "0AJSJYAL",
      "run_time": 0.8414499759674072,
      "semantic": {
        "cea": [
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/Newport,_Arkansas",
              "desc": "city in Arkansas, USA",
              "label": "Newport",
              "wikidata": "http://www.wikidata.org/entity/Q79414",
              "wikipedia": "http://en.wikipedia.org/wiki/Newport,_Arkansas"
            },
            "target": [
              1,
              0
            ]
          },
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/Thomas_(2001_film)",
              "desc": "2001 film by Raffaele Mertes",
              "label": "Thomas",
              "wikidata": "http://www.wikidata.org/entity/Q2421872",
              "wikipedia": "http://en.wikipedia.org/wiki/Thomas_(2001_film)"
            },
            "target": [
              2,
              0
            ]
          },
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/8082_Haynes",
              "desc": "asteroid",
              "label": "8082 Haynes",
              "wikidata": "http://www.wikidata.org/entity/Q533244",
              "wikipedia": "http://en.wikipedia.org/wiki/8082_Haynes"
            },
            "target": [
              3,
              0
            ]
          },
          {
            "annotation": {
              "desc": "family name",
              "label": "Lampitt",
              "wikidata": "http://www.wikidata.org/entity/Q37468695"
            },
            "target": [
              4,
              0
            ]
          },
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/Solanki",
              "desc": "family name",
              "label": "Solanki",
              "wikidata": "http://www.wikidata.org/entity/Q37521226",
              "wikipedia": "http://en.wikipedia.org/wiki/Solanki"
            },
            "target": [
              5,
              0
            ]
          },
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/Weston,_Colorado",
              "desc": "unincorporated community in Colorado",
              "label": "Weston",
              "wikidata": "http://www.wikidata.org/entity/Q7989353",
              "wikipedia": "http://en.wikipedia.org/wiki/Weston,_Colorado"
            },
            "target": [
              6,
              0
            ]
          }
        ],
        "cpa": [],
        "cta": [
          {
            "annotation": [
              {
                "dbpedia": "http://dbpedia.org/resource/Human_settlement",
                "desc": "community of any size, in which people live",
                "label": "human settlement",
                "wikidata": "http://www.wikidata.org/entity/Q486972",
                "wikipedia": "http://en.wikipedia.org/wiki/Human_settlement"
              },
              {
                "dbpedia": "http://dbpedia.org/resource/Surname",
                "desc": "part of a naming scheme for individuals, used in many cultures worldwide",
                "label": "family name",
                "wikidata": "http://www.wikidata.org/entity/Q101352",
                "wikipedia": "http://en.wikipedia.org/wiki/Surname"
              }
            ],
            "target": 0
          }
        ]
      },
      "status": "Success",
      "structure": {
        "cells": 37,
        "columns": 7,
        "core_attribute": 0,
        "encoding": "utf-8",
        "headers": [
          0
        ],
        "r_cells": 0.7551020408163265,
        "rows": 7,
        "table type": "vertical relation"
      },
      "table_cells": [
        [
          "col0",
          "col1",
          "col2",
          "col3",
          "col4",
          "col5",
          "col6"
        ],
        [
          "Newport",
          "31",
          "8",
          "95",
          "2",
          "-",
          "-"
        ],
        [
          "Thomas",
          "30",
          "5",
          "98",
          "2",
          "-",
          "-"
        ],
        [
          "Haynes",
          "25",
          "8",
          "68",
          "2",
          "-",
          "-"
        ],
        [
          "Lampitt",
          "29.4",
          "10",
          "73",
          "3",
          "-",
          "-"
        ],
        [
          "Solanki",
          "19",
          "4",
          "76",
          "1",
          "-",
          "-"
        ],
        [
          "Weston",
          "1",
          "0",
          "1",
          "0",
          "-",
          "-"
        ]
      ]
    }
  ]
}
```


### Annotate multiple tables:
Note: 
- Please do not send more than 100 tables for one request to avoid data transmission corruption. (We only process 100 tables per request).
- Please put your tables in a folder named tables and compress like this file [mytables.zip](https://github.com/phucty/mtab_tool/blob/master/interface/static/others/mytables.zip). (We only accept a compressed file in zip format to speed up data transmission) 
```
mytable.zip
|-- tables (folder)
|   |--table_1.csv 
|   |--table_2.csv 
|   |--...
```
**Command:** 
```bash
% curl -X POST -F file=@"YOUR_FILE_LOCATION/mytables.zip" https://mtab.app/api/v1/mtab
```

**Expected Answer:**
Refer to the [mytables.json](https://github.com/phucty/mtab_tool/blob/master/interface/static/others/mytables.json) as the full answers


### Annotate multiple tables with targets (CEA, CTA, and CPA as [SemTab challenge](https://www.cs.ox.ac.uk/isg/challenges/sem-tab/)):
Note:
The format of the compressed file like [mytables_ntar.zip](https://github.com/phucty/mtab_tool/blob/master/interface/static/others/mytable_ntar.zip).
```
mytable_ntar.zip
|-- tables (folder)
|   |--table_1.csv 
|   |--table_2.csv 
|   |--...
|-- cea.csv (Cell annotation targets in the format of [table ID, row index, column index])
|-- cta.csv (Column annotation targets in the format of [table ID, column index])
|-- cpa.csv (The relation between two columns in the format of [table ID, column 1, column 2]
```

**Command:** 
```bash
% curl -X POST -F file=@"YOUR_ZIP_FILE_LOCATION/mytables_ntar.zip" https://mtab.app/api/v1/mtab
```
**Expected Answer:**

Refer to the [mytables_ntar.json](https://github.com/phucty/mtab_tool/blob/master/interface/static/others/mytables_ntar.json) as the full answers

### Other Examples:
#### Table Annotation
<img src="../static/images/mtab_pic.png" height="500" alt="">

#### Data correction:
Input: Tabular data

| col0                    | col1     | col2       | col3       |
|-------------------------|----------|------------|------------|
| 2MASS J10540655-0031018 | -5.7     | 19.3716366 | 13.6356351 |
| 2MASS J0464841+0715177  | -2.77475 | 26.671236  | 11.8187551 |
| 2MAS J08351104+2006371  | 72.216   | 3.7242888  | 128.151961 |
| 2MASS J08330994+186328  | -6.993   | 6.0962562  | 127.649963 |

Output: 

| [star](http://www.wikidata.org/entity/Q523)                    | [radial velocity](http://www.wikidata.org/prop/direct/P2216) | [parallax](http://www.wikidata.org/prop/direct/P2214) | [right ascension](http://www.wikidata.org/prop/direct/P6257)    |
|-------------------------|-----------------|----------|--------------------|
| [2MASS J00540655-0031018](http://www.wikidata.org/entity/Q222120) | -5.70           | 19.2561  | 13.52741580209200  |
| [2MASS J00464841+0715177](http://www.wikidata.org/entity/Q222110) | -2.75           | 26.6180  | 11.70173767885790  |
| [2MASS J08351104+2006371](http://www.wikidata.org/entity/Q78611172) | 72              | 3.6984   | 128.79594070217040 |
| [2MASS J08330994+1806328](http://www.wikidata.org/entity/Q78610810) | -7              | 6.1146   | 128.29142004157090 |