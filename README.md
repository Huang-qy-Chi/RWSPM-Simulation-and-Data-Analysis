# RWSPM — Region-Wise Statistical Parametric Mapping

**Language / 语言** · [English](#english) · [简体中文](#简体中文)

## English

RWSPM partitions images into overlapping windows, transforms each window with the log quantile density (LQD) representation, runs a regional Ball Covariance (BCov) test, and combines the connected significant regions with RW-MTCCT. The repository contains two independent Python workflows. Both use an interior LQD quantile grid from `eta` to `1 - eta`, with default `eta = 1e-3` and 21 grid points.

| Directory | Workflow |
| --- | --- |
| [Simulation](Simulation/) | Seven synthetic settings. Each region in the selected cluster contributes to the Cauchy statistic with fixed weight `1/m`, where `m` is the total number of windows. |
| [Realdata](Realdata/) | Left and right hippocampal SNP scans with covariate adjustment, a compiled SNP-specific BCov kernel and a NumPy backend. ADNI data are not included in this repository. |

Use Python 3.12 and install the requirements for the workflow you want to run.

### Simulation

From the repository root:

```bash
cd Simulation
python -m pip install -r requirements.txt
python run_simu_parallel_eta.py --settings 1 --n_rep 2 --n 24 --M1 14 --M2 11 --window_width 7 --n_workers 1 --method gamma --n_perm 19
```

This small example checks execution. For experiment runs, set the settings, sample size, replication count, window width and calibration method explicitly. Omitting `--window_width` on the command line enables JSD-based width selection. Use `--eta` to change the truncation boundary. Use `--help` for the complete options. The default output directory `Simulation/data/result/` (when run from `Simulation/`) contains per-region statistics and p-values and one cluster-level p-value per replication.

The simulation supports `gamma`, `permu` and `limit`. Build the Ball BDD library for `limit` using `bash cball_ext/compile_linux.sh` on Linux. On Windows with MinGW-w64 on PATH, run `compile_win.bat` from the `cball_ext` directory in Command Prompt.

### ADNI analysis

From the repository root, on Linux:

```bash
cd Realdata
python -m pip install -r requirements.txt
bash cball_ext/compile_snp_linux.sh
python smoke_test_GWAS.py --backend c --n_process 2 --n_perm 19
```

On Windows with MinGW-w64 on PATH, run `compile_snp_win.bat` from the `cball_ext` directory in Command Prompt. The smoke test generates its own data and runs both hemispheres. `--backend c` requires a loadable C library. `auto` falls back to NumPy when that library is unavailable. For `--method limit`, also build the separate Ball BDD library as described above.

ADNI data should not be shared publicly and are not included in this repository. If you need the data used for this analysis, please contact XXX (email: [EMAIL TO BE PROVIDED]) regarding access, subject to applicable data-use requirements. Once obtained, place the four files listed below directly in the repository's `Realdata/` folder, alongside `GWAS_left.py` and `GWAS_right.py`. The scripts read this folder by default. Alternatively, place them in another authorized directory and specify its path with `--data_dir`. The genotype input is the sampled 25,000-SNP array. The pipeline assumes the same subjects in the same row order in all matrices and cannot verify subject identity from the matrices.

| File | Object and layout |
| --- | --- |
| `ADNI_1_3_sampled_25000.npy` | Numeric subject-by-SNP array with genotype dosages coded 0, 1 or 2. SNP indices start at zero. The filename is retained for compatibility. |
| `cov_inf_0711_1_3.rdata` | `cov_inf1_3`, subject-by-covariate design matrix including the intercept. |
| `left_hipp_ori.rdata` | `left_hipp_inf1_3`, subject-by-15,000 left hippocampal measurements, flattened in row-major order from a 150 × 100 grid. |
| `right_hipp_ori.rdata` | `right_hipp_inf1_3`, same layout for the right hippocampus. |

```bash
python GWAS_left.py --snp_start 0 --n_snp 1 --method gamma --n_perm 199 --backend c --n_process 2
python GWAS_right.py --snp_start 0 --n_snp 1 --method gamma --n_perm 199 --backend c --n_process 2
```

These commands illustrate the input and output interfaces. Each hemisphere writes a SNP summary and per-region p-values under `Realdata/results_gwas_left/` or `Realdata/results_gwas_right/`. The default partition is width 11 and step 3. The ADNI branch retains the source GWAS aggregation convention, using denominator `m - n_sig + B`, where `n_sig` counts all screened regions and `B` counts those in the selected component. The `gamma_sample` option fits the permutation null on a fixed genotype-stratified subsample and uses a separate calibration from full-sample `gamma`. Choose the calibration and permutation count for the analysis being reproduced. The synthetic smoke test checks execution, including the selected backend. It provides no evidence about extreme-tail calibration.

Simulation is based on the `code_lqd/Python` eta branch. The ADNI workflow is based on the SNP-accelerated GWAS source also used for the server's November 8 benchmark, with interior quantiles added for this release. The earlier simulation repository provides the layout reference. [RWSPM simulation repository](https://github.com/Huang-qy-Chi/RWSPM-Region-Wise-Statistical-Parametric-Mapping)

See [third-party source notices](THIRD_PARTY_NOTICES.md) for the bundled Ball sources.

[Back to language selector](#rwspm--region-wise-statistical-parametric-mapping)

## 简体中文

RWSPM 用重叠滑窗划分图像，对各窗口做对数分位密度（LQD）变换，使用 Ball Covariance（BCov）进行区域检验，再以 RW-MTCCT 聚合空间连通的显著区域。两个目录可独立运行，均默认在 `[eta, 1 - eta]` 上使用 21 个等距分位点，`eta = 1e-3`。

| 目录 | 用途 |
| --- | --- |
| [Simulation](Simulation/) | 七种模拟设置。入选簇中的每个区域以固定权重 `1/m` 计入 Cauchy 统计量，`m` 为筛选前的区域总数。 |
| [Realdata](Realdata/) | 左右海马 SNP 关联分析，包含协变量校正、SNP 专用 BCov C 内核和 NumPy 后端。本仓库不包含 ADNI 数据。 |

使用 Python 3.12，并安装对应目录的依赖。

### 模拟实验

在仓库根目录执行以下命令。

```bash
cd Simulation
python -m pip install -r requirements.txt
python run_simu_parallel_eta.py --settings 1 --n_rep 2 --n 24 --M1 14 --M2 11 --window_width 7 --n_workers 1 --method gamma --n_perm 19
```

这是小规模运行示例。正式实验请显式指定模拟设置、样本量、重复次数、窗宽和校准方法。命令行省略 `--window_width` 时按 JSD 自动选宽，`--eta` 可调整分位网格截断，`--help` 可查看完整参数。从 `Simulation/` 运行时，默认输出至 `Simulation/data/result/`，包括每次重复的区域统计量、区域 p 值和簇级 p 值。

模拟支持 `gamma`、`permu` 和 `limit`。`limit` 需要编译 Ball BDD 库。在 Linux 上执行 `bash cball_ext/compile_linux.sh`。在 Windows 上将 MinGW-w64 加入 PATH，然后在命令提示符中进入 `cball_ext` 运行 `compile_win.bat`。

### ADNI 分析

在 Linux 上，从仓库根目录执行以下命令。

```bash
cd Realdata
python -m pip install -r requirements.txt
bash cball_ext/compile_snp_linux.sh
python smoke_test_GWAS.py --backend c --n_process 2 --n_perm 19
```

在 Windows 上将 MinGW-w64 加入 PATH，然后在命令提示符中进入 `cball_ext` 运行 `compile_snp_win.bat`。冒烟测试使用现场生成的合成数据运行两个半球。`--backend c` 要求成功加载 C 库。`auto` 在 C 库不可用时回退到 NumPy。`--method limit` 还需要编译独立的 Ball BDD 库，编译方式见上文。

ADNI 数据不宜直接公开，本仓库不提供这些数据。如需获取本分析所用数据，请联系 XXX（邮箱：[待填写]），并遵守适用的数据使用要求。获得数据后，请将下表中的四个文件直接放入仓库的 `Realdata/` 文件夹，与 `GWAS_left.py` 和 `GWAS_right.py` 位于同一目录，脚本默认从该目录读取。也可将文件放在其他获授权的目录，并通过 `--data_dir` 指定路径。基因型输入为抽取的 25,000 个 SNP 数组。所有矩阵必须按同一受试者顺序逐行对齐，矩阵本身无法验证受试者身份。

| 文件 | 对象与格式 |
| --- | --- |
| `ADNI_1_3_sampled_25000.npy` | 受试者 × SNP 的数值数组，基因型剂量编码为 0、1、2。SNP 列索引从 0 开始。文件名沿用原流程。 |
| `cov_inf_0711_1_3.rdata` | 对象 `cov_inf1_3`，受试者 × 协变量的设计矩阵，包含截距列。 |
| `left_hipp_ori.rdata` | 对象 `left_hipp_inf1_3`，每位受试者 15,000 个左海马测量值，按行展开自 150 × 100 网格。 |
| `right_hipp_ori.rdata` | 对象 `right_hipp_inf1_3`，右海马，格式同左侧。 |

```bash
python GWAS_left.py --snp_start 0 --n_snp 1 --method gamma --n_perm 199 --backend c --n_process 2
python GWAS_right.py --snp_start 0 --n_snp 1 --method gamma --n_perm 199 --backend c --n_process 2
```

以上命令用于说明输入输出接口。左右半球分别在 `Realdata/results_gwas_left/` 和 `Realdata/results_gwas_right/` 输出 SNP 汇总和区域 p 值。默认窗宽为 11，步长为 3。ADNI 分支沿用来源 GWAS 的聚合约定，权重分母为 `m - n_sig + B`，其中 `n_sig` 是通过初筛的区域数，`B` 是入选簇中的区域数。`gamma_sample` 在固定的基因型分层子样本上拟合置换零分布，使用独立于全样本 `gamma` 的校准。正式复现时按目标分析选择方法和置换次数。合成数据测试用于验证运行流程和后端，不用于验证极端尾部校准。

模拟部分基于 `code_lqd/Python` 的 eta 分支。ADNI 部分基于服务器 11 月 8 日基准所用的 SNP 加速源码，并接入分位网格截断。目录组织参考先前的模拟仓库。[RWSPM 模拟仓库](https://github.com/Huang-qy-Chi/RWSPM-Region-Wise-Statistical-Parametric-Mapping)

随附 Ball 源码的版权与许可见[第三方源码说明](THIRD_PARTY_NOTICES.md)。

[返回语言选择](#rwspm--region-wise-statistical-parametric-mapping)
