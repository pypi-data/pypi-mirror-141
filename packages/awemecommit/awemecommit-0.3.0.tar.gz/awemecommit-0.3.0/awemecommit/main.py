import json
import os
from pathlib import Path
from typing import Iterable
from collections import OrderedDict

import typer
import click
from click import Context

import questionary
from questionary import Style
import pydoc

from git import Git
import pyperclip
import subprocess
from git.repo import Repo

# 理论上应该搞个模板来解析，为了方便直接硬编码了
# <type>: <subject>
# <BLANK LINE>
# <body>
# <BLANK LINE>
# <meego>

TYPE: OrderedDict = OrderedDict({
    "feat": "增加新的Feature",
    "fix": "修复Bug",
    "pref": "提高性能的代码更改",
    "refactor": "既不是修复bug也不是增加新Feature的代码重构",
    "style": "不影响代码含义的修改, 比如空格、格式化、缺失的分号等",
    "test": "增加确实的测试或者矫正已存在的测试",
    "docs": "仅对注释的修改",
    "build": "对构建系统或者外部依赖项进行了修改",
    "ci": "对CI配置文件或脚本进行了修改"
})

# 缓存路径

CACHE_FILE_PATH = str(Path.home()) + '/Library/Caches/awemecommit'
CACHE_NAME = '/awemecommit_cache.json'

# 缓存
DEFAULT_CACHE = {
    'type': '',
    'subject': '',
    'body': '',
    'meego': ''
}


class OrderedCommands(click.Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        # 修改command默认顺序
        return ['commit', 'owncommit']


app = typer.Typer(cls=OrderedCommands, help='commit message 辅助工具')

# git 相关
top_git_path: str = subprocess.run(
    ['git', 'rev-parse', '--show-toplevel'], capture_output=True).stdout.decode().strip()
if top_git_path == '':
    typer.secho('请在 git 目录下使用本工具',
                fg=typer.colors.RED, err=True)
    exit()

repo = Repo(top_git_path)
git: Git = repo.git
current_branch = git.branch('--show-current')


def safe_run_git(lambda_expr):
    try:
        lambda_expr()
    except Exception as e:
        typer.secho(e.stdout,
                    fg=typer.colors.RED, err=True)
        typer.secho(e.stderr,
                    fg=typer.colors.RED, err=True)
        typer.secho("git 出错, 请查看以上报错信息",
                    fg=typer.colors.RED, err=True)
        raise typer.Abort()


# 缓存输入过的信息
cached_json = DEFAULT_CACHE
cached_file_path = CACHE_FILE_PATH + CACHE_NAME

if not os.path.exists(CACHE_FILE_PATH):
    os.mkdir(CACHE_FILE_PATH)

if not os.path.exists(cached_file_path):
    open(cached_file_path, 'w+').close()

try:
    all_cached_json = json.load(open(cached_file_path, 'r'))
except json.decoder.JSONDecodeError:
    all_cached_json = {}


def save_cached_json():
    with open(cached_file_path, 'w+') as f:
        if top_git_path not in all_cached_json:
            all_cached_json[top_git_path] = {}
        all_cached_json[top_git_path][current_branch] = cached_json
        json.dump(all_cached_json, f)


if os.path.exists(cached_file_path) and top_git_path in all_cached_json and current_branch in all_cached_json[top_git_path]:
    cached_json = all_cached_json[top_git_path][current_branch]
else:
    save_cached_json()


def avoid_keyboard_interrupts(ret):
    if ret is None:
        raise typer.Abort()


@app.command(help='用规范的 message 提交 commit')
def commit(message: str = typer.Option('', '--message', '-m', hidden=True),
           add: bool = typer.Option(
               False, '--add', '-a', help='在仓库根目录 git add .'),
           clipboard: bool = typer.Option(
               False, '--clipboard', '-c', help='将 commit message 复制到剪切板'),
           push: bool = typer.Option(
               False, '--push', '-p', help='创建 commit 后直接push')
           ):
    if message != '':
        typer.secho('禁止使用 --message 提交消息, 请使用本工具生成 commit message!',
                    fg=typer.colors.RED, err=True)
        raise typer.Abort()

    # 查看此时是否有 changes added to commit
    if not add:
        staged_files = git.diff('--name-only', '--cached').strip()
        if staged_files == '':
            typer.secho('没有 changes, 请使用 git add 或者 awemecommit commit --add',
                        fg=typer.colors.RED, err=True)
            raise typer.Abort()

    # 生成 commit_message
    commit_message = get_commit_message()

    # copy 到剪切板
    if clipboard:
        pyperclip.copy(commit_message)
        typer.secho('commit 信息已复制到剪切板!',
                    fg=typer.colors.GREEN, err=True)
        continue_commit = questionary.confirm(
            '是否要继续提交此commit', qmark='', default=True, style=Style([
                ('answer',
                 f'fg:{typer.colors.YELLOW} bold'),
            ])).ask()
        avoid_keyboard_interrupts(continue_commit)
        if not continue_commit:
            raise typer.Exit()

    if add:
        git.add(top_git_path)

    safe_run_git(lambda: git.commit('-m', commit_message))

    typer.secho("git commit 完成!", fg=typer.colors.GREEN)

    if push:
        safe_run_git(lambda: git.push())
        typer.secho("git push 完成!", fg=typer.colors.GREEN)


def get_commit_message():
    commit_type_str = cached_json['type'] + ':' + \
        TYPE[cached_json['type']
             ] if cached_json['type'] != '' else ''
    subject = cached_json['subject']
    body = cached_json['body']
    meego = cached_json['meego']
    commit_message = ''
    while True:
        commit_type_str: str = questionary.select('请选择你的 commit 类型:', choices=[f'{k}:{v}' for k, v in TYPE.items()],
                                                  qmark='', instruction='使用↑↓选择', style=Style([
                                                      ('highlighted',
                                                       f'fg:{typer.colors.GREEN} bold'),
                                                      ('instruction', 'bold'),
                                                      ('answer',
                                                       f'fg:{typer.colors.YELLOW} bold'),
                                                  ]), default=(None if commit_type_str == '' else commit_type_str)).ask()
        avoid_keyboard_interrupts(commit_type_str)
        commit_type = commit_type_str.split(':')[0]
        cached_json['type'] = commit_type
        save_cached_json()

        subject = questionary.text('请输入本次修改的简洁描述, 如需求名, 修复的Bug等:', qmark='', style=Style([
            ('answer',
             f'fg:{typer.colors.YELLOW} bold'),
        ]), default=subject, validate=lambda val: len(val) > 0).ask()
        avoid_keyboard_interrupts(subject)
        cached_json['subject'] = subject
        save_cached_json()

        body_confirm = questionary.confirm(
            '是否有额外信息需要补充, 如修改了哪些组件, 有哪些不兼容的修改, 遗留了哪些问题:', qmark='', default=False, style=Style([
                ('answer',
                 f'fg:{typer.colors.YELLOW} bold'),
            ])).ask()
        avoid_keyboard_interrupts(body_confirm)

        if body_confirm:
            body = questionary.text('补充额外信息:', qmark='', multiline=True, instruction='(结束请输入 Esc 然后输入 Enter)\n', style=Style([
                ('answer',
                    f'fg:{typer.colors.YELLOW} bold'),
            ]), default=body).ask().strip()
            avoid_keyboard_interrupts(body)
            cached_json['body'] = body
            save_cached_json()

        meego = questionary.text('Meego 需求链接或 Bug 链接(需求请在 Meego 中关联技术文档):', qmark='', style=Style([
            ('answer',
             f'fg:{typer.colors.YELLOW} bold'),
        ]), default=meego).ask().strip()
        avoid_keyboard_interrupts(meego)
        cached_json['meego'] = meego
        save_cached_json()

        commit_message = commit_type + ': ' + subject
        if body != '':
            commit_message += f'\n\n{body}\n'
        if meego != '':
            commit_message += f'\nmeego:{meego}'
        all_confirm = questionary.confirm('确认以上 commit message?', qmark='', default=True, style=Style([
            ('answer',
             f'fg:{typer.colors.YELLOW} bold'),
        ])).ask()
        avoid_keyboard_interrupts(all_confirm)
        if all_confirm:
            break
    return commit_message


@app.command(help='查看目前分支上所有新增的 commit, 但不包含 merge 来的')
def owncommit(branch: str = typer.Option('develop', '--branch', '-b', help='作比较的分支')):
    safe_run_git(lambda: pydoc.pager(git.log(f'{branch}..{current_branch}',
                                             '--first-parent', '--no-merges')))


if __name__ == '__main__':
    app()
