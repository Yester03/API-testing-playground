from fastapi.responses import HTMLResponse


_TEMPLATE = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>__APP_NAME__</title>
  <style>
    :root {--bg:#0d0b14;--panel:#1d1630cc;--line:#3c2f65;--text:#f8efff;--muted:#bda8d6;--ok:#9effd0;}
    * { box-sizing: border-box; }
    body {margin:0;font-family:"Inter","Segoe UI","PingFang SC",sans-serif;color:var(--text);
      background:radial-gradient(circle at 12% 10%,#3f1a57 0%,transparent 30%),radial-gradient(circle at 85% 20%,#1c2d68 0%,transparent 30%),linear-gradient(160deg,#0d0b14 0%,#130f1f 100%);}
    .wrap {max-width:1200px;margin:0 auto;padding:30px 20px 50px;}
    .hero {border:1px solid var(--line);background:linear-gradient(145deg,#1f1633e8,#120d22e8);border-radius:22px;padding:28px;box-shadow:0 20px 60px #00000080;}
    .badge {display:inline-flex;padding:6px 12px;border:1px solid #6c4b8f;border-radius:99px;color:var(--ok);background:#241a3890;font-size:13px;}
    h1 {margin:14px 0 10px;font-size:clamp(28px,4vw,44px);}
    .subtitle {color:var(--muted);line-height:1.8;max-width:860px;}
    .row,.api-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;}
    .api-grid {grid-template-columns:repeat(auto-fit,minmax(320px,1fr));margin-top:18px;}
    .card {border:1px solid var(--line);background:var(--panel);border-radius:16px;padding:16px 18px;}
    .card h3 {margin:0 0 10px;color:#ffd2f0;font-size:18px;}
    .card li {margin:7px 0;color:#dfcaef;}
    .pill {display:inline-block;margin:4px 6px 0 0;font-size:12px;padding:4px 9px;border-radius:999px;background:#2a1f42;border:1px solid #5e4b8f;color:#d3c3ff;}
    a {color:#ffd0ef;text-decoration:none;border-bottom:1px dashed #a087d3;}
    .endpoint {display:flex;justify-content:space-between;gap:10px;align-items:center;border:1px solid #4f3c7a;border-radius:12px;padding:10px 12px;margin:8px 0;background:#1a143090;font-size:14px;cursor:pointer;}
    .endpoint:hover {border-color:#a67dff;background:#241940;}
    .method {min-width:52px;text-align:center;font-weight:700;border-radius:8px;padding:4px 7px;border:1px solid #8d6aca;background:#2f2052;color:#ffe3f4;}
    .endpoint-path {flex:1;}
    .example {margin-top:18px;border:1px solid #5e4b8f;border-radius:14px;background:#140f25;padding:14px;display:none;}
    .example.show {display:block;}
    pre {white-space:pre-wrap;word-break:break-word;background:#0f0b1d;border:1px solid #3d3263;border-radius:10px;padding:10px;color:#e7d8ff;}
    .mini {color:#b5a3d3;font-size:13px;}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <span class="badge">API Testing Playground · v__VERSION__</span>
      <h1>__APP_NAME__</h1>
      <p class="subtitle">用于练习接口测试：认证鉴权、CRUD、分页/过滤/排序、状态码断言、文件上传、超时重试、幂等、管理员权限、订单状态流转。</p>
      <div><span class="pill">JWT</span><span class="pill">统一响应</span><span class="pill">SQLite</span><span class="pill">幂等</span><span class="pill">Flaky/Unstable</span></div>
      <div class="row" style="margin-top:16px;">
        <div class="card"><h3>快速入口</h3><ul><li><a href="/docs">/docs</a></li><li><a href="/redoc">/redoc</a></li><li><a href="/health">/health</a></li></ul></div>
        <div class="card"><h3>默认账号</h3><ul><li>admin / Admin123456</li><li>tester / Test123456</li></ul></div>
      </div>
    </section>

    <section class="api-grid">
      <article class="card"><h3>A. 基础</h3>
        <div class="endpoint" data-key="health"><span class="method">GET</span><span class="endpoint-path">/health</span></div>
      </article>
      <article class="card"><h3>B. 认证</h3>
        <div class="endpoint" data-key="register"><span class="method">POST</span><span class="endpoint-path">/auth/register</span></div>
        <div class="endpoint" data-key="login"><span class="method">POST</span><span class="endpoint-path">/auth/login</span></div>
        <div class="endpoint" data-key="profile"><span class="method">GET</span><span class="endpoint-path">/auth/profile</span></div>
      </article>
      <article class="card"><h3>C. 用户</h3>
        <div class="endpoint" data-key="users"><span class="method">GET</span><span class="endpoint-path">/users?page=1&page_size=5</span></div>
        <div class="endpoint" data-key="create_user"><span class="method">POST</span><span class="endpoint-path">/users</span></div>
        <div class="endpoint" data-key="user_detail"><span class="method">GET</span><span class="endpoint-path">/users/{id}</span></div>
      </article>
      <article class="card"><h3>D/E. 商品 + 订单</h3>
        <div class="endpoint" data-key="items"><span class="method">GET</span><span class="endpoint-path">/items</span></div>
        <div class="endpoint" data-key="create_item"><span class="method">POST</span><span class="endpoint-path">/items</span></div>
        <div class="endpoint" data-key="order"><span class="method">POST</span><span class="endpoint-path">/orders</span></div>
      </article>
      <article class="card"><h3>F/G. 上传 + 回显</h3>
        <div class="endpoint" data-key="upload"><span class="method">POST</span><span class="endpoint-path">/upload/single</span></div>
        <div class="endpoint" data-key="echo"><span class="method">POST</span><span class="endpoint-path">/echo/json</span></div>
      </article>
      <article class="card"><h3>H/I/J/K. 其它训练模块</h3>
        <div class="endpoint" data-key="status"><span class="method">GET</span><span class="endpoint-path">/status/422</span></div>
        <div class="endpoint" data-key="delay"><span class="method">GET</span><span class="endpoint-path">/delay/{seconds}</span></div>
        <div class="endpoint" data-key="idempotent"><span class="method">POST</span><span class="endpoint-path">/idempotent/orders</span></div>
        <div class="endpoint" data-key="admin"><span class="method">GET</span><span class="endpoint-path">/admin/stats</span></div>
      </article>
    </section>

    <section id="example" class="example">
      <h3 id="ex-title">接口示例</h3>
      <div class="mini" id="ex-desc"></div>
      <h4>请求示例</h4>
      <pre id="ex-req"></pre>
      <h4>返回示例</h4>
      <pre id="ex-res"></pre>
    </section>
  </div>
<script>
const examples = {
  health:{title:'GET /health',desc:'基础连通性测试',req:'curl http://127.0.0.1:8000/health',res:'{\n  "code": 0,\n  "message": "success",\n  "data": {"status": "ok", "env": "dev"}\n}'},
  register:{title:'POST /auth/register',desc:'注册用户',req:'curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d "{\\"username\\":\\"newuser\\",\\"email\\":\\"new@test.com\\",\\"password\\":\\"Test123456\\",\\"role\\":\\"user\\",\\"status\\":\\"active\\"}"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"id":3,"username":"newuser"}\n}'},
  login:{title:'POST /auth/login',desc:'登录换取 token',req:'curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\\"username\\":\\"admin\\",\\"password\\":\\"Admin123456\\"}"',res:'{\n  "code": 0,\n  "message": "success",\n  "data": {"access_token":"...","token_type":"bearer","expires_in":7200}\n}'},
  profile:{title:'GET /auth/profile',desc:'需要 Bearer Token',req:'curl http://127.0.0.1:8000/auth/profile -H "Authorization: Bearer <TOKEN>"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"id":1,"username":"admin","role":"admin"}\n}'},
  users:{title:'GET /users',desc:'分页/过滤/排序',req:'curl "http://127.0.0.1:8000/users?page=1&page_size=5" -H "Authorization: Bearer <TOKEN>"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"total":2,"list":[...] }\n}'},
  create_user:{title:'POST /users',desc:'创建用户(201)',req:'curl -X POST http://127.0.0.1:8000/users -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\\"username\\":\\"u001\\",\\"email\\":\\"u001@test.com\\",\\"password\\":\\"Test123456\\",\\"role\\":\\"user\\",\\"status\\":\\"active\\"}"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"id":3,"username":"u001"}\n}'},
  user_detail:{title:'GET /users/{id}',desc:'单用户查询',req:'curl http://127.0.0.1:8000/users/1 -H "Authorization: Bearer <TOKEN>"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"id":1,"username":"admin"}\n}'},
  items:{title:'GET /items',desc:'商品查询',req:'curl "http://127.0.0.1:8000/items?page=1&page_size=10"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"total":3,"list":[...]}\n}'},
  create_item:{title:'POST /items',desc:'新建商品',req:'curl -X POST http://127.0.0.1:8000/items -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\\"name\\":\\"Pen\\",\\"price\\":2.5,\\"stock\\":10,\\"category\\":\\"stationery\\",\\"tags\\":[\\"new\\"],\\"is_active\\":true}"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"id":4,"name":"Pen"}\n}'},
  order:{title:'POST /orders',desc:'下单并扣减库存',req:'curl -X POST http://127.0.0.1:8000/orders -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\\"user_id\\":2,\\"item_id\\":1,\\"quantity\\":1}"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"id":1,"status":"created"}\n}'},
  upload:{title:'POST /upload/single',desc:'multipart 文件上传',req:'curl -X POST http://127.0.0.1:8000/upload/single -F "file=@demo.txt"',res:'{\n  "code":0,\n  "message":"uploaded",\n  "data":{"filename":"demo.txt","size":11}\n}'},
  echo:{title:'POST /echo/json',desc:'回显 JSON body',req:'curl -X POST http://127.0.0.1:8000/echo/json -H "Content-Type: application/json" -d "{\\"hello\\":\\"world\\"}"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"hello":"world"}\n}'},
  status:{title:'GET /status/422',desc:'状态码演示',req:'curl http://127.0.0.1:8000/status/422',res:'{\n  "code":1422,\n  "message":"validation demo",\n  "data":null\n}'},
  delay:{title:'GET /delay/{seconds}',desc:'超时与重试训练',req:'curl http://127.0.0.1:8000/delay/3',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"delayed":3}\n}'},
  idempotent:{title:'POST /idempotent/orders',desc:'幂等键重放测试',req:'curl -X POST http://127.0.0.1:8000/idempotent/orders -H "Authorization: Bearer <TOKEN>" -H "Idempotency-Key: key-1001" -H "Content-Type: application/json" -d "{\\"user_id\\":2,\\"item_id\\":1,\\"quantity\\":1}"',res:'{\n  "code":0,\n  "message":"success|idempotent replay",\n  "data":{"id":2,...}\n}'},
  admin:{title:'GET /admin/stats',desc:'管理员权限接口',req:'curl http://127.0.0.1:8000/admin/stats -H "Authorization: Bearer <ADMIN_TOKEN>"',res:'{\n  "code":0,\n  "message":"success",\n  "data":{"users":2,"items":3,"orders":1}\n}'}
};
for (const node of document.querySelectorAll('.endpoint')) {
  node.addEventListener('click', () => {
    const ex = examples[node.dataset.key];
    if (!ex) return;
    document.getElementById('example').classList.add('show');
    document.getElementById('ex-title').textContent = ex.title;
    document.getElementById('ex-desc').textContent = ex.desc;
    document.getElementById('ex-req').textContent = ex.req;
    document.getElementById('ex-res').textContent = ex.res;
  });
}
</script>
</body>
</html>
"""


def render_homepage(app_name: str, version: str) -> HTMLResponse:
    html = _TEMPLATE.replace("__APP_NAME__", app_name).replace("__VERSION__", version)
    return HTMLResponse(content=html)
