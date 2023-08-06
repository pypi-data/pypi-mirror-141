# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_morning']

package_data = \
{'': ['*'], 'nonebot_plugin_morning': ['resource/*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot2>=2.0.0-beta.2,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-morning',
    'version': '0.2.2',
    'description': 'Good morning & good night!',
    'long_description': '<div align="center">\n\n# Good Morning\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_🌈 おはよう！ 🌈_\n<!-- prettier-ignore-end -->\n\n</div>\n<p align="center">\n  \n  <a href="https://github.com/KafCoppelia/nonebot_plugin_morning/blob/beta/LICENSE">\n    <img src="https://img.shields.io/badge/license-MIT-informational">\n  </a>\n  \n  <a href="https://github.com/nonebot/nonebot2">\n    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2-green">\n  </a>\n  \n  <a href="">\n    <img src="https://img.shields.io/badge/release-v0.2.2-orange">\n  </a>\n  \n</p>\n\n</p>\n\n## 版本\n\nv0.2.2\n\n⚠ 适配nonebot2-2.0.0beta.2；\n\n👉 适配alpha.16版本参见[alpha.16分支](https://github.com/KafCoppelia/nonebot_plugin_morning/tree/alpha.16)\n\n[更新日志](https://github.com/KafCoppelia/nonebot_plugin_morning/releases/tag/v0.2.2)\n\n## 安装\n\n1. 通过`pip`或`nb`安装，版本指定`0.2.2`；\n\n2. 用户数据`data.json`及早晚安配置文件`config.json`位于`./resource`下，可在`env`内设置`MORNING_PATH`更改：\n\n    ```python\n    MORNING_PATH="your-path-to-resource"\n    ```\n\n## 功能\n\n1. 和Bot说早晚安，记录睡眠时间，培养良好作息；\n\n2. 群管及超管可设置早安时限、晚安时限、优质睡眠、深度睡眠等；\n\n3. 分群管理群友作息；\n\n4. おはよう！🌈\n\n## 命令\n\n1. 早晚安：早安/晚安，记录睡眠时间；\n\n2. 查看我的作息：我的作息；\n\n3. 查看群友作息：群友作息，看看今天几个人睡觉或起床了；\n\n4. 查看配置当前安晚安规则：早晚安设置；\n\n5. [群管或群主或超管] 设置命令\n\n    - 开启/关闭某个配置：早安/晚安开启/关闭某项功能；\n\n    - 早安/晚安设置：设置功能的参数；\n\n    - 详见规则配置；\n\n## 规则配置\n\n`confg.json`文件已默认写入下述配置，当其不存在时则默认下载仓库的预置配置文件：\n\n```python\n{\n    "morning": {\n        "get_up_intime": {      # 是否只能在规定时间起床\n            "enable": true,     # 默认开启，若关闭则下面两项无效\n            "early_time": 6,    # 允许的最早的起床时间，默认早上6点\n            "late_time": 12     # 允许的最晚的起床时间，默认中午12点\n        },\n        "multi_get_up": {       # 是否允许多次起床\n            "enable": false,    # 默认不允许，若允许则下面一项无效\n            "interval": 6       # 两次起床间隔的时间，小于这个时间就不允许起床\n        },\n        "super_get_up": {       # 是否允许超级亢奋\n            "enable": false,    # 默认不允许，若允许则下面一项无效\n            "interval": 3       # 这次起床和上一次睡觉的时间间隔，小于这个时间就不允许起床，不怕猝死？给我睡！\n        }\n    },\n    "night": {\n        "sleep_intime": {       # 是否只能在规定时间睡觉\n            "enable": true,     # 默认开启，若关闭则下面两项无效\n            "early_time": 21,   # 允许的最早的睡觉时间，默认晚上21点\n            "late_time": 6      # 允许的最晚的睡觉时间，默认次日早上6点\n        },\n        "good_sleep": {         # 是否开启优质睡眠\n            "enable": true,     # 默认开启，若关闭则下面一项无效\n            "interval": 6       # 两次睡觉间隔的时间，小于这个时间就不允许睡觉\n        },\n        "deep_sleep": {         # 是否允许深度睡眠\n            "enable": false,    # 默认不允许，若允许则下面一项无效\n            "interval": 3       # 这次睡觉和上一次起床的时间间隔，小于这个时间就不允许睡觉，睡个锤子，快起床！\n        }\n    }\n}\n```\n\n1. 默认配置（如上）\n\n    - 早安：\n\n      是否要求规定时间内起床：是\n\n      是否允许连续多次起床：否\n\n      是否允许超级亢奋(即睡眠时长很短)：否\n\n    - 晚安：\n\n      是否要求规定时间内睡觉：是\n\n      是否开启优质睡眠：是\n      \n      是否允许深度睡眠(即清醒时长很短)：否\n\n2. 早安配置\n    \n    - [早安开启 xx] 开启某个配置选项，xx可选值目前有 [时限 / 多重起床 / 超级亢奋]；\n    \n    - [早安关闭 xx] 关闭某个配置选项，xx可选值目前有 [时限 / 多重起床 / 超级亢奋]；\n    \n    - [早安设置 xx x] 设置某个配置的参数，xx可选值目前有 [时限 / 多重起床 / 超级亢奋]，x可选值为0到24的整数；\n      \n      ※ 当设置时限时需要两个参数，命令为：[早安设置 时限 x y]，当不是时限时只需一个参数，命令为：[早安设置 xx x]\n\n3. 晚安配置\n    \n    - [晚安开启 xx] 开启某个配置选项，xx可选值目前有 [时限 / 优质睡眠 / 深度睡眠]；\n    \n    - [晚安关闭 xx] 关闭某个配置选项，xx可选值目前有 [时限 / 优质睡眠 / 深度睡眠]；\n    \n    - [晚安设置 xx x] 设置某个配置的参数，xx可选值目前有 [时限 / 优质睡眠 / 深度睡眠]，x可选值为0到24的整数；\n      \n      ※ 当设置时限时需要两个参数，命令为：[晚安设置 时限 x y]，当不是时限时只需一个参数，命令为：[晚安设置 xx x]\n\n## 本插件改自\n\n[hoshinobot-good_morning](https://github.com/azmiao/good_morning)\n\n1. 修改代码结构；\n\n2. 修改部分配置名称、功能，修改群组数据储存格式；\n\n3. 参考并修改配置部分README；',
    'author': 'KafCoppelia',
    'author_email': 'k740677208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
