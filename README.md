<img src="interface/static/images/logo_mtab_1.png" height="120" alt="MTab">

---

MTab: Entity Search and Table Annotation with Knowledge Graphs (Wikidata, Wikipedia and DBpedia)

### Update:
- MTab at SemTab 2021: Round 2 dataset. [More Detail](https://www.aicrowd.com/challenges/semtab-2021/leaderboards)
  - Hard Table: 
    - CEA: 1st | F1: 0.985 | Precision:	0.985	
    - CTA: 1st | F1: 0.977 | Precision:	0.977	
    - CPA: 1st | F1: 0.997 | Precision:	0.998	
  - Bio Table:
    - CEA: 2nd | F1: 0.964 | Precision:	0.964	
    - CTA: 1st | F1: 0.956 | Precision:	1.000	
    - CPA: 1st | F1: 0.947 | Precision:	1.000	
 

### Demo
- Demo (Teaser): https://youtu.be/sr-zxH5JUjw
- Demonstration Video: https://youtu.be/0ibTWeObWaA
- Entity Search: https://mtab.app/mtabes
- Table Annotation: https://mtab.app/mtab


### API usage
- Entity Search: [MTabES](docs/mtabes.md)
  - Request Example: [entity search](api/lookup/m_mtabes.py)
- Table Annotation: [MTab](docs/mtab.md)
  - Request Example: [table annotation](api/annotator/m_tabano.py)

### Dataset

- SemTab 2020 (Round [1](data/semtab/2020/R1.zip), [2](data/semtab/2020/R2.zip), [3](data/semtab/2020/R3.zip), [4](data/semtab/2020/R4.zip)), and [Tough Tables](data/semtab/2020/2T.zip) datasets. We added redirect entities into ground truth for fair evaluation. 

### References
- Phuc Nguyen, Ikuya Yamada, Natthawut Kertkeidkachorn, Ryutaro Ichise, Hideaki Takeda, Demonstration of MTab: Tabular Data Annotation with Knowledge Graphs. [[video](https://youtu.be/0ibTWeObWaA)]

- Phuc Nguyen, Hideaki Takeda, MTab: Tabular Data Annotation, NII Open House June 2021. [[video](https://youtu.be/1ByffPp2alg?t=3269)]

- Phuc Nguyen, Ikuya Yamada, Hideaki Takeda, [MTabES: Entity Search with Keyword Search, Fuzzy Search, and Entity Popularities](https://drive.google.com/file/d/10Tl0Qd5gxFSiCsnSjJbvRSUiDXW-Kifn/view?usp=sharing), In The 35th Annual Conference of the Japanese Society for Artificial Intelligence (JSAI), 2021. [[video](https://drive.google.com/file/d/1gYSP619HcMT-sE6iD3LiQeRtZw9UZTWQ/view?usp=sharing)]


- Phuc Nguyen, Ikuya Yamada, Natthawut Kertkeidkachorn, Ryutaro Ichise, Hideaki Takeda, [MTab4Wikidata at SemTab 2020: Tabular Data Annotation with Wikidata](http://ceur-ws.org/Vol-2775/paper9.pdf), In SemTab@ISWC, 2020. [[video](https://drive.google.com/file/d/1vz-6nkc9t6MQZYzgg-PZNLs-9TT86wRD/view?usp=sharing)]

  
- Phuc Nguyen, Natthawut Kertkeidkachorn, Ryutaro Ichise, Hideaki Takeda [MTab: Matching Tabular Data to Knowledge Graph using Probability Models](http://ceur-ws.org/Vol-2553/paper2.pdf), In SemTab@ISWC, 2019, [[slides](http://www.cs.ox.ac.uk/isg/challenges/sem-tab/2019/slides/MTab.pptx)]

  
### Awards:
- 1st prize at SemTab 2020 (tabular data to Wikidata matching). [Results](http://www.cs.ox.ac.uk/isg/challenges/sem-tab/2020/results.html)
  <img src="static/images/semtab2020.png" height="350" alt="MTab">

- 1st prize at SemTab 2019 (tabular data to DBpedia matching). [Results](http://www.cs.ox.ac.uk/isg/challenges/sem-tab/2019/results.html)
  <img src="static/images/semtab2019.png" height="350" alt="MTab">

### Citing

If you find MTab tool useful in your work, and you want to cite our work, please use the following referencee:
```
@inproceedings{2020_mtab4wikidata,
  author    = {Phuc Nguyen and
               Ikuya Yamada and
               Natthawut Kertkeidkachorn and
               Ryutaro Ichise and
               Hideaki Takeda},
  title     = {MTab4Wikidata at SemTab 2020: Tabular Data Annotation with Wikidata},
  booktitle = {SemTab@ISWC 2020},
  volume    = {2775},
  pages     = {86--95},
  publisher = {CEUR-WS.org},
  year      = {2020}
}
```

### Contact
Phuc Nguyen (`phucnt@nii.ac.jp`)
