# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcov', 'dcov.violationsreporters']

package_data = \
{'': ['*'], 'dcov': ['templates/*']}

install_requires = \
['Jinja2>=2.7.1',
 'Pygments>=2.9.0,<3.0.0',
 'chardet>=3.0.0',
 'pluggy>=0.13.1,<2']

extras_require = \
{':python_version < "3.8"': ['setuptools>=17.0.0'],
 'toml': ['tomli>=1.2.1,<2.0.0']}

entry_points = \
{'console_scripts': ['dcov = dcov.diff_cover_tool:main',
                     'dcov-quality = dcov.diff_quality_tool:main']}

setup_kwargs = {
    'name': 'dcov',
    'version': '1.0.5',
    'description': 'Modify diff algorithm',
    'long_description': 'Diff Coverage\n=============\n\n## 安装\n\n```\npip install dcov\n```\n\n## 使用\n\n不指定报告，则控制台输出 diff 内容，默认对比分支为 origin/main\n\n```\ndcov\n```\n\n指定分支作为对比对象\n\n```\ndcov --compare-branch dev-branch\n```\n\n如果指定报告，则会把 diff 结果和覆盖率报告对比再生成增量覆盖报告。对比规则相对原插件做了改动\n\n- 原插件是根据覆盖率报告作为基础，本插件是根据对比结果作为基础. 例如: 如果对比结果包含的内容没有在覆盖率报告中出现，则视为没有覆盖\n\n```\ndcov --ignore-whitespace --coverage_xml tests/data/cobe.xml \n```\n\n## 开发\n\n下载 poetry\n\n```\npip install poetry\n```\n\n开发\n\n```\ncd <本项目目录>\npoetry run dcov\n```\n\n打包\n\n```\npoetry build\n```\n安装\n\n```\npoetry install\n```\n\n发布\n```\n# 自动推送到 pypi, 如果有旧版本存在，需要先修改 pyproject.toml 中的 version\npoetry publish --build\n```\n\n更多功能\n\n```\npoetry --help\n```\n\n## 贡献\n\n欢迎提交 PR\n\n## 感谢\n\nDiff Coverage is forked from [diff_cover](https://github.com/Bachmann1234/diff_cover) and add some features\n\n',
    'author': 'See Contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xiak/dcov',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
