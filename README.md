# FEMdemo

有限元讨论班的代码。
参考教材：Jacob Fish 和 Ted Belytschko 的《A First Course in Finite Elements》。
您可以去 [b-ok.cc](https://b-ok.cc/)（可能需要翻墙）或者 [清华网盘](https://cloud.tsinghua.edu.cn/f/6449f1d74f9144b286d0/) 下载。

Demo codes for FEM (Finite Element Method) workshop.
We are following *A First Course in Finite Elements* by Jacob Fish and Ted Belytschko.

### Part 1: Finite element formulation for one-dimensional problems

* `Part1.ipynb`

    一维梁的拉伸（或压缩），截面均匀和不均匀情况。
    Tensile of 1D beams with uniform and non-uniform cross-section.
    
    视频讲解：[b站](https://www.bilibili.com/video/BV15r4y1v7s5), [Youtube](https://youtu.be/veZwGJd3_Dc)

### Part 2: Finite element formulation for scalar field problems in multidimensions

* `Example8-1.ipynb`, `Example8-2.ipynb`

    参考教材的两道例题，三角形网格和四边形上的二维热传导方程，使用 [SymPy](www.sympy.org) 辅助推导。
    Example 8.1 and 8.2 of Fish's *A First Course in Finite Elements* in which a heat conduction problem is solved using two triangular elements in Example 8.1 and a single quadrilateral element in Example 8.2.
    [SymPy](www.sympy.org) is used for symbolic computations.

    视频讲解：[b站](https://www.bilibili.com/video/BV1TR4y1T7R7/)

* `two_dim_heat.py` by [soundsinteresting](https://github.com/soundsinteresting)

    二维圆盘的热传导方程，三角网格。
    Heat equation for a 2d disk with triangular mesh.

    视频讲解：[b站](https://www.bilibili.com/video/BV1VZ4y1f7wP)

* `Part2.ipynb`

    二维热传导方程，四边形网格。
    2D heat conduction with quadrilateral mesh.


### Part 3: Finite element formulation for vector field problems in two dimensions

### Miscellaneous

* `packages-compare.md`

    选择各种 Python 包的笔记。
    Notes about choosing Python packages.
