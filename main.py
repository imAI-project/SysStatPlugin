from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

import os
import psutil


# 注册插件
@register(name="SysStat", description="查看系统状态", version="0.1", author="RockChinQ")
class SysStatPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        pass

    @on(GroupCommandSent)
    @on(PersonCommandSent)
    def command_send(self, host: PluginHost, event: EventContext, command: str, **kwargs):
        if command == "sysstat" or command == "sys":
            event.prevent_default()
            event.prevent_postorder()

            core_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            sysmem_info = psutil.virtual_memory()
            cpu_info = psutil.cpu_times
            disk_info = psutil.disk_usage('/')
            cpu_ststs = psutil.cpu_stats()
            cpu_freq = psutil.cpu_freq()
            
            res = f"""====系统状态====
进程内存占用: {core_mem:.2f}MB
总内存: {sysmem_info.total / 1024 / 1024:.2f}MB
已用内存: {sysmem_info.used / 1024 / 1024:.2f}MB
空闲内存: {sysmem_info.free / 1024 / 1024:.2f}MB
内存使用率: {sysmem_info.percent:.2f}%
用户态CPU时间: {cpu_info().user:.2f}秒
系统态CPU时间: {cpu_info().system:.2f}秒
空闲CPU时间: {cpu_info().idle:.2f}秒
CPU使用率: {psutil.cpu_percent(interval=1):.2f}%
CPU逻辑核心数: {psutil.cpu_count()}
CPU物理核心数: {psutil.cpu_count(logical=False)}
CPU当前频率: {cpu_freq.current:.2f}MHz
总磁盘空间: {disk_info.total / 1024 / 1024 / 1024:.2f}GB
已用磁盘空间: {disk_info.used / 1024 / 1024 / 1024:.2f}GB
空闲磁盘空间: {disk_info.free / 1024 / 1024 / 1024:.2f}GB
磁盘使用率: {disk_info.percent:.2f}%
============"""

            event.add_return(
                "reply",
                [res.strip()]
            )

    # 插件卸载时触发
    def __del__(self):
        pass
