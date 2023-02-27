# highspeed-train-route-programming
A project aimed to design routes for high speed trains using 0-1 integer programming.

The project is the coursework of the course Operational Optimization and Decision Making in the Spring Semester, 2022. The project is mainly contributed by me, and my teammates Jasper Wang and Zihan Zhao for their great contributions.

The structure of this project is as follows:

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

Notes:

- OpenSolver is needed for the Excel demo. Note that this is just a demo, and we **strongly recommend using PyGurobi** for a more robust solution.
- You may refer to the report (in Chinese) for a detailed explanation of this project.
- There are two "optimizers" in the `src` folder. `Optimizer_input.py` receives inputs from your keyboard when running. `Optimizer_args.py` receives inputs from arguments of the command line. There are 3 choices of arguments:
  1. -o Opencity 始发地. Example: 北京
  2. -d Destination 终点. Example: 桂林
  3. -f Filepath 文件路径. Example: ./data/Project_.xls
  Usage Example: Python3.8 Optimizer_args.py -o 北京 -d 桂林 -f ./data/Project_.xls

The project is mainly based on Python and pyGurobi. Depedent packages are listed in requirements.txt. Feel free to contact me for any problems.
