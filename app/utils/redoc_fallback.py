from fastapi.responses import HTMLResponse


def render_redoc_fallback() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>API ReDoc (Offline Fallback)</title>
  <style>
    body { font-family: Inter, Arial, sans-serif; margin: 0; background: #0f1220; color: #eef2ff; }
    .wrap { max-width: 1100px; margin: 0 auto; padding: 20px; }
    .hint { background: #1b2140; border: 1px solid #36407a; border-radius: 10px; padding: 12px; margin-bottom: 16px; }
    .path { border: 1px solid #36407a; background: #171d37; border-radius: 10px; padding: 10px; margin: 10px 0; }
    .method { display: inline-block; min-width: 58px; text-align: center; padding: 2px 8px; border-radius: 6px; background: #2f3b77; margin-right: 8px; }
    code { color: #9ed0ff; }
    a { color: #9ed0ff; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>API 文档（ReDoc 离线回退页）</h1>
    <div class="hint">
      当前页面用于解决某些服务器环境访问外部 CDN 失败导致 <code>/redoc</code> 空白的问题。<br/>
      你仍然可以使用 <a href="/docs">/docs</a> 或直接查看 <a href="/openapi.json">/openapi.json</a>。
    </div>
    <div id="paths"></div>
  </div>
  <script>
    fetch('/openapi.json').then(r=>r.json()).then(spec=>{
      const root = document.getElementById('paths');
      const paths = spec.paths || {};
      Object.keys(paths).sort().forEach(path => {
        const block = document.createElement('div');
        block.className = 'path';
        const methods = Object.keys(paths[path]).sort();
        const title = document.createElement('div');
        title.innerHTML = '<strong>' + path + '</strong>';
        block.appendChild(title);
        methods.forEach(m => {
          const row = document.createElement('div');
          const summary = (paths[path][m] && paths[path][m].summary) ? (' - ' + paths[path][m].summary) : '';
          row.innerHTML = '<span class="method">' + m.toUpperCase() + '</span>' + summary;
          block.appendChild(row);
        });
        root.appendChild(block);
      });
    }).catch(err => {
      document.getElementById('paths').innerHTML = '<p>加载 openapi.json 失败：' + err + '</p>';
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)
