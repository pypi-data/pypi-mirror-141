import json
from typing import List, Dict, Tuple, Union
import random
import re
import uuid
from pathlib import Path
from datetime import datetime
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import htmlmin
from logboss.config import LogTagBase

ACTION_JS = """

"""

PYTHON_CSS = """
/* Styles for Python code */
.highlight .hll { background-color: rgba(42, 213, 213, 0.2) }
.highlight .c { color: #408080; font-style: italic } /* Comment */
.highlight .err { border: 1px solid #FF0000 } /* Error */
.highlight .k { color: #008000; font-weight: bold } /* Keyword */
.highlight .o { color: #666666 } /* Operator */
.highlight .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #BC7A00 } /* Comment.Preproc */
.highlight .c1 { color: #408080; font-style: italic } /* Comment.Single */
.highlight .cs { color: #408080; font-style: italic } /* Comment.Special */
.highlight .gd { color: #A00000 } /* Generic.Deleted */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gr { color: #FF0000 } /* Generic.Error */
.highlight .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.highlight .gi { color: #00A000 } /* Generic.Inserted */
.highlight .go { color: #808080 } /* Generic.Output */
.highlight .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.highlight .gt { color: #0040D0 } /* Generic.Traceback */
.highlight .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: #008000 } /* Keyword.Pseudo */
.highlight .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: #B00040 } /* Keyword.Type */
.highlight .m { color: #666666 } /* Literal.Number */
.highlight .s { color: #BA2121 } /* Literal.String */
.highlight .na { color: #7D9029 } /* Name.Attribute */
.highlight .nb { color: #008000 } /* Name.Builtin */
.highlight .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.highlight .no { color: #880000 } /* Name.Constant */
.highlight .nd { color: #AA22FF } /* Name.Decorator */
.highlight .ni { color: #999999; font-weight: bold } /* Name.Entity */
.highlight .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.highlight .nf { color: #0000FF } /* Name.Function */
.highlight .nl { color: #A0A000 } /* Name.Label */
.highlight .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.highlight .nt { color: #008000; font-weight: bold } /* Name.Tag */
.highlight .nv { color: #19177C } /* Name.Variable */
.highlight .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.highlight .w { color: #bbbbbb } /* Text.Whitespace */
.highlight .mf { color: #666666 } /* Literal.Number.Float */
.highlight .mh { color: #666666 } /* Literal.Number.Hex */
.highlight .mi { color: #666666 } /* Literal.Number.Integer */
.highlight .mo { color: #666666 } /* Literal.Number.Oct */
.highlight .sb { color: #BA2121 } /* Literal.String.Backtick */
.highlight .sc { color: #BA2121 } /* Literal.String.Char */
.highlight .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.highlight .s2 { color: #BA2121 } /* Literal.String.Double */
.highlight .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.highlight .sh { color: #BA2121 } /* Literal.String.Heredoc */
.highlight .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.highlight .sx { color: #008000 } /* Literal.String.Other */
.highlight .sr { color: #BB6688 } /* Literal.String.Regex */
.highlight .s1 { color: #BA2121 } /* Literal.String.Single */
.highlight .ss { color: #19177C } /* Literal.String.Symbol */
.highlight .bp { color: #008000 } /* Name.Builtin.Pseudo */
.highlight .vc { color: #19177C } /* Name.Variable.Class */
.highlight .vg { color: #19177C } /* Name.Variable.Global */
.highlight .vi { color: #19177C } /* Name.Variable.Instance */
.highlight .il { color: #666666 } /* Literal.Number.Integer.Long */
.highlight .filename { color: #444; font-style: italic } /* Filename */
"""

STYLES_CSS = """

"""


class Html2LogGenerator:
    """
    Generates an HTML log file from the given logs. The logs must derive from the logger in the
    format returned by ``Logger.get_logs()``.
    """

    class _keys:
        file_path = 'file_path'
        function_name = 'function_name'
        line_num = 'line_num'
        msg = 'msg'
        tag_id = 'tag_id'
        depth = 'depth'
        thread_id = 'thread_id'
        thread_name = 'thread_name'
        is_main_thread = 'is_main_thread'
        timestamp = 'timestamp'

    def __init__(self, logs: Dict):
        self._orig_tags = logs['log_tags']
        self._log_tags = self._get_log_tags(logs['log_tags'])
        self._log_entries = logs['log_entries']
        self._main_thread_id = logs['main_thread_id']

    def generate(self, log_file: Union[str, Path], title: str = 'Log Results', include_code: bool = False,
                 datetime_range: Tuple[datetime, datetime] = None, exclude_files: List[str] = None):
        log_entries = []
        for le in self._log_entries.values():
            log_entries += le
        log_entries = sorted(log_entries, key=lambda x: x['timestamp'])
        log_file = Path(log_file)
        html = htmlmin.minify(f"""
                <html>
                    <head>
                        <title>{title}</title>
                        <script type="text/javascript">
                            {ACTION_JS}
                        </script>
                        <style>
                            {STYLES_CSS}
                        </style>
                    </head>
                    <body>
                        <!-- Title -->
                        <div id="title">
                            <h1>{title}</h1>
                        </div>
                    </body>
                    {'<br/>' * 12}
                </html>
                """, remove_comments=True, remove_empty_space=True)

        # region Send Files To Log Directory
        resources = log_file.parent
        resources.mkdir(parents=True, exist_ok=True)
        # if code_blocks:
        #     for values in code_blocks.values():
        #         with open(f"{resources}/{values['path']}", 'w') as f:
        #             f.write(values['code'])

        html_file = Path(f'{resources.absolute()}/{log_file.stem}.html')
        json_file = Path(f'{resources.absolute()}/{log_file.stem}.json')
        with html_file.open('w') as f:
            f.write(html)
        with json_file.open('w') as j:
            json.dump({
                'logs': self._log_entries,
                'tags': self._log_tags
            }, j)
        # endregion Send Files To Log Directory

    def generate1(self, log_file: Union[str, Path], title: str = 'Log Results', include_code: bool = False,
                 datetime_range: Tuple[datetime, datetime] = None, exclude_files: List[str] = None):
        """
        Generates an HTML log file from the logs persisted by the logger.

        If using a compiling tool such as PyInstaller, ``include_code`` must be ``False``. Also, there is more
        overhead when including the code snippets associated to the log events. Each log event is associated to a
        file; each file is imported in HTML format as an iframe to the overall output.

        Args:
            log_file: Absolute path to the SQLite DB log file.
            title: Title of the log file. Default is "Log File".
            include_code: If ``True`` the include iframes of the source code of the files associated to the log
                          entries.
            datetime_range: Defines the start and/or end date parameters of the log data included in the
                            output file. This is always a ``Tuple`` of size 2 where the first item is the
                            start date and the second is the end date. If only a start or end date is
                            desired, then set the other value to ``None``. Date should be ``datetime``
                            objects.
            exclude_files: A list of regular expressions for files that should NOT be included in the
                           code blocks. If ``include_code`` is ``True``, then the code files are included in
                           the output so the code can be referenced directly by the logs. This parameter
                           can be used to improve security and space. It is recommended to exclude files
                           that may leak sensitive information and are highly unlikely to provide much
                           use to the log file.
        """
        # region Get Content Of Log File
        if not isinstance(log_file, Path):
            log_file = Path(log_file)
        # endregion Get Content Of Log File

        # region Create HTML File
        if datetime_range:
            start, end = datetime_range  # type: datetime, datetime
            start_eval = (lambda x: x >= start.timestamp()) if start else (lambda x: True)
            end_eval = (lambda x: x <= end.timestamp()) if end else (lambda x: True)
            temp_log_entries = {
                k: sorted([
                    x for x in v
                    if start_eval(x[self._keys.timestamp]) and end_eval(x[self._keys.timestamp])],
                    key=lambda y: y['timestamp']
                )
                for k, v in self._log_entries
            }
        else:
            temp_log_entries = {
                k: sorted(v, key=lambda y: y['timestamp'])
                for k, v in self._log_entries.items()
            }
        log_entries = []
        if len(temp_log_entries.keys()) > 1 or self._main_thread_id in map(str, temp_log_entries.keys()):
            # Must be multi-threaded
            thread_starts = [(t, le[0][self._keys.timestamp]) for t, le in temp_log_entries.items()
                             if not le[0][self._keys.is_main_thread]]
            thread_starts = sorted(thread_starts, key=lambda x: x[1])

            if self._main_thread_id in temp_log_entries.keys():
                thread_id, timestamp = thread_starts.pop() if thread_starts else None, None
                for entry in temp_log_entries.pop(self._main_thread_id):
                    while timestamp and entry[self._keys.timestamp] >= timestamp:
                        log_entries += temp_log_entries.pop(thread_id)
                        if thread_starts:
                            thread_id, timestamp = thread_starts.pop()
                        else:
                            thread_id = timestamp = None
                    log_entries.append(entry)
            if temp_log_entries and thread_starts:
                for thread_id, timestamp in thread_starts:
                    log_entries += temp_log_entries.pop(thread_id)
        else:
            # Must be only single threaded
            log_entries = temp_log_entries[list(temp_log_entries.keys())[0]]
        code_blocks = self._get_code_blocks(log_entries=log_entries,
                                            exclude_files=exclude_files) if include_code else None

        used_log_tags, log_entries_html = self._get_log_entries(log_entries=log_entries,
                                                                code_blocks=code_blocks if include_code else None)
        self._log_tags = {k: v for k, v in self._log_tags.items() if k in used_log_tags}
        code_blocks_html = ''.join([cb['block'] for cb in code_blocks.values()]) if code_blocks else ''
        legend_html = self._legend()
        additional_styles_css = self._get_styles(include_code=include_code)

        # Minify HTML file to reduce space.
        html = htmlmin.minify(f"""
        <html>
            <head>
                <title>{title}</title>
                <script type="text/javascript">
                    {ACTION_JS}
                </script>
                <style>
                    {STYLES_CSS}
                    {additional_styles_css}
                </style>
            </head>
            <body>
                <!-- Title -->
                <div id="title">
                    <h1>{title}</h1>
                </div>
                <!-- Legend -->
                <div id="legend">
                    {legend_html}
                </div>
                <!-- Code Blocks -->
                <div class="hide" id="code-blocks">
                    {code_blocks_html}
                </div>
                <!-- Log Entries -->
                <div id="log-entries">
                    {log_entries_html}
                </div>
            </body>
            {'<br/>' * 12}
        </html>
        """, remove_comments=True, remove_empty_space=True)
        # endregion Create HTML File

        # region Send Files To Log Directory
        resources = log_file.parent
        resources.mkdir(parents=True, exist_ok=True)
        if code_blocks:
            for values in code_blocks.values():
                with open(f"{resources}/{values['path']}", 'w') as f:
                    f.write(values['code'])

        html_file = Path(f'{resources.absolute()}/{log_file.stem}.html')
        with html_file.open('w') as f:
            f.write(html)
        # endregion Send Files To Log Directory

    @staticmethod
    def _get_log_tags(log_tags: List[Dict[str, Union[int, str]]]):
        tags = {}
        hue_interval = int(360 / len(log_tags))
        for e, tag in enumerate(log_tags):
            lt = LogTagBase(
                name=tag['name'],
                value=tag['value'],
                color=tag['color']
            )
            lt.__tag_id__ = tag['id']
            if not lt.color:
                random.seed(lt.name)
                hue = hue_interval * e
                sat = random.randint(20, 80)
                light = random.randint(4, 7) * 10
                lt.color = f'hsl({hue}, {sat}%, {light}%)'
            tags[lt.__tag_id__] = lt
        return tags

    def _get_styles(self, include_code: bool):
        """
        Sets the global dynamic style variables and classes. These styles cannot be controlled
        by a stylesheet because they are dynamically created based on the log tags.
        """
        colors = []
        classes = []
        for ll in self._log_tags.values():
            colors.append(f'--{ll.alias}: {ll.color};')  # Color of log tag.
            # Each log tag has its own style class for highlighting the bottom of the
            # log entry.
            classes.append(f"""
            .{ll.alias} {{
                border-left: var(--{ll.alias}) solid 5px;
                border-bottom: lightgrey solid 2px;
                transition: border-bottom 0.2s ease-in-out;
            }}

            .{ll.alias}:hover {{
                border-bottom: var(--{ll.alias}) solid 2px;

            }}
            """)
        colors = '\n\t'.join(colors)
        classes = '\n'.join(classes)
        # Send the style classes along with a variable that sets the number of log entry buttons
        # to show. The "Code" button can be omitted.
        return f"""
        :root {{
            {colors}
            --log-entry-btns: {3 if include_code else 2}
        }}

        {classes}
        """

    def _legend(self):
        """
        Sets the log tags and the search filters in the legend.
        """

        def add_filter(log_tag: LogTagBase):
            return f"""
            <div class="log-tag fancy-checkbox" 
                 aria-label="{log_tag.alias}" 
                 aria-valuetext="{log_tag.value}"
                 onclick="handleLogTagFilter(this)">
                <label class="switch">
                    <input id="{log_tag.alias}" type="checkbox" checked>
                    <span 
                        class="slider round" 
                        style="background-color: var(--{log_tag.alias}); box-shadow: 0 0 10px var(--{log_tag.alias});">
                    </span>
                </label>
                <span>{log_tag.name}</span>
                <button id="{log_tag.alias}" class="btn" onclick="expandByTag(this.id)">Show</button>
            </div>
            """

        filters = '\n'.join([
            add_filter(log_tag=log_tag)
            for log_tag in self._log_tags.values()
        ])
        return f"""
        <div id="filters-container">
            <div id="filters-controls">
                <button id="filters-btn" class="btn" onclick="handleShowFilter(this)">Hide Filters</button>
            </div>
            <div id="filters-wrapper">
                <div id="filters" class="decompressed">
                    <div id="log-tags" style="grid-template-columns: repeat({min(len(self._log_tags), 4)}, auto">
                        {filters}
                    </div>
                    <div class="divider"></div>
                    <div id="search-container">
                        <div id="search-params">
                            <div class="search-param fancy-checkbox">
                                <label class="switch">
                                    <input id="search-in-msg" type="checkbox" checked>
                                    <span class="slider round"></span>
                                </label>
                                <span>Include Message Blocks</span>
                            </div>
                            <div class="search-param fancy-checkbox">
                                <label class="switch">
                                    <input id="search-in-info" type="checkbox" checked>
                                    <span class="slider round"></span>
                                </label>
                                <span>Include Info Blocks</span>
                            </div>
                            <div></div>
                            <div class="search-param fancy-checkbox">
                                <label class="switch">
                                    <input id="search-whole-word" type="checkbox">
                                    <span class="slider round"></span>
                                </label>
                                <span>Whole Word Only</span>
                            </div>
                            <div class="search-param fancy-checkbox">
                                <label class="switch">
                                    <input id="search-regex" type="checkbox">
                                    <span class="slider round"></span>
                                </label>
                                <span>Use Regular Expression</span>
                            </div>
                            <div class="search-param fancy-checkbox">
                                <label class="switch">
                                    <input id="search-match-case" type="checkbox">
                                    <span class="slider round"></span>
                                </label>
                                <span>Match Case</span>
                            </div>
                        </div>
                        <div id="search-controls">
                            <input id="search" type="text" placeholder="Search for text..." onkeyup="searchOnEnter(event, this.id)">
                            <button id="go-btn" class="btn" onclick="search('search')">Go</button>
                        </div>
                        <div id="search-count"></div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _get_code_blocks(self, log_entries: List, exclude_files: List[str] = None):
        """
        Creates the code block panel, code block object tags, and the file name for each block.
        The object tag uses a function to send a line number to scroll to when the frame is opened.
        """
        exclude_files = exclude_files or []
        codes = {}  # type: Dict
        fc = 0
        if exclude_files:
            exclude_regexes = "(" + ")|(".join(exclude_files) + ")"
        else:
            exclude_regexes = None
        for le in log_entries:
            fp = le[self._keys.file_path]
            if fp not in codes.keys():
                if exclude_regexes and re.match(pattern=exclude_regexes, string=fp, flags=re.IGNORECASE):
                    continue
                with open(fp, 'r') as f:
                    code = f.read()
                code_html = highlight(
                    code=code,
                    lexer=PythonLexer(),
                    formatter=HtmlFormatter(linenos='inline')
                )
                fc += 1
                file_id = f"file-id-{fc}"
                # Minify to reduce space.
                code = htmlmin.minify(f"""
                <html>
                    <head>
                        <script>
                            window.addEventListener("message", function(event) {{
                                line_num = Number(event.data);
                                view_line = line_num > 2 ? line_num - 3 : 0;
                                linenos = document.querySelectorAll('.lineno');
                                if(linenos.length > 0) {{
                                    linenos.forEach(line => {{line.style.backgroundColor = 'transparent';}})
                                    linenos[line_num - 1].style.backgroundColor = 'lightgreen';
                                    body = document.querySelector('body');
                                    body.scrollTo({{top: linenos[view_line].offsetTop, behavior: 'smooth'}});
                                }}
                            }})
                        </script>
                        <style>
                            {PYTHON_CSS}
                        </style>
                    </head>
                    <body>
                        {code_html}
                    </body>
                </html>
                """, remove_empty_space=True)
                # A UUID is used on the filename to create a consistent but unique filename for the HTML file
                # for the code. This prevents clashing of filenames.
                path = f'{uuid.uuid3(uuid.NAMESPACE_OID, fp).hex}.html'
                codes[fp] = {
                    'id'   : file_id,
                    'path' : path,
                    'block': f'''
                        <div class="code-block hide" id="{file_id}" aria-label="{Path(fp).stem}.html">
                            <div class="code-block-controls">
                                <span class="filepath" title="{le[self._keys.file_path]}">{le[self._keys.file_path]}</span>
                                <button class="close-code" onclick="hideCode('{file_id}')">X</button>
                            </div>
                            <div>
                                <object class="code" data="./{path}" type="text/html"></object>
                            </div>
                        </div>
                    ''',
                    'code' : code
                }
        return codes

    def _get_log_entries(self, log_entries: List, code_blocks: Dict[str, Dict[str, str]]):
        """
        Creates the reset button, log entries, and log blocks.
        """

        def format_info_block(le: dict):
            timestamp = datetime.fromtimestamp(le[self._keys.timestamp]).strftime('%a %b %-d %-I:%M:%S %p')
            return f'File: {le[self._keys.file_path]}\n' \
                   f'Line Number: {le[self._keys.line_num]}\n' \
                   f'Qualified Name: {le[self._keys.function_name]}\n' \
                   f'Thread Id: {le[self._keys.thread_id]}\n' \
                   f'Thread Name: {le[self._keys.thread_name]}\n' \
                   f'Timestamp: {timestamp}\n' \
                   f'Log Tag: {self._log_tags[le[self._keys.tag_id]].name}'

        logs = [
            f"""
            <div id="log-entries-controls">
                <div class="btn">
                    <button id="reset-btn" onclick="resetLogBlocks()">Reset</button>
                </div>
            </div>
            """
        ]
        used_log_tags = set()

        for e, log_entry in enumerate(log_entries):
            log_tag = self._log_tags[log_entry[self._keys.tag_id]]
            used_log_tags.add(log_entry[self._keys.tag_id])
            log_entry_id = f'log-entry-{e}'
            msg_block_id = f'msg-block-{e}'
            info_block_id = f'info-block-{e}'

            display = "hide" if log_entry[self._keys.depth] > 0 else "show"
            # Only show exp btn if there are child entries to this entry.
            if e < (len(log_entries) - 1) and \
                    log_entries[e + 1][self._keys.depth] > log_entry[self._keys.depth]:
                expand_btn = f"""
                <div class="btn item-container">
                    <button class="exp-btn hide-logs" onclick="toggleExpLogs('{log_entry_id}')"></button>
                </div>
                """
            else:
                expand_btn = f"""
                <div class="item-container">
                    <div class="no-exp">-</div>
                </div>
                """
            # Only show the code block button if enabled.
            if code_blocks:
                code_block = code_blocks.get(log_entry[self._keys.file_path])
                fid, fp = code_block.get('id'), code_block.get('path')
                code_btn = f'''
                    <div class="code-btn btn item-container">
                        <button onclick="showCode('{fid}', '{fp}', {log_entry[self._keys.line_num]})">Code</button>
                    </div>
                '''
            else:
                code_btn = ''
            func_def = f'{log_entry[self._keys.function_name]}:{log_entry[self._keys.line_num]}'
            logs.append(f"""
            <div id='{log_entry_id}' 
                 class="log-entry {display}"
                 aria-valuetext="{log_tag.alias}" 
                 aria-label="{log_entry[self._keys.depth]}">
                <div class="log-row {log_tag.alias}" style="margin-left: {log_entry[self._keys.depth] * 25}px;">
                    {expand_btn}
                    <div class="func item-container">
                        <span title="{func_def}">{func_def}</span>
                    </div>
                    <div class="preview item-container">
                        <span>{log_entry[self._keys.msg]}</span>
                    </div>
                    <div class="msg-btn btn item-container">
                        <button onclick="handleLogContent(this, '{msg_block_id}')">Message</button>
                    </div>
                    <div class="info-btn btn item-container">
                        <button onclick="handleLogContent(this, '{info_block_id}')">Info</button>
                    </div>
                    {code_btn}
                </div>
                <div 
                    class="log-block-container" 
                    style="border-left: var(--{log_tag.alias}) solid 5px; margin-left: {log_entry[self._keys.depth] * 25}px;"
                >
                    <div id="info-block-{e}" class="info-block log-block hide">
                        <pre>{format_info_block(log_entry)}</pre>
                    </div>
                    <div id="msg-block-{e}" class="msg-block log-block hide">
                        <pre>{log_entry[self._keys.msg]}</pre>
                    </div>
                </div>
            </div>
            """)
            e += 1
        return used_log_tags, ''.join(logs)
