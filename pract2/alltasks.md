# Задание 1

Получение служебной информации о пакете

Команда:
unzip -p matplotlib-3.11.2-cp315-cp315t-musllinux_1_2_x86_64.whl 'matplotlib-3.11.2.dist-info/METADATA' | head -20
Результат:
```python
Metadata-Version: 2.1
Name: matplotlib
Version: 3.11.2
Summary: Python plotting package
Author: John D. Hunter, Michael Droettboom
Author-Email: Unknown <matplotlib-users@python.org>
License: License agreement for matplotlib versions 1.3.0 and later
         =========================================================

         1. This LICENSE AGREEMENT is between the Matplotlib Development Team
         ("MDT"), and the Individual or Organization ("Licensee") accessing and
         otherwise using matplotlib software in source or binary form and its
         associated documentation.

         2. Subject to the terms and conditions of this License Agreement, MDT
         hereby grants Licensee a nonexclusive, royalty-free, world-wide license
         to reproduce, analyze, test, perform and/or display publicly, prepare
         derivative works, distribute, and otherwise use matplotlib
         alone or in any derivative version, provided, however, that MDT's
         License Agreement and MDT's notice of copyright, i.e., "Copyright (c)
```

Пакет без менеджера пакетов можно получить скачав его дистрибутив напрямую из репозитория PyPI или взяв исходники из репозитория проекта на гитхабе
curl -O https://files.pythonhosted.org/packages/7b/30/687ccce22f66a57fed85942450e88062773bcbf1a42914e70c7148ec71dc/matplotlib-3.11.2-cp315-cp315t-musllinux_1_2_x86_64.whl



# Задание 2

Получение служебной информации о пакете

Команда:
tar -xzOf express-4.22.3.tgz package/package.json | head -60
Результат:
```json
{
  "name": "express",
  "description": "Fast, unopinionated, minimalist web framework",
  "version": "4.22.3",
  "author": "TJ Holowaychuk <tj@vision-media.ca>",
  "contributors": [
    "Aaron Heckmann <aaron.heckmann+github@gmail.com>",
    "Ciaran Jessup <ciaranj@gmail.com>",
    "Douglas Christopher Wilson <doug@somethingdoug.com>",
    "Guillermo Rauch <rauchg@gmail.com>",
    "Jonathan Ong <me@jongleberry.com>",
    "Roman Shtylman <shtylman+expressjs@gmail.com>",
    "Young Jae Sim <hanul@hanul.me>"
  ],
  "license": "MIT",
  "repository": "expressjs/express",
  "homepage": "http://expressjs.com/",
  "funding": {
    "type": "opencollective",
    "url": "https://opencollective.com/express"
  },
  "keywords": [
    "express",
    "framework",
    "sinatra",
    "web",
    "http",
    "rest",
    "restful",
    "router",
    "app",
    "api"
  ],
  "dependencies": {
    "accepts": "~1.3.8",
    "array-flatten": "1.1.1",
    "body-parser": "~1.20.5",
    "content-disposition": "~0.5.4",
    "content-type": "~1.0.4",
    "cookie": "~0.7.1",
    "cookie-signature": "~1.0.6",
    "debug": "2.6.9",
    "depd": "2.0.0",
    "encodeurl": "~2.0.0",
    "escape-html": "~1.0.3",
    "etag": "~1.8.1",
    "finalhandler": "~1.3.1",
    "fresh": "~0.5.2",
    "http-errors": "~2.0.0",
    "merge-descriptors": "1.0.3",
    "methods": "~1.1.2",
    "on-finished": "~2.4.1",
    "parseurl": "~1.3.3",
    "path-to-regexp": "~0.1.13",
    "proxy-addr": "~2.0.7",
    "qs": "~6.16.0",
    "range-parser": "~1.2.1",
    "safe-buffer": "5.2.1",
    "send": "~0.19.0",
    "serve-static": "~1.16.2"
```

Пакет без менеджера пакетов можно получить скачав его tarball-архив напрямую из реестра npm или взяв исходники из репозитория проекта на гитхабе или другом репозитории.
curl -O https://registry.npmjs.org/express/-/express-4.22.3.tgz



# Задание 3

Код двух баш файлов для создания png где изображены зависимости matplotlib и express

express
```bash
python3 -c "import json; print('\n'.join(json.load(open('express-package.json'))['dependencies'].keys()))" > deps-express.txt

{
  echo 'digraph express_deps {'
  echo '    rankdir=LR;'
  echo '    node [shape=box, style="rounded,filled", fillcolor="#e8e8e8"];'
  echo '    "express" [fillcolor="#cf17e0", fontcolor=black];'
  while read -r d; do
    [ -z "$d" ] && continue
    echo "    \"express\" -> \"$d\";"
  done < deps-express.txt
  echo '}'
} > express-deps.dot

dot -Tpng express-deps.dot -o express-deps.png
```
matplotlib
```bash
unzip -p matplotlib-*.whl '*/METADATA' | grep '^Requires-Dist:' | sed 's/Requires-Dist: //; s/[<>=!;\[].*//; s/ *$//' > deps-matplotlib.txt

{
  echo 'digraph matplotlib_deps {'
  echo '    rankdir=LR;'
  echo '    node [shape=box, style="rounded,filled", fillcolor="#e8e8e8"];'
  echo '    "matplotlib" [fillcolor="#cf17e0", fontcolor=black];'
  while read -r d; do
    [ -z "$d" ] && continue
    echo "    \"matplotlib\" -> \"$d\";"
  done < deps-matplotlib.txt
  echo '}'
} > matplotlib-deps.dot

dot -Tpng matplotlib-deps.dot -o matplotlib-deps.png
```
# Задание 4

Код для поиска счастливого билета в MiniZinc
```mzn
include "all_different.mzn";

var 0..9: A;
var 0..9: B;
var 0..9: C;
var 0..9: D;
var 0..9: E;
var 0..9: F;

constraint A + B + C = D + E + F;

constraint all_different([A, B, C, D, E, F]);

solve minimize A + B + C;

output ["Билет: \(A)\(B)\(C) \(D)\(E)\(F)\n", "Сумма трех цифр: \(A + B + C)\n"];
```

Результат
Билет: 620 431
Сумма трех цифр: 8

# Задание 5

Код для решения задачи о зависимости пакетов
```mzn
var 1..6: menu;        % 1=1.0.0, 2=1.1.0, 3=1.2.0, 4=1.3.0, 5=1.4.0, 6=1.5.0
var 1..5: dropdown;    % 1=1.8.0, 2=2.0.0, 3=2.1.0, 4=2.2.0, 5=2.3.0
var 1..2: icons;       % 1=1.0.0, 2=2.0.0

constraint (menu == 1) -> (dropdown == 1);
constraint (menu >= 2 /\ menu <= 6) -> (dropdown >= 2 /\ dropdown <= 5);

constraint (dropdown >= 2 /\ dropdown <= 5) -> (icons == 2);

constraint icons == 1;

solve satisfy;

output ["Menu: \(menu)\n", "Dropdown: \(dropdown)\n", "Icons: \(icons)\n"];
```
Результат
Menu: 1
Dropdown: 1
Icons: 1

# Задание 6

Код для решения задачи о зависимости пакетов
```mzn
var 1..2: foo;      % 1=1.0.0, 2=1.1.0
var 1..2: target;   % 1=1.0.0, 2=2.0.0
var 1..1: left;     % 1=1.0.0
var 1..1: right;    % 1=1.0.0
var 1..2: shared;   % 1=1.0.0, 2=2.0.0

constraint foo >= 1 /\ foo <= 2;
constraint target == 2;
constraint (foo == 2) -> (left == 1);
constraint (foo == 2) -> (right == 1);
constraint (left == 1) -> (shared >= 1);
constraint (right == 1) -> (shared <= 1);
constraint (shared == 1) -> (target == 1);

solve satisfy;

output ["foo     = \(foo)\n", "target  = \(target)\n", "left    = \(left)\n", "right   = \(right)\n", "shared  = \(shared)\n"];
```
Результат
=====UNSATISFIABLE=====

# Задание 7

Код для решения задачи

```python
data = {
    "root": {
        "1.0.0": {"foo": "^1.0.0", "target": "^2.0.0"}
    },
    "foo": {
        "1.0.0": {},
        "1.1.0": {"left": "^1.0.0", "right": "^1.0.0"}
    },
    "target": {
        "1.0.0": {},
        "2.0.0": {}
    },
    "left": {
        "1.0.0": {"shared": ">=1.0.0"}
    },
    "right": {
        "1.0.0": {"shared": "<2.0.0"}
    },
    "shared": {
        "1.0.0": {"target": "^1.0.0"},
        "2.0.0": {}
    }
}



from data import data

def parse_version(v):
    return tuple(int(x) for x in v.split("."))

def matches_range(version, range_str):
    v = parse_version(version)
    if range_str.startswith("^"):
        base = parse_version(range_str[1:])
        upper = (base[0] + 1, 0, 0)
        return base <= v < upper
    elif range_str.startswith(">="):
        return v >= parse_version(range_str[2:])
    elif range_str.startswith("<"):
        return v < parse_version(range_str[1:])
    else:
        return v == parse_version(range_str)

pkg_versions = {p: sorted(d.keys(), key=parse_version) for p, d in data.items()}

pkg_index = {p: {v: i + 1 for i, v in enumerate(vs)} for p, vs in pkg_versions.items()}


lines = []

for pkg, versions in pkg_versions.items():
    max_idx = len(versions)
    comment = ", ".join(f"{i+1}={v}" for i, v in enumerate(versions))
    lines.append(f"var 0..{max_idx}: {pkg};  % 0=не установлен, {comment}")

lines.append("")

lines.append("constraint root == 1;\n")

for pkg, versions in data.items():
    for version, deps in versions.items():
        pkg_idx = pkg_index[pkg][version]
        for dep_name, rng in deps.items():
            allowed = [pkg_index[dep_name][dv]
                       for dv in pkg_versions[dep_name]
                       if matches_range(dv, rng)]
            if allowed:
                allowed_str = " \\/ ".join(f"{dep_name} == {a}" for a in allowed)
                lines.append(f"constraint ({pkg} == {pkg_idx}) -> ({allowed_str});")
            else:
                lines.append(f"constraint {pkg} != {pkg_idx};")

lines.append("\nsolve satisfy;\n")

lines.append("output [")
for pkg, versions in pkg_versions.items():
    parts = [f'if fix({pkg}) == 0 then "не установлен"']
    for i, v in enumerate(versions, start=1):
        parts.append(f'elseif fix({pkg}) == {i} then "{v}"')
    parts.append('else "?" endif')
    expr = " ".join(parts)
    lines.append(f'    "{pkg} = " ++ ({expr}) ++ "\\n",')
lines.append("];")

with open("packages_auto.mzn", "w") as f:
    f.write("\n".join(lines))

print("Сложили packages_auto.mzn")
```

Результат
Создан файл packages_auto.mzn 
При проверке его через minizinc packages_auto.mzn получается
root = 1.0.0
foo = 1.0.0
target = 2.0.0
left = не установлен
right = не установлен
shared = не установлен
