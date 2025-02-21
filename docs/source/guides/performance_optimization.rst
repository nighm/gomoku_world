性能优化指南
========

本指南提供了优化五子棋世界项目性能的最佳实践和建议。

AI性能优化
--------

算法优化
~~~~~~~

优化AI算法性能::

    # 使用Alpha-Beta剪枝
    def minmax_with_pruning(board, depth, alpha, beta, maximizing):
        if depth == 0 or is_terminal(board):
            return evaluate_position(board)
            
        if maximizing:
            value = float('-inf')
            for move in get_valid_moves(board):
                value = max(value, minmax_with_pruning(
                    make_move(board, move),
                    depth - 1,
                    alpha,
                    beta,
                    False
                ))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta剪枝
            return value
        else:
            # ... 类似的最小化代码

并行计算
~~~~~~~

利用多核处理器::

    from concurrent.futures import ProcessPoolExecutor
    
    def parallel_evaluation(positions):
        with ProcessPoolExecutor() as executor:
            return list(executor.map(evaluate_position, positions))

缓存策略
~~~~~~~

实现位置评估缓存::

    from functools import lru_cache
    
    @lru_cache(maxsize=1000)
    def cached_evaluate_position(board_hash):
        return evaluate_position(board_hash)

GUI性能优化
---------

渲染优化
~~~~~~~

优化棋盘渲染::

    class BoardCanvas:
        def __init__(self):
            self._cache = {}
            self._dirty = True
        
        def redraw(self):
            if not self._dirty:
                return
                
            # 只重绘变化的部分
            for x, y in self._changed_cells:
                self._redraw_cell(x, y)
            
            self._dirty = False
            self._changed_cells.clear()

事件处理
~~~~~~~

优化事件处理::

    def handle_mouse_event(self, event):
        # 使用事件节流
        if time.time() - self._last_event_time < 0.016:  # 约60FPS
            return
            
        self._last_event_time = time.time()
        # 处理事件...

内存管理
~~~~~~~

减少内存使用::

    class GameState:
        __slots__ = ['board', 'current_player', 'moves']
        
        def __init__(self):
            self.board = numpy.zeros((15, 15), dtype=numpy.int8)
            self.current_player = 1
            self.moves = []

网络性能优化
---------

连接池
~~~~~

使用连接池管理网络连接::

    class ConnectionPool:
        def __init__(self, max_size=10):
            self._pool = []
            self._max_size = max_size
        
        async def get_connection(self):
            if self._pool:
                return self._pool.pop()
            return await create_connection()
        
        async def release_connection(self, conn):
            if len(self._pool) < self._max_size:
                self._pool.append(conn)
            else:
                await conn.close()

消息压缩
~~~~~~~

压缩网络消息::

    import zlib
    
    def compress_message(message):
        return zlib.compress(json.dumps(message).encode())
    
    def decompress_message(data):
        return json.loads(zlib.decompress(data).decode())

协议优化
~~~~~~~

优化网络协议::

    # 使用二进制协议
    class BinaryProtocol:
        def encode_move(self, x, y):
            return struct.pack('!BB', x, y)
        
        def decode_move(self, data):
            return struct.unpack('!BB', data)

数据库优化
--------

索引优化
~~~~~~~

优化数据库索引::

    # 创建合适的索引
    CREATE INDEX idx_game_timestamp ON games(timestamp);
    CREATE INDEX idx_player_rating ON players(rating DESC);
    
    # 使用复合索引
    CREATE INDEX idx_game_player ON games(player_id, timestamp);

查询优化
~~~~~~~

优化数据库查询::

    # 使用批量操作
    def save_moves(moves):
        with connection.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO moves (game_id, x, y, player) VALUES (?, ?, ?, ?)",
                moves
            )

连接池
~~~~~

使用数据库连接池::

    from dbutils.pooled_db import PooledDB
    
    pool = PooledDB(
        creator=pymysql,
        maxconnections=10,
        mincached=2,
        maxcached=5
    )

资源管理
-------

图像资源
~~~~~~~

优化图像资源::

    class ImageManager:
        def __init__(self):
            self._cache = {}
            
        def load_image(self, path):
            if path in self._cache:
                return self._cache[path]
                
            image = Image.open(path)
            image.load()  # 预加载到内存
            self._cache[path] = image
            return image

音频资源
~~~~~~~

优化音频资源::

    class SoundManager:
        def __init__(self):
            self._cache = {}
            self._current_size = 0
            self._max_size = 50 * 1024 * 1024  # 50MB
            
        def load_sound(self, path):
            if path in self._cache:
                return self._cache[path]
                
            if self._current_size > self._max_size:
                self._cleanup_cache()
                
            sound = pygame.mixer.Sound(path)
            self._cache[path] = sound
            self._current_size += sound.get_length() * 44100 * 2
            return sound

内存管理
~~~~~~~

内存使用优化::

    import gc
    
    def optimize_memory():
        # 触发垃圾回收
        gc.collect()
        
        # 减少内存碎片
        gc.set_threshold(700, 10, 5)
        
        # 监控内存使用
        process = psutil.Process()
        memory_info = process.memory_info()
        
        if memory_info.rss > 500 * 1024 * 1024:  # 500MB
            cleanup_caches()

监控和分析
--------

性能监控
~~~~~~~

实现性能监控::

    from prometheus_client import Counter, Histogram
    
    # 定义指标
    MOVE_TIME = Histogram('ai_move_time_seconds', 'Time taken for AI moves')
    RENDER_TIME = Histogram('gui_render_time_seconds', 'Time taken for rendering')
    NETWORK_LATENCY = Histogram('network_latency_seconds', 'Network request latency')
    
    # 使用指标
    @MOVE_TIME.time()
    def get_ai_move(board):
        return ai.get_move(board)

性能分析
~~~~~~~

使用性能分析工具::

    import cProfile
    import pstats
    
    def profile_game():
        profiler = cProfile.Profile()
        profiler.enable()
        
        # 运行游戏...
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats()

日志优化
~~~~~~~

优化日志性能::

    import logging
    from logging.handlers import RotatingFileHandler
    
    # 使用异步日志处理器
    handler = RotatingFileHandler(
        'game.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    
    # 批量处理日志
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

调试工具
-------

性能调试
~~~~~~~

添加性能调试工具::

    class PerformanceDebugger:
        def __init__(self):
            self.fps_counter = 0
            self.frame_times = []
            self.last_time = time.time()
        
        def update(self):
            current_time = time.time()
            frame_time = current_time - self.last_time
            self.frame_times.append(frame_time)
            
            if len(self.frame_times) > 60:
                self.frame_times.pop(0)
            
            self.fps_counter += 1
            if current_time - self.last_time >= 1.0:
                self.fps = self.fps_counter
                self.fps_counter = 0
                self.last_time = current_time

内存调试
~~~~~~~

添加内存调试工具::

    class MemoryDebugger:
        def __init__(self):
            self.snapshots = []
        
        def take_snapshot(self):
            snapshot = {
                'time': time.time(),
                'memory': psutil.Process().memory_info().rss,
                'objects': len(gc.get_objects())
            }
            self.snapshots.append(snapshot)
        
        def analyze(self):
            for i in range(1, len(self.snapshots)):
                prev = self.snapshots[i-1]
                curr = self.snapshots[i]
                print(f"Memory change: {curr['memory'] - prev['memory']} bytes")
                print(f"Object count change: {curr['objects'] - prev['objects']}")

持续优化
-------

性能测试
~~~~~~~

编写性能测试::

    import pytest
    
    @pytest.mark.benchmark
    def test_ai_performance(benchmark):
        board = create_test_board()
        
        result = benchmark(lambda: ai.get_move(board))
        
        assert result is not None
        assert benchmark.stats.stats.mean < 0.1  # 100ms

性能监控
~~~~~~~

实现持续性能监控::

    class PerformanceMonitor:
        def __init__(self):
            self.metrics = {}
            
        def record_metric(self, name, value):
            if name not in self.metrics:
                self.metrics[name] = []
            self.metrics[name].append({
                'value': value,
                'timestamp': time.time()
            })
        
        def analyze_trends(self):
            for name, values in self.metrics.items():
                trend = calculate_trend(values)
                if trend > threshold:
                    alert_performance_degradation(name, trend)

自动优化
~~~~~~~

实现自动优化机制::

    class AutoOptimizer:
        def __init__(self):
            self.optimizations = []
            
        def check_and_optimize(self):
            current_performance = measure_performance()
            
            if current_performance < threshold:
                for optimization in self.optimizations:
                    if optimization.should_apply(current_performance):
                        optimization.apply()
                        
                        new_performance = measure_performance()
                        if new_performance > current_performance:
                            log_successful_optimization(optimization)
                        else:
                            optimization.rollback() 