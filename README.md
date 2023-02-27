# highspeed-train-route-programming
A project aimed to design routes for high speed trains using 0-1 integer programming.

The project is the coursework of the course Operational Optimization and Decision Making in the Spring Semester, 2022. The project is mainly contributed by me. My teammates Jasper Wang and Zihan Zhao also made great contributions.

The structure of this project is as follows:

```shell
├── PPT
  ├── A PowerPoint for presentation
├── Excel
  ├── one spread sheet for a *demo* solution with Excel contributed by Jasper Wang
├── src
  ├── AHP.py  Code for Hierarchical Analysis and weight generation
  ├── Optimizer_input.py  Optimizer for train routes
  ├── Optimizer_args.py  (optional) Optimizer for train routes with input from command lines
├── data
  ├── data_vfinal.xlsx  Original data containing detailed process of preprocessing and normalization
  ├── Project_.xls  DEPENDENT data for codes in "src"
├── proposal  Proposal Reports
├── report
  ├── 《运筹优化与最优决策》第五组期末报告——基于整数优化的高速列车运行路径优化问题.pdf  Project report in Chinese
└── README.md  README file
```

Notes:

- OpenSolver is needed for the Excel demo. Note that this is just a demo, and we **strongly recommend using PyGurobi** for a more robust solution.
- You may refer to the report (in Chinese) for a detailed explanation of this project.
- There are two "optimizers" in the `src` folder. `Optimizer_input.py` receives inputs from your keyboard when running. `Optimizer_args.py` receives inputs from arguments of the command line. There are 3 choices of arguments:
  1. -o Opencity 始发地. Example: 北京
  2. -d Destination 终点. Example: 桂林
  3. -f Filepath 文件路径. Example: ./data/Project_.xls
  Usage Example: Python3.8 Optimizer_args.py -o 北京 -d 桂林 -f ./data/Project_.xls

The project is mainly based on Python and pyGurobi. Depedent packages are listed in requirements.txt. As a result, please run the following command before you delve into source codes:
```
pip install -r requirements.txt
```
Feel free to contact me for any problems.

## References

- 闫绍辉,张天伟,董隆健.高速铁路跨线列车运行路径选择优化模型[J].铁道运输与经济,2021,43(05):109-116.DOI:10.16668/j.cnki.issn.1003-1421.2021.05.17.
- 毛万华,陈亚茹.高速铁路列车运行图新增列车运行线优化方法研究[J].铁道运输与经济,2021,43(11):1-6+26.DOI:10.16668/j.cnki.issn.1003-1421.2021.11.01.
- 葛露露.基于群决策层次分析法的铁路信息化评价考核指标体系权重确定[J].铁路计算机应用,2017,26(04):6-9.
- 赵若开. 普速铁路与高速铁路跨线旅客列车开行方案优化研究[D].西南交通大学,2018.
- 《中国城市品牌影响力报告（2021）》. 中国社会科学院财经战略研究院、中国社会科学出版社, https://baijiahao.baidu.com/s?id=1718472393380246339&wfr=spider&for=pc.
- 中国铁路12306信息网站. www.12306.cn
- 线路基本信息. 中华人民共和国国家发展和改革委员会网站.