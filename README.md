# PyRTIS

该项目是我在中国科学技术大学 2024 年春季课程《面向科学问题求解的编程实践》中的大作业。

这是一个用 Python 编写的简易路径追踪框架，并将要在其上实现各种重要性采样算法，比较它们的性能。

框架的编写思路来源于 [Ray Tracing in One Weekend Series](https://raytracing.github.io/)。

部分代码的实现有参考中国科学技术大学 2024 年春季课程《计算机图形学》的框架（[USTC-CG/USTC_CG_24: Homework repo for the course "Computer Graphics" in the 2024 spring @USTC (github.com)](https://github.com/USTC-CG/USTC_CG_24)）。

本项目得到了中国科学技术大学 Vlab 实验平台的帮助与支持。本项目超过一半的代码在 Vlab 提供的在线虚拟机中编写，并在虚拟机中进行了大量的光追运算，得到了高品质的 baseline 图像。

本项目绝大多数代码都是在 Ubuntu 22.04 系统下编写并测试，在 Windows 下并未经过充分测试。

因为我目前经验不足，许多代码存在编写不规范的问题。作为独立编写的大作业项目，本项目的注释也并不充足。如果阅读代码遇到困难，还请抱歉。

必需依赖：

- matplotlib：输出各种数学图像
- pillow 7.2：读取 Cubemap 格式天空盒文件；便于输出 jpeg 格式的文件，防止输出 GIF 时大分辨率、大 spp 的格式造成的存储容量过大问题。

可选依赖：

- PyPy 3.8：加速 Python 脚本的运行
- FFmpeg：用于将 ppm 格式的图像转换为其他格式，包括采样数增加过程的 gif 图。

目前我还没有将程序调整至不需要这些可选依赖也能运行的版本。如果现在就想运行该项目，请安装这些可选依赖。

## TODO List

### Part 1 - 将 C++ 版本的 Ray Tracing in One Weekend 改写为 Python（已完成）

### Part 2 - 将“玩具光追”改写为一个严谨的路径追踪器

- [x] 添加三角片的 Primitive Scene Object
- [x] 搭建 Cornell Box 模型
- [x] 搭建 MIS 模型
- [x] 添加球形光源与矩形光源
- [x] 对光源直接采样，完善路径追踪积分
- [x] 将材质 BRDF 的采样与计算分离
- [x] 完善天空盒，引入 CubeMap
- [ ] 用 BVH 优化射线求交性能

### Part 3 - 引入各种重要性采样算法

- [x] 实现 MIS：对光源采样 + 对 BRDF 采样
- [ ] 实现环境光重要性采样（别名法）
- [ ] 研究并实现 RIS
- [ ] 尝试用 CPU 模拟 Nvidia 的 ReSTIR GI 算法
- [ ] 探索更多的重要性采样算法

### Part 4 - 设计性能比较工具

- [x] 输出采样数增加过程的 GIF 图
- [ ] 设计测试器，将每种算法每轮采样的用时、能量和、方差输出至文件中
- [ ] 用 matplotlib 绘制曲线，并比较分析
- [ ] 完善视频输出系统，生成多种算法在同一屏幕内比较的视频

### Part 5 - 进一步完善我们的渲染器

- [x] 引入多线程
- [ ] 完善模型读取功能
- [ ] 完善 PBR 材质
- [ ] 搭建漂亮的场景
- [ ] 设计动画渲染，并研究 ReSTIR GI 在动画渲染下的优化
