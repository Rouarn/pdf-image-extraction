# PDF 图片提取工具

## 项目概述

PDF 图片提取工具是一个高效的 Python 脚本，专门用于从 PDF 文件中提取所有图片。该工具针对大文件和大量图片进行了优化，确保在处理大型 PDF 文件时能够高效运行并节省内存。

### 主要功能

- 从 PDF 文件中提取所有图片
- 自动去重，避免提取重复图片
- 内存优化，支持处理大型 PDF 文件
- 详细的进度显示和性能统计
- 命令行参数支持，方便集成到其他工作流
- 错误处理，提高脚本的稳定性

## 安装指南

### 环境要求

- Python 3.6 或更高版本
- PyMuPDF 库

### 依赖项安装

1. 确保已安装 Python 3.6 或更高版本
2. 安装 PyMuPDF 库：

```bash
pip install PyMuPDF
```

## 使用说明

### 基本操作流程

1. 克隆或下载本项目到本地
2. 安装所需依赖
3. 运行脚本提取 PDF 中的图片

### 核心功能演示

#### 基本用法

```bash
# 使用默认参数（处理当前目录下的 PDF 文件，输出到 extracted_images 目录）
python pdf_image_extraction.py

# 指定输入 PDF 文件和输出目录
python pdf_image_extraction.py -i input.pdf -o output_images
```

#### 命令行参数

| 参数     | 缩写 | 描述                | 默认值           |
| -------- | ---- | ------------------- | ---------------- |
| --input  | -i   | 输入的 PDF 文件路径 | 梧桐币1000.pdf   |
| --output | -o   | 输出图片的目录      | extracted_images |

### 示例输出

```
Opened PDF with 100 pages.
已提取 1000 张唯一图片... (耗时 5.23 秒)
已提取 2000 张唯一图片... (耗时 10.45 秒)

提取完成!
总共提取了 2500 张唯一图片。
总耗时: 13.67 秒
平均速度: 183.02 张/秒
```

## 项目结构说明

```
pdf-image-extraction/
├── pdf_image_extraction.py    # 主脚本文件
├── 梧桐币1000.pdf            # 示例 PDF 文件
├── extracted_images/         # 提取的图片目录
│   ├── img_00001_xref5.png
│   ├── img_00002_xref6.png
│   └── ...
└── README.md                 # 项目说明文档
```

### 文件说明

- **pdf_image_extraction.py**：主脚本文件，包含提取图片的核心逻辑
- **梧桐币1000.pdf**：示例 PDF 文件，用于测试脚本功能
- **extracted_images/**：默认的图片输出目录，脚本会自动创建

## 配置说明

### 脚本参数配置

脚本支持通过命令行参数进行配置，主要参数包括：

- **-i, --input**：指定输入的 PDF 文件路径
- **-o, --output**：指定输出图片的目录

### 输出文件命名规则

提取的图片文件命名格式为：`img_<序号>_xref<xref值>.<扩展名>`

- `<序号>`：图片的序号，从 1 开始，5 位数字格式
- `<xref值>`：PDF 中图片的交叉引用值，用于去重
- `<扩展名>`：图片的原始扩展名

## 贡献指南

欢迎对本项目进行贡献！如果您有任何改进建议或发现了问题，请通过以下方式参与：

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 许可证信息

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。

## 联系方式

如果您有任何问题或建议，请通过以下方式联系：

- 项目地址：https://github.com/Rouarn/pdf-image-extraction
- 邮箱：die3881123@163.com

---

**注**：本工具仅用于合法目的，请勿用于侵犯他人版权的行为。
