import re
import itertools
import pyperclip as cl
from typing import NamedTuple, List, Union


class MarkdownText():
    def __init__(self, level: int, text: str, section: str = None) -> None:
        self.level = level
        self.text = text
        self.section = section

    # def __str__(self) -> str:
    #     return f'''({self.level},
    #             {self.text},
    #             {self.section})'''

    def to_markdown_text(self) -> str:
        if self.level > 0 and self.text.rstrip():
            # インデント 0以上かつ中身があれば
            return '*' * self.level + ' ' + self.text
        if self.level == 0:
            return self.text

    def to_indent_text(self, indent: str) -> str:
        ret = indent * self.level + self.text
        return ret


def get_section(text: str, before_section: str = None) -> Union[str, None]:
    """セクションを返す

    Parameters
    ----------
    text : str
        行

    Returns
    -------
    str
        セクションの種類( pre, ...)
    """
    if '<>' in text:
        return 'pre'
    elif before_section is not None:
        if f'</{before_section}>' in text:
            # sectionが閉じられた
            return None
        else:
            # sectionが閉じられていない
            return before_section
    else:
        return None


def _to_mdt_list(lines: List[str], level_word: str, line_pattern: str, return_ends: str) -> List[MarkdownText]:
    
    re_level = re.compile(line_pattern) # [マークダウン部, その他] の正規表現

    ret: List[MarkdownText] = []
    next_level = None
    section = None
    level = None
    
    for l in lines:
        section = get_section(l, section)

        level_match = re_level.findall(l)

        if level_match:
            # レベルがある場合
            level_match = list(itertools.chain.from_iterable(level_match)) # flatten

            if next_level is not None:
                level = next_level
                next_level = None
            else:
                level = level_match[0].count(level_word) # レベルを数える

            text = level_match[1]
            
        else:
            # レベルが無い場合
            level = 0
            text = l

        if l.endswith(return_ends):
            next_level = 0

        ret.append(MarkdownText(level, text))

    return ret

def to_markdown_mdt_list(lines: List[str]) -> List[MarkdownText]:
    """
    マークダウンの文字列を含むリストを、MarkdownText オブジェクトにして返す
        * マークダウンレベル用の文字: 「*」
        * 同じレベルでの改行文字: 「  *」

    Parameters
    ----------
    lines : List[str]
        マークダウンの文字列を含むリスト

    Returns
    -------
    List[MarkdownText]

    """

    level_word = '\t' # マークダウンの記号
    return_ends = '  \r\n'
    line_pattern = fr'(^{level_word}+)(.*)' # [マークダウン部, その他] の正規表現
    ret = _to_mdt_list(lines, level_word, line_pattern, return_ends)

    return ret

if __name__=='__main__':

    indent = '\t'

    clipbord_text = cl.paste()
    # 行ごとにsplit
    clipbord_text = clipbord_text.splitlines(keepends=True)
    
    mdt_list = to_markdown_mdt_list(clipbord_text)

    results = ''
    for mdt in mdt_list:
        results += mdt.to_markdown_text()

    cl.copy(results)
