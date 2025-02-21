开发指南
========

本指南将帮助您参与五子棋世界（Gomoku World）的开发。

开发环境设置
----------

1. 克隆代码
~~~~~~~~~

首先克隆项目代码::

    git clone https://github.com/nighm/gomoku_world.git
    cd gomoku_world

2. 安装依赖
~~~~~~~~~

安装开发依赖::

    # 使用pip
    pip install -e ".[dev,docs]"
    
    # 或使用Poetry
    poetry install --with dev,docs

3. 配置pre-commit
~~~~~~~~~~~~~~~

安装pre-commit钩子::

    pre-commit install

代码规范
-------

1. 代码风格
~~~~~~~~~

我们使用以下工具确保代码质量：

* black：代码格式化
* isort：导入语句排序
* flake8：代码风格检查
* mypy：类型检查
* pylint：代码分析
* bandit：安全检查

运行代码检查::

    # 使用tox运行所有检查
    tox
    
    # 或单独运行
    black src tests
    isort src tests
    flake8 src tests
    mypy src tests
    pylint src tests
    bandit -r src

2. 文档规范
~~~~~~~~~

* 使用Google风格的文档字符串
* 所有公共API都需要文档
* 包含中英文注释
* 示例代码需要可运行

测试规范
-------

1. 单元测试
~~~~~~~~~

使用pytest编写测试::

    def test_board_initialization():
        board = Board(size=15)
        assert board.size == 15
        assert len(board.board) == 15

运行测试::

    # 运行所有测试
    pytest
    
    # 运行特定测试
    pytest tests/test_board.py
    
    # 运行带覆盖率报告的测试
    pytest --cov=gomoku_world

2. 性能测试
~~~~~~~~~

使用pytest-benchmark进行性能测试::

    @pytest.mark.benchmark
    def test_ai_performance(benchmark):
        def ai_move():
            board = Board()
            ai = AI()
            return ai.get_move(board, 1)
        
        benchmark(ai_move)

提交代码
-------

1. 分支管理
~~~~~~~~~

* main：主分支，只接受合并请求
* develop：开发分支，日常开发工作
* feature/*：新功能分支
* bugfix/*：错误修复分支
* release/*：发布分支

2. 提交规范
~~~~~~~~~

提交信息格式::

    <类型>(<范围>): <描述>
    
    <详细描述>
    
    <相关问题>

类型包括：

* feat：新功能
* fix：错误修复
* docs：文档更新
* style：代码风格更改
* refactor：代码重构
* perf：性能优化
* test：测试相关
* chore：构建过程或辅助工具的变动

3. 合并请求
~~~~~~~~~

* 创建合并请求前先更新分支
* 确保所有测试通过
* 完成代码审查
* 解决所有评论
* 等待CI检查通过

发布流程
-------

1. 版本管理
~~~~~~~~~

使用语义化版本::

    MAJOR.MINOR.PATCH

例如：1.0.0, 1.1.0, 1.1.1

2. 发布步骤
~~~~~~~~~

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建发布分支
4. 运行测试套件
5. 构建文档
6. 创建标签
7. 发布到PyPI

发布命令::

    # 构建
    python -m build
    
    # 上传到PyPI
    python -m twine upload dist/*

持续集成
-------

我们使用GitHub Actions进行CI/CD：

* 代码检查
* 单元测试
* 性能测试
* 文档构建
* 自动发布

配置文件位于：.github/workflows/

Docker开发
--------

使用Docker进行开发::

    # 构建开发环境
    docker build -f ci/docker/Dockerfile.dev -t gomoku_world:dev .
    
    # 运行开发容器
    docker run -it --rm -v $(pwd):/app gomoku_world:dev

贡献指南
-------

1. 选择任务
2. 创建分支
3. 编写代码
4. 添加测试
5. 更新文档
6. 提交代码
7. 创建合并请求

详细信息请参考：CONTRIBUTING.md 