from fastapi.responses import HTMLResponse


def render_homepage(app_name: str, version: str) -> HTMLResponse:
    html = f"""
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{app_name}</title>
  <style>
    :root {{
      --bg: #0d0b14;
      --bg-soft: #171225;
      --panel: #1d1630cc;
      --line: #3c2f65;
      --text: #f8efff;
      --muted: #bda8d6;
      --accent: #ff6ac1;
      --accent-2: #8a7dff;
      --ok: #9effd0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Inter", "Segoe UI", "PingFang SC", sans-serif;
      color: var(--text);
      background: radial-gradient(circle at 12% 10%, #3f1a57 0%, transparent 30%),
                  radial-gradient(circle at 85% 20%, #1c2d68 0%, transparent 30%),
                  linear-gradient(160deg, var(--bg) 0%, #130f1f 100%);
      min-height: 100vh;
    }}
    .wrap {{ max-width: 1200px; margin: 0 auto; padding: 30px 20px 50px; }}
    .hero {{
      border: 1px solid var(--line);
      background: linear-gradient(145deg, #1f1633e8, #120d22e8);
      border-radius: 22px;
      padding: 28px;
      box-shadow: 0 20px 60px #00000080;
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: -120px auto auto -80px;
      width: 280px;
      height: 280px;
      border-radius: 50%;
      background: radial-gradient(circle, #ff6ac133 0%, transparent 70%);
      pointer-events: none;
    }}
    .badge {{
      display: inline-flex;
      padding: 6px 12px;
      border: 1px solid #6c4b8f;
      border-radius: 99px;
      color: var(--ok);
      background: #241a3890;
      font-size: 13px;
    }}
    h1 {{ margin: 14px 0 10px; font-size: clamp(28px, 4vw, 44px); }}
    .subtitle {{ color: var(--muted); line-height: 1.8; max-width: 860px; }}
    .row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 24px; }}
    .card {{ border: 1px solid var(--line); background: var(--panel); border-radius: 16px; padding: 16px 18px; }}
    .card h3 {{ margin: 0 0 10px; color: #ffd2f0; font-size: 18px; }}
    .card ul {{ margin: 0; padding-left: 18px; }}
    .card li {{ margin: 7px 0; color: #dfcaef; }}
    .pill {{
      display: inline-block;
      margin: 4px 6px 0 0;
      font-size: 12px;
      padding: 4px 9px;
      border-radius: 999px;
      background: #2a1f42;
      border: 1px solid #5e4b8f;
      color: #d3c3ff;
    }}
    a {{ color: #ffd0ef; text-decoration: none; border-bottom: 1px dashed #a087d3; }}
    .api-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-top: 18px; }}
    .endpoint {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      border: 1px solid #4f3c7a;
      border-radius: 12px;
      padding: 10px 12px;
      margin: 8px 0;
      background: #1a143090;
      font-size: 14px;
    }}
    .method {{
      min-width: 48px;
      text-align: center;
      font-weight: 700;
      border-radius: 8px;
      padding: 4px 7px;
      border: 1px solid #8d6aca;
      background: #2f2052;
      color: #ffe3f4;
    }}
    footer {{ margin-top: 26px; color: #b5a3d3; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <span class="badge">API Testing Playground · v{version}</span>
      <h1>{app_name}</h1>
      <p class="subtitle">
        一个用于练习接口测试的靶场服务：覆盖认证鉴权、CRUD、分页/过滤/排序、状态码断言、文件上传、
        超时重试、幂等、管理员权限与订单状态流转。可直接用于 Postman / Apifox / curl / pytest + requests。
      </p>
      <div>
        <span class="pill">JWT 鉴权</span><span class="pill">统一响应</span><span class="pill">SQLite 持久化</span>
        <span class="pill">上传校验</span><span class="pill">幂等键</span><span class="pill">Flaky/Unstable</span>
      </div>
      <div class="row">
        <div class="card">
          <h3>快速入口</h3>
          <ul>
            <li><a href="/docs">Swagger 文档 /docs</a></li>
            <li><a href="/redoc">ReDoc 文档 /redoc</a></li>
            <li><a href="/health">健康检查 /health</a></li>
          </ul>
        </div>
        <div class="card">
          <h3>默认账号</h3>
          <ul>
            <li>admin / Admin123456（管理员）</li>
            <li>tester / Test123456（普通用户）</li>
            <li>先登录获取 Token 后再测鉴权接口</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="api-grid">
      <article class="card"><h3>A. 基础</h3>
        <div class="endpoint"><span class="method">GET</span><span>/</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/health</span></div>
      </article>
      <article class="card"><h3>B. 认证</h3>
        <div class="endpoint"><span class="method">POST</span><span>/auth/register</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/auth/login</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/auth/profile</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/auth/logout</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/auth/forbidden-demo</span></div>
      </article>
      <article class="card"><h3>C. 用户</h3>
        <div class="endpoint"><span class="method">GET</span><span>/users</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/users</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/users/{{id}}</span></div>
        <div class="endpoint"><span class="method">PUT</span><span>/users/{{id}}</span></div>
        <div class="endpoint"><span class="method">PATCH</span><span>/users/{{id}}</span></div>
        <div class="endpoint"><span class="method">DELETE</span><span>/users/{{id}}</span></div>
      </article>
      <article class="card"><h3>D/E. 商品 + 订单</h3>
        <div class="endpoint"><span class="method">GET</span><span>/items</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/items</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/items/{{id}}</span></div>
        <div class="endpoint"><span class="method">PUT</span><span>/items/{{id}}</span></div>
        <div class="endpoint"><span class="method">DELETE</span><span>/items/{{id}}</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/orders</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/orders / /orders/{{id}}</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/orders/{{id}}/pay | /cancel</span></div>
      </article>
      <article class="card"><h3>F/G. 上传 + 回显</h3>
        <div class="endpoint"><span class="method">POST</span><span>/upload/single</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/upload/multiple</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/upload/files</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/echo/query</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/echo/json</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/echo/form</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/echo/headers | /echo/cookies</span></div>
      </article>
      <article class="card"><h3>H/I/J/K. 其它训练模块</h3>
        <div class="endpoint"><span class="method">GET</span><span>/status/200..500</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/delay/{{seconds}}</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/flaky | /unstable</span></div>
        <div class="endpoint"><span class="method">POST</span><span>/idempotent/orders</span></div>
        <div class="endpoint"><span class="method">GET</span><span>/admin/stats | /admin/users</span></div>
      </article>
    </section>

    <footer>
      提示：返回结构统一为 <code>{{"code":0,"message":"success","data":...}}</code>。
      推荐先从 <code>/health</code> → <code>/auth/login</code> → 鉴权接口开始练习。
    </footer>
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html)
