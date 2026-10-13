#!/usr/bin/env python3
"""Static scan of skill folders for corrupted or harmful content.

Nothing here executes skill code: files are only read as bytes/text, parsed
(ast.parse / json.loads / yaml.safe_load) or syntax-checked. Run with -I.

usage: scan_skills.py OUT.json ROOT [ROOT ...]
Each ROOT is a directory whose immediate children are skill folders.
"""
import ast, json, os, re, sys, stat, subprocess, collections

OUT = sys.argv[1]
ROOTS = sys.argv[2:]

TEXT_EXT = {'.md', '.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.json', '.sh', '.bash', '.zsh', '.ps1',
            '.bat', '.cmd', '.txt', '.yml', '.yaml', '.toml', '.html', '.htm', '.css', '.scss', '.csv', '.xml',
            '.svg', '.ini', '.cfg', '.conf', '.rb', '.go', '.rs', '.java', '.kt', '.swift', '.php', '.pl', '.sql',
            '.lua', '.r', '.mdx', '.vue', '.svelte', '.ipynb', '.lock', '.env', '.example', '.tmpl', '.j2',
            '.jinja', '.rst', '.tex', '.gitignore', '.cs', '.cpp', '.c', '.h', '.hpp', '.dart', '.ex', '.exs',
            '.zig', '.nix', '.mk', '.make', '.gradle', '.properties', '.plist', '.jsonl', '.ndjson', '.map'}
SCRIPT_EXT = {'.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.sh', '.bash', '.zsh', '.ps1', '.bat', '.cmd', '.rb',
              '.pl', '.php', '.go', '.rs', '.lua'}
BIN_EXT = {'.exe', '.dll', '.so', '.dylib', '.jar', '.whl', '.pyc', '.pyo', '.class', '.apk', '.msi', '.scr',
           '.com', '.bin', '.o', '.a', '.deb', '.rpm', '.dmg', '.pkg', '.node', '.wasm', '.egg', '.zip', '.tar',
           '.gz', '.tgz', '.7z', '.rar', '.xz', '.bz2'}
MAGIC = [(b'\x7fELF', 'ELF'), (b'MZ', 'PE/DOS'), (b'\xfe\xed\xfa\xce', 'Mach-O'), (b'\xfe\xed\xfa\xcf', 'Mach-O'),
         (b'\xcf\xfa\xed\xfe', 'Mach-O'), (b'\xce\xfa\xed\xfe', 'Mach-O'), (b'\xca\xfe\xba\xbe', 'Java/Mach-O fat'),
         (b'PK\x03\x04', 'zip-like'), (b'\x1f\x8b', 'gzip'), (b'\x00asm', 'wasm'), (b'#!', 'shebang')]
ALLOWED_FM = {'name', 'description', 'license', 'compatibility', 'allowed-tools', 'metadata'}

F = []  # findings
def add(cat, sev, skill, rel, line, snip):
    F.append({'cat': cat, 'sev': sev, 'skill': skill, 'file': rel, 'line': line, 'snip': snip[:200].strip()})

def rx(p, fl=re.I):
    return re.compile(p, fl)

# (category, severity, regex, applies_to: 'all' | 'script' | 'md')
RULES = [
    # remote execution / download-and-run
    ('remote-exec', 'HIGH', rx(r'(curl|wget)\b[^\n|]{0,300}\|\s*(sudo\s+)?(ba|z|da|k)?sh\b'), 'all'),
    ('remote-exec', 'HIGH', rx(r'\b(irm|iwr|Invoke-WebRequest|Invoke-RestMethod)\b[^\n|]{0,300}\|\s*(iex|Invoke-Expression)\b'), 'all'),
    ('remote-exec', 'HIGH', rx(r'(bash|sh|zsh)\s+<\(\s*(curl|wget)'), 'all'),
    ('remote-exec', 'HIGH', rx(r'(eval|source)\s+["\']?\$\(\s*(curl|wget)'), 'all'),
    ('remote-exec', 'HIGH', rx(r'\b(exec|eval)\s*\(\s*(requests\.get|urllib|urlopen|fetch|atob|base64|codecs\.decode|zlib\.decompress|bytes\.fromhex)'), 'script'),
    ('remote-exec', 'MED', rx(r'\bInvoke-Expression\b|\biex\s*\('), 'all'),
    # obfuscation
    ('obfuscation', 'HIGH', rx(r'base64\s+(-d|--decode)\b[^\n]{0,80}\|\s*(ba|z)?sh'), 'all'),
    ('obfuscation', 'MED', rx(r'\b(b64decode|atob|base64\.b64decode|Buffer\.from\([^)]*[\'"]base64[\'"])'), 'script'),
    ('obfuscation', 'MED', rx(r'marshal\.loads|pickle\.loads?\(|exec\(compile\(|__import__\(["\']base64|codecs\.decode\([^)]*rot'), 'script'),
    ('obfuscation', 'MED', rx(r'(\\x[0-9a-f]{2}){12,}'), 'script'),
    ('obfuscation', 'MED', rx(r'String\.fromCharCode\([^)]{40,}\)'), 'script'),
    # credential access
    ('cred-access', 'MED', rx(r'~/\.ssh|\.ssh/id_|id_rsa|id_ed25519|\.aws/credentials|\.netrc|\.git-credentials|\.docker/config\.json|/etc/shadow|\.npmrc|\.pypirc|\.kube/config|gcloud/credentials|\.config/gh/hosts'), 'script'),
    ('cred-access', 'MED', rx(r'security\s+find-generic-password|Login Data|Cookies\.sqlite|chrome.*(cookies|login data)|keychain|credential\s*manager|CredRead'), 'script'),
    ('cred-access', 'MED', rx(r'\b(printenv|os\.environ\b[^\n]{0,20}(items|copy|dict)|env\s*\|\s*(curl|nc|base64)|process\.env\)\s*[,;]?\s*$)'), 'script'),
    # outbound sends / exfil channels
    ('exfil-channel', 'HIGH', rx(r'discord(app)?\.com/api/webhooks|hooks\.slack\.com/services|api\.telegram\.org/bot|pastebin\.com|transfer\.sh|webhook\.site|requestbin|ngrok\.(io|app)|burpcollaborator|oast\.(fun|live|pro|site)|interact\.sh|pipedream\.net|beeceptor|canarytokens|0x0\.st|file\.io|anonfiles'), 'all'),
    ('exfil-channel', 'MED', rx(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?![\d.])'), 'all'),
    ('exfil-channel', 'MED', rx(r'https?://(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|rb\.gy|shorturl\.at)/'), 'all'),
    ('net-send', 'INFO', rx(r'curl\b[^\n]{0,200}(\s-d\s|--data|\s-F\s|-X\s*POST|--upload-file|-T\s)'), 'script'),
    ('net-send', 'INFO', rx(r'requests\.(post|put)\(|axios\.(post|put)\(|method\s*:\s*[\'"](POST|PUT)[\'"]|urlopen\([^)]*data\s*='), 'script'),
    # destructive
    ('destructive', 'HIGH', rx(r'rm\s+-[a-z]*r[a-z]*f?[a-z]*\s+(--no-preserve-root\s+)?(/|~|\$HOME|"\$HOME"|\$\{HOME\}|/\*|~/\*)(\s|$|"|\')'), 'all'),
    ('destructive', 'HIGH', rx(r'\bmkfs(\.\w+)?\s|\bdd\s+if=[^\n]*of=/dev/|:\(\)\s*\{\s*:\|:&\s*\}|>\s*/dev/sd[a-z]|chmod\s+-R\s+0?777\s+/(\s|$)|format\s+c:|del\s+/[sq]\s+/[sq]\s+[a-z]:\\'), 'all'),
    ('destructive', 'MED', rx(r'git\s+push\s+(-f\b|--force(?!-with-lease))|git\s+reset\s+--hard|git\s+clean\s+-[a-z]*f|DROP\s+(TABLE|DATABASE)|TRUNCATE\s+TABLE|Remove-Item\s+[^\n]*-Recurse[^\n]*-Force|shutil\.rmtree\(\s*[\'"]/|os\.system\(\s*[\'"]rm\s'), 'script'),
    # persistence / privilege
    ('persistence', 'MED', rx(r'crontab\s+-|/etc/cron|systemctl\s+(enable|--user\s+enable)|launchctl\s+(load|bootstrap)|schtasks\s+/create|authorized_keys|/etc/sudoers|NOPASSWD|chmod\s+[ug]?\+s\b|LD_PRELOAD|CurrentVersion\\Run|>>\s*~?/?\$?HOME?/?\.?(bashrc|zshrc|profile|bash_profile)|>>\s*~/\.(bashrc|zshrc|profile)'), 'script'),
    ('persistence', 'INFO', rx(r'\bsudo\s'), 'script'),
    # prompt injection / hiding behaviour from the user
    ('prompt-injection', 'HIGH', rx(r'ignore\s+(all\s+|any\s+)?(the\s+)?(previous|prior|above|earlier|preceding)\s+(instructions|prompts?|rules|messages)|disregard\s+(all\s+|any\s+)?(the\s+)?(previous|prior|above|system|earlier)\s+(instructions|prompts?|rules)|forget\s+(all\s+)?(your|the)\s+(previous|prior)\s+instructions'), 'md'),
    ('prompt-injection', 'HIGH', rx(r"(do\s+not|don't|never)\s+(tell|inform|mention|reveal|show|let)\s+(the\s+)?user|without\s+(telling|informing|notifying|alerting)\s+(the\s+)?user|(hide|conceal)\s+(this|it)\s+from\s+the\s+user|secretly\s+(send|upload|post|exfiltrate|run|execute|install|add)|silently\s+(send|upload|post|exfiltrate|install)"), 'md'),
    ('prompt-injection', 'HIGH', rx(r'you\s+are\s+now\s+(DAN|in\s+developer\s+mode|unrestricted|jailbroken)|developer\s+mode\s+enabled|override\s+(your|the)\s+(system|safety)\s+(prompt|instructions|rules)|(reveal|print|output|repeat|leak)\s+(your|the)\s+(system\s+prompt|hidden\s+instructions)'), 'md'),
    ('prompt-injection', 'MED', rx(r'exfiltrat'), 'md'),
    # secrets
    ('secret', 'HIGH', rx(r'ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,}|gh[ousr]_[A-Za-z0-9]{36}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|\bsk-[A-Za-z0-9]{40,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,}|hf_[A-Za-z0-9]{34,}|-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}', 0), 'all'),
    # lifecycle scripts
    ('lifecycle-script', 'MED', rx(r'"(pre|post)?install"\s*:|"prepare"\s*:\s*"|cmdclass\s*=|setup\(\s*[^)]*cmdclass'), 'all'),
]

# hook / auto-run wiring: file names and frontmatter
HOOK_FILES = {'hooks.json', 'settings.json', 'settings.local.json', '.mcp.json', 'mcp.json', 'plugin.json',
              'marketplace.json', 'package.json', 'pyproject.toml', 'setup.py', 'Makefile', 'Dockerfile',
              'docker-compose.yml', '.pre-commit-config.yaml', 'lefthook.yml', '.husky'}
HOOK_TEXT = rx(r'\b(PreToolUse|PostToolUse|SessionStart|SessionEnd|UserPromptSubmit|PreCompact|SubagentStop)\b|"hooks"\s*:')

ZW = {0x200B: 'ZWSP', 0x200C: 'ZWNJ', 0x200D: 'ZWJ', 0x2060: 'WORD-JOINER', 0xFEFF: 'BOM/ZWNBSP', 0x180E: 'MVS',
      0x00AD: 'SOFT-HYPHEN'}
BIDI = {0x200E: 'LRM', 0x200F: 'RLM', 0x202A: 'LRE', 0x202B: 'RLE', 0x202C: 'PDF', 0x202D: 'LRO', 0x202E: 'RLO',
        0x2066: 'LRI', 0x2067: 'RLI', 0x2068: 'FSI', 0x2069: 'PDI'}

def is_tag(cp):   # unicode tag characters (invisible ASCII smuggling)
    return 0xE0000 <= cp <= 0xE007F
def is_vs_sup(cp):  # variation selectors supplement
    return 0xE0100 <= cp <= 0xE01EF

DOMAIN = re.compile(r'https?://([A-Za-z0-9.-]+\.[A-Za-z]{2,})(?::\d+)?', re.I)

stats = collections.Counter()
domains = collections.defaultdict(lambda: collections.defaultdict(set))  # domain -> skill -> files (scripts only)
fm_info = {}
per_skill_files = collections.Counter()
allowed_tools = collections.defaultdict(list)

def parse_frontmatter(text):
    if not text.startswith('---'):
        return None, 'no frontmatter'
    m = re.match(r'^---\r?\n(.*?)\r?\n---\s*(\r?\n|$)', text, re.S)
    if not m:
        return None, 'unterminated frontmatter'
    try:
        import yaml
        d = yaml.safe_load(m.group(1))
    except Exception as e:  # noqa
        return None, 'yaml error: %s' % str(e).splitlines()[0][:100]
    if not isinstance(d, dict):
        return None, 'frontmatter not a mapping'
    return d, None

def scan_text(skill, rel, text, ext, is_script, is_md):
    lines = text.split('\n')
    # conflict markers
    for i, ln in enumerate(lines, 1):
        if ln.startswith('<<<<<<< ') or ln.startswith('>>>>>>> ') or ln == '=======' and i > 1 and ext in ('.py', '.js', '.json', '.ts'):
            add('corruption', 'MED', skill, rel, i, 'merge-conflict marker: ' + ln[:60])
    # unicode checks (whole text)
    seen = collections.Counter()
    first = {}
    for i, ln in enumerate(lines, 1):
        for ch in ln:
            cp = ord(ch)
            if cp < 0x80:
                continue
            kind = None
            if cp in ZW and not (cp == 0xFEFF and i == 1 and ln.startswith(ch)):
                kind = 'zero-width:' + ZW[cp]
            elif cp in BIDI:
                kind = 'bidi:' + BIDI[cp]
            elif is_tag(cp):
                kind = 'unicode-tag'
            elif is_vs_sup(cp):
                kind = 'variation-selector-supp'
            if kind:
                seen[kind] += 1
                first.setdefault(kind, i)
    for kind, n in seen.items():
        sev = 'HIGH' if kind.startswith(('bidi:RLO', 'bidi:LRO', 'bidi:RLE', 'bidi:LRE', 'bidi:RLI', 'bidi:LRI', 'bidi:FSI', 'unicode-tag', 'variation-selector-supp')) else 'MED'
        if kind in ('zero-width:SOFT-HYPHEN', 'bidi:LRM', 'bidi:RLM', 'zero-width:ZWJ', 'zero-width:ZWNJ') :
            sev = 'INFO'
        add('hidden-unicode', sev, skill, rel, first[kind], '%s x%d' % (kind, n))
    # HTML comments in markdown (hidden instructions)
    if is_md:
        for m in re.finditer(r'<!--(.*?)-->', text, re.S):
            body = m.group(1).strip()
            if len(body) >= 40:
                ln = text.count('\n', 0, m.start()) + 1
                add('html-comment', 'INFO', skill, rel, ln, body.replace('\n', ' '))
        for m in re.finditer(r'^\[//\]:\s*#\s*\((.{30,})\)\s*$', text, re.M):
            add('html-comment', 'INFO', skill, rel, text.count('\n', 0, m.start()) + 1, m.group(1))
    # rules
    for i, ln in enumerate(lines, 1):
        if len(ln) > 6000:
            seg = ln[:6000]
            # long minified lines: look for base64 blobs separately below
        else:
            seg = ln
        for cat, sev, pat, scope in RULES:
            if scope == 'script' and not is_script:
                continue
            if scope == 'md' and not (is_md or ext in ('.txt', '.yml', '.yaml', '.json', '.html')):
                continue
            m = pat.search(seg)
            if m:
                add(cat, sev, skill, rel, i, seg[max(0, m.start() - 40):m.end() + 60])
        if HOOK_TEXT.search(seg) and (is_script or ext in ('.json', '.yml', '.yaml', '.toml')):
            add('hook-wiring', 'MED', skill, rel, i, seg)
    # long base64-ish literals in scripts and SKILL.md
    if is_script or rel.endswith('SKILL.md'):
        for m in re.finditer(r'[A-Za-z0-9+/]{240,}={0,2}', text):
            pre = text[max(0, m.start() - 30):m.start()]
            if 'base64,' in pre and ext not in ('.py', '.sh', '.js', '.mjs', '.ps1'):
                continue
            add('obfuscation', 'MED', skill, rel, text.count('\n', 0, m.start()) + 1, 'long base64-like literal len=%d pre=%r' % (len(m.group(0)), pre))
    # domains in scripts
    if is_script:
        for m in DOMAIN.finditer(text):
            domains[m.group(1).lower().rstrip('.')][skill].add(rel)

def syntax_check(skill, rel, path, ext, text):
    try:
        if ext == '.py':
            compile(text, rel, 'exec', dont_inherit=True)
        elif ext == '.json':
            json.loads(text)
        elif ext in ('.yml', '.yaml'):
            import yaml
            list(yaml.safe_load_all(text))
        elif ext in ('.sh', '.bash'):
            r = subprocess.run(['bash', '-n', path], capture_output=True, text=True, timeout=20)
            if r.returncode != 0:
                add('corruption', 'INFO', skill, rel, 0, 'bash -n: ' + (r.stderr.strip().splitlines() or ['?'])[0])
        elif ext in ('.js', '.mjs', '.cjs'):
            r = subprocess.run(['node', '--check', path], capture_output=True, text=True, timeout=20)
            if r.returncode != 0:
                add('corruption', 'INFO', skill, rel, 0, 'node --check: ' + (r.stderr.strip().splitlines() or ['?'])[-1])
    except SyntaxError as e:
        add('corruption', 'INFO', skill, rel, getattr(e, 'lineno', 0) or 0, 'python syntax: %s' % e.msg)
    except (ValueError, Exception) as e:  # json/yaml/other parse failure
        add('corruption', 'INFO', skill, rel, 0, 'parse error: %s' % str(e).splitlines()[0][:100])

def scan_skill(root, skill):
    sdir = os.path.join(root, skill)
    sk_md = os.path.join(sdir, 'SKILL.md')
    if not os.path.isfile(sk_md):
        add('structure', 'MED', skill, 'SKILL.md', 0, 'missing SKILL.md')
    else:
        try:
            t = open(sk_md, encoding='utf-8').read()
            fm, err = parse_frontmatter(t)
            if err:
                add('structure', 'MED', skill, 'SKILL.md', 1, err)
            else:
                fm_info[skill] = fm
                nm, desc = fm.get('name'), fm.get('description')
                if not nm:
                    add('structure', 'MED', skill, 'SKILL.md', 1, 'frontmatter has no name')
                elif str(nm) != skill:
                    add('structure', 'INFO', skill, 'SKILL.md', 1, 'name %r != folder %r' % (nm, skill))
                if not desc or not str(desc).strip():
                    add('structure', 'MED', skill, 'SKILL.md', 1, 'frontmatter has no description')
                elif len(str(desc)) > 1024:
                    add('structure', 'INFO', skill, 'SKILL.md', 1, 'description %d chars (>1024)' % len(str(desc)))
                extra = set(fm) - ALLOWED_FM
                if extra:
                    add('structure', 'INFO', skill, 'SKILL.md', 1, 'non-standard frontmatter keys: %s' % ','.join(sorted(map(str, extra))))
                if 'hooks' in fm:
                    add('hook-wiring', 'HIGH', skill, 'SKILL.md', 1, 'frontmatter declares hooks: %s' % json.dumps(fm['hooks'])[:150])
                at = fm.get('allowed-tools')
                if at:
                    allowed_tools[skill] = at if isinstance(at, list) else str(at).split()
                    s = json.dumps(at)
                    if re.search(r'Bash(\(\*\))?"|Bash\(\*|"\*"|\bBash\b(?!\()', s):
                        add('permission', 'MED', skill, 'SKILL.md', 1, 'allowed-tools grants broad access: ' + s[:150])
        except UnicodeDecodeError:
            add('corruption', 'HIGH', skill, 'SKILL.md', 0, 'SKILL.md is not valid UTF-8')
    for dp, dn, fn in os.walk(sdir, followlinks=False):
        # unwanted directories
        for d in list(dn):
            rel_d = os.path.relpath(os.path.join(dp, d), sdir)
            if d in ('.git', '.svn', '.hg'):
                add('hidden-file', 'MED', skill, rel_d, 0, 'VCS directory shipped inside skill')
            if d in ('hooks', '.husky', '.claude-plugin', '.github') or (d == '.claude' and True):
                add('hook-wiring', 'INFO', skill, rel_d, 0, 'directory named %s' % d)
            p = os.path.join(dp, d)
            if os.path.islink(p):
                tgt = os.readlink(p)
                add('symlink', 'MED', skill, rel_d, 0, 'directory symlink -> ' + tgt)
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, sdir)
            per_skill_files[skill] += 1
            stats['files'] += 1
            if os.path.islink(p):
                tgt = os.readlink(p)
                real = os.path.realpath(p)
                ok = os.path.exists(p)
                inside = real.startswith(os.path.realpath(sdir) + os.sep)
                add('symlink', 'HIGH' if (not inside) else 'INFO', skill, rel, 0, 'symlink -> %s (exists=%s inside_skill=%s)' % (tgt, ok, inside))
                continue
            st = os.lstat(p)
            ext = os.path.splitext(f)[1].lower()
            base = f
            if st.st_size == 0:
                if f not in ('__init__.py', '.gitkeep', '.keep', 'py.typed'):
                    add('corruption', 'INFO', skill, rel, 0, 'zero-byte file')
                continue
            if st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                stats['executable-bit'] += 1
                if ext not in SCRIPT_EXT:
                    add('exec-bit', 'INFO', skill, rel, 0, 'executable bit on non-script file')
            if base.startswith('.') and base not in ('.gitignore', '.gitkeep', '.keep', '.gitattributes', '.editorconfig', '.prettierrc', '.eslintrc', '.npmignore', '.dockerignore'):
                add('hidden-file', 'INFO', skill, rel, 0, 'dotfile')
            if base in HOOK_FILES or base.lower() in ('hooks.json',):
                add('hook-wiring', 'MED' if base in ('hooks.json', 'settings.json', 'settings.local.json', '.mcp.json', 'mcp.json', 'plugin.json') else 'INFO', skill, rel, 0, 'config file %s' % base)
            with open(p, 'rb') as fh:
                head = fh.read(8)
            magic = next((n for m, n in MAGIC if head.startswith(m)), None)
            if ext in BIN_EXT or (magic and magic not in ('shebang',) and ext not in ('.zip',) and ext not in TEXT_EXT):
                if magic in ('ELF', 'PE/DOS', 'Mach-O', 'Java/Mach-O fat', 'wasm') or ext in BIN_EXT:
                    add('binary', 'HIGH' if magic in ('ELF', 'PE/DOS', 'Mach-O', 'wasm') or ext in ('.exe', '.dll', '.so', '.dylib', '.jar', '.msi', '.scr', '.node', '.wasm', '.bin', '.whl', '.pyc') else 'MED', skill, rel, 0, 'binary/archive: ext=%s magic=%s size=%d' % (ext, magic, st.st_size))
                    stats['binary'] += 1
                    continue
            if ext not in TEXT_EXT and f not in ('Makefile', 'Dockerfile', 'LICENSE', 'NOTICE', 'README', 'CHANGELOG', 'VERSION', 'Gemfile', 'Procfile', 'requirements.txt') and not ext == '':
                stats['asset:' + ext] += 1
                continue
            if st.st_size > 6_000_000:
                add('structure', 'INFO', skill, rel, 0, 'large text file %d bytes (not regex-scanned)' % st.st_size)
                continue
            raw = open(p, 'rb').read()
            if b'\x00' in raw:
                add('corruption', 'MED', skill, rel, 0, 'NUL byte inside supposed text file (ext=%s)' % ext)
                continue
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError as e:
                add('corruption', 'MED', skill, rel, 0, 'not valid UTF-8: %s' % e)
                continue
            stats['text-files'] += 1
            is_script = ext in SCRIPT_EXT or (head.startswith(b'#!'))
            is_md = ext in ('.md', '.mdx', '.rst', '.txt')
            scan_text(skill, rel, text, ext, is_script, is_md)
            syntax_check(skill, rel, p, ext, text)

for root in ROOTS:
    for skill in sorted(os.listdir(root)):
        if os.path.isdir(os.path.join(root, skill)) and not os.path.islink(os.path.join(root, skill)):
            stats['skills'] += 1
            scan_skill(root, skill)
        elif os.path.islink(os.path.join(root, skill)):
            add('symlink', 'HIGH', skill, '.', 0, 'skill folder is a symlink -> ' + os.readlink(os.path.join(root, skill)))

res = {
    'roots': ROOTS, 'stats': dict(stats), 'findings': F,
    'domains': {d: {s: sorted(fs) for s, fs in v.items()} for d, v in domains.items()},
    'allowed_tools': allowed_tools,
    'frontmatter_keys': {s: sorted(map(str, d)) for s, d in fm_info.items()},
}
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False, default=list)
print('skills', stats['skills'], 'files', stats['files'], 'text', stats['text-files'], 'binary', stats['binary'], 'findings', len(F))
c = collections.Counter((f['cat'], f['sev']) for f in F)
for (cat, sev), n in sorted(c.items(), key=lambda x: (['HIGH', 'MED', 'INFO'].index(x[0][1]), x[0][0])):
    print('%-5s %-18s %d' % (sev, cat, n))
