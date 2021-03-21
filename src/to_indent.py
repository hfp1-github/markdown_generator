

import re
import itertools
import pyperclip as cl
from typing import NamedTuple, List

class MarkdownText(NamedTuple):
    level: int # マークダウンレベル
    text: str # レベル部以外のテキスト

def mdt_to_indent_text(mt: MarkdownText, indent: str):
    ret = indent * mt.level + mt.text
    return ret

def to_indent_mdt_list(lines: List[str]) -> List[MarkdownText]:
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

    level_word = r'*' # マークダウンの記号
    return_ends = '  \r\n'
    re_level = re.compile(fr'(^\{level_word}+\s)(.*)') # [マークダウン部, その他] の正規表現

    ret: List[MarkdownText] = []
    next_level = None
    for l in lines:
        level_match = re_level.findall(l)
        if level_match:
            level_match = list(itertools.chain.from_iterable(level_match)) # flatten
            level = level_match[0].count(level_word) # レベルを数える
            ret.append(MarkdownText(level, level_match[1]))
        else:
            # レベル部が無い場合
            if next_level:
                level = next_level
                next_level = None
            else:
                level = 0
            
            ret.append(MarkdownText(level, l))
        
        if l.endswith(return_ends):
            next_level = level

    return ret

if __name__=='__main__':

    indent = '\t'

    clipbord_text = cl.paste()
    # 行ごとにsplit
    clipbord_text = clipbord_text.splitlines(keepends=True)
    
    mdt_list = to_indent_mdt_list(clipbord_text)

    results = ''
    for l in mdt_list:
        results += mdt_to_indent_text(l, indent)

    cl.copy(results)



