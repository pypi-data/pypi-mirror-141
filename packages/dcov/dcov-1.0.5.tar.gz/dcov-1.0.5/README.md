Diff Coverage
=============

## 安装

```
pip install dcov
```

## 使用

不指定报告，则控制台输出 diff 内容，默认对比分支为 origin/main

```
dcov
```

指定分支作为对比对象

```
dcov --compare-branch dev-branch
```

如果指定报告，则会把 diff 结果和覆盖率报告对比再生成增量覆盖报告。对比规则相对原插件做了改动

- 原插件是根据覆盖率报告作为基础，本插件是根据对比结果作为基础. 例如: 如果对比结果包含的内容没有在覆盖率报告中出现，则视为没有覆盖

```
dcov --ignore-whitespace --coverage_xml tests/data/cobe.xml 
```

## 开发

下载 poetry

```
pip install poetry
```

开发

```
cd <本项目目录>
poetry run dcov
```

打包

```
poetry build
```
安装

```
poetry install
```

发布
```
# 自动推送到 pypi, 如果有旧版本存在，需要先修改 pyproject.toml 中的 version
poetry publish --build
```

更多功能

```
poetry --help
```

## 贡献

欢迎提交 PR

## 感谢

Diff Coverage is forked from [diff_cover](https://github.com/Bachmann1234/diff_cover) and add some features

