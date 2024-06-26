# PyRTIS

该项目是我在中国科学技术大学 2024 年春季课程《面向科学问题求解的编程实践》中的大作业。

这是一个用 Python 编写的简易路径追踪框架，并将要在其上实现各种重要性采样算法，比较它们的性能。

框架的编写思路来源于 [Ray Tracing in One Weekend Series](https://raytracing.github.io/)。

部分代码的实现有参考中国科学技术大学 2024 年春季课程《计算机图形学》的框架（[USTC-CG/USTC_CG_24: Homework repo for the course "Computer Graphics" in the 2024 spring @USTC (github.com)](https://github.com/USTC-CG/USTC_CG_24)）。

本项目得到了中国科学技术大学 Vlab 实验平台的帮助与支持。本项目超过一半的代码在 Vlab 提供的在线虚拟机中编写，并在虚拟机中进行了大量的光追运算，得到了高品质的参考图像。

本项目绝大多数代码都是在 Ubuntu 22.04 系统下编写并测试，在 Windows 下也能保证稳定的运行。

因为我目前经验不足，许多代码存在编写不规范的问题。作为独立编写的大作业项目，本项目的注释也并不充足。如果阅读代码遇到困难，可以向作者询问。

依赖：

- matplotlib：输出各种数学图像
- numpy：对接图像的输入输出
- pillow 7.2：读取 Cubemap 格式天空盒文件；便于输出 jpeg 格式的文件，防止输出 GIF 时大分辨率、大 spp 的格式造成的存储容量过大问题。

- PyPy 3.8：加速 Python 脚本的运行
- FFmpeg：用于将 ppm 格式的图像转换为其他格式，包括采样数增加过程的 gif 图。

## 命令行选项

在 Linux 系统下，可以在项目根目录下通过 `run.sh` 自定义输出图像的行为。例如：

```bash
./run.sh -o ref -size 800*600 -spp 2048 -scene cornell_cubemap
```

你还可以用形如以下的命令进行自动测试：

```bash
./run.sh -o autotest -spp 256 -scene cornell_nospecular -test -ref ./data/cornell_nospecular_ref.txt
```

在 Windows 系统下同理：
```bat
./run.bat -o ref -size 800*600 -spp 2048 -scene cornell_cubemap
```

| 选项 | 作用 |
|----|----------|
| `-o <file>`| 输出图像到 `output/<file>` 目录下 |
| `-size <w>*<h>`| 设置输出图像的宽高 |
| `-spp <spp>`| 设置输出图像中每个像素点的采样数（在 Time Limit 模式下无效） |
| `-j <number>`| 设置程序运行的线程数 |
| `-backup <number>`| 设置每多少张图像做一次备份 |
| `-timelimit <time>`| 打开 Time Limit 模式并设置光追程序的运行时长 |
| `-scene <scenename>`| 设置场景（目前已有场景在下表中） |
| `-ref <file>`| 将 `file`（txt 文件） 作为测试参考的理想收敛情形 |
| `-mis`| 用 MIS 算法进行渲染（默认值） |
| `-lightsis`| 用光源重要性采样进行渲染 |
| `-brdfis`| 用 BRDF 采样进行渲染 |
| `-cosineis`| 用半球余弦采样进行渲染 |
| `-gif`| 输出 gif 图像 |
| `-compress-output`| 使程序输出的内容更窄 |

| 场景 | 描述 |
|----|----------|
| `cornell`| 渐变天空盒材质的 Cornell Box |
| `cornell_cubemap`| Cube Map 天空盒材质的 Cornell Box |
| `cornell_nospecular`| 不含镜面反射材质的 Cornell Box |
| `mis`| 测试 MIS 所用的经典场景 |
| `material`| 仅有 Cube Map 天空盒和一个小球，用于测试材质 |
| `oneweekend`| Ray Tracing in one weekend 的场景（目前玻璃材质渲染有误） |

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
- [x] 实现环境光重要性采样（别名法）
- [ ] 研究并实现 RIS
- [ ] 尝试用 CPU 模拟 Nvidia 的 ReSTIR GI 算法
- [ ] 探索更多的重要性采样算法

### Part 4 - 设计性能比较工具

- [x] 输出采样数增加过程的 GIF 图
- [x] 设计测试器，将每种算法每轮采样的用时、能量和、方差输出至文件中
- [x] 用 matplotlib 绘制曲线，并比较分析
- [ ] 完善视频输出系统，生成多种算法在同一屏幕内比较的视频

### Part 5 - 进一步完善我们的渲染器

- [x] 引入多线程
- [ ] 完善模型读取功能
- [ ] 完善 PBR 材质
- [ ] 搭建漂亮的场景
- [ ] 设计动画渲染，并研究 ReSTIR GI 在动画渲染下的优化

---

以下是 6 月 23 日的版本生成的测试效果图像：

![img](images/gt.png)

Cosine IS：

![img](images/test_CosineIS.png)

BRDF IS：

![img](images/test_BRDFIS.png)

Lights IS：

![img](images/test_LightsIS.png)

MIS：

![img](images/test_MIS.png)