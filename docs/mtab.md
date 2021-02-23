MTab: Tabular Data Annotation
===========
---
**Under development**
### Features:
- Semantic Annotation with knowledge graphs: Wikidata, Wikipedia, DBpedia
    - Cells to Entities: Similar to SemTab CEA task
    - Table attributes to Entity types, or classes. The tool currently support table attributes as table columns. 
    - The relation between table attributes to property. The tool currently supports table attributes as table columns
- Structure Annotation: (under development)
  - Table types: matrix, relational, layout
  - headers
  - core attributes
  - basic stats
  - data types
  - languages
- Good for table interpretation, data integration, and knowledge discovery.

### API URL:
http://119.172.242.147/api/v1/mtab

### Parameter: 
Currently, the tool only supports the input of the SemTab 2020 challenge, where the tool will accept a zip file with the format like the mytable.zip file.
```
mytable.zip
|-- tables (folder)
|   |--0CF12YZK.csv (table with table ID 0CF12YZK)
|   |--K0PM5GMK.csv (table with table ID K0PM5GMK)
|-- cea.csv (Cell annotation targets in the format of [table ID, row index, column index])
|-- cta.csv (Column annotation targets in the format of [table ID, column index])
|-- cpa.csv (The relation between two columns in the format of [table ID, column 1, column 2]
```

Note that: After processing the data and return the annotation, we will delete your data immediately. 

### Examples:
Making annotations for two tables in mytables.zip. 
**Command:** 
```
% curl -X POST -F file=@"YOUR_ZIP_FILE_LOCATION/mytables.zip" http://119.172.242.147/api/v1/mtab
```
Expected Answer:

Refer to the mytables.json as the full answers
```json5
{
  "n_tables": 2,
  "status": "Success",
  "tables": [
    {
      "file_name": "0CF12YZK.csv",
      "run_time": 28.576568126678467,
      "semantic": {
        "cea": [
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/Price,_Utah",
              "wikidata": "http://www.wikidata.org/entity/Q482891",
              "wikipedia": "http://en.wikipedia.org/wiki/Price,_Utah"
            },
            "target": [1,0]
          },
          ...
        ],
        "cpa": [
          {
            "annotation": {
              "wikidata": "http://www.wikidata.org/prop/direct/P4511"
            },
            "target": [0,1]
          },
          ...
        ],
        "cta": [
          {
            "annotation": {
              "dbpedia": "http://dbpedia.org/resource/Impact_crater",
              "wikidata": "http://www.wikidata.org/entity/Q55818",
              "wikipedia": "http://en.wikipedia.org/wiki/Impact_crater"
            },
            "target": 0
          }
        ]
      },
      "structure": {
        "columns": 3,
        "core_attribute": 0,
        "header": [0],
        "missing ratio": 0,
        "row": 45,
        "table type": "vertical relation"
      },
      "table_id": "0CF12YZK"
    },
    {
      "file_name": "K0PM5GMK.csv",
      ...
    }
  ]
}
```
