# API Testing Playground

一个用于学习与练习接口测试的 FastAPI 靶场项目，覆盖认证、CRUD、分页过滤排序、状态码、文件上传、超时重试、幂等、权限控制、接口依赖等常见场景。

## 1. 项目简介
- 面向 Postman / Apifox / curl / pytest + requests 练习。
- 统一响应结构：
  - 成功：`{"code":0,"message":"success","data":...}`
  - 失败：`{"code":业务码,"message":"错误信息","data":null|详情}`
- HTTP 状态码用于传输层语义，`code` 用于业务错误语义。

## 2. 技术栈
- Python 3.12
- FastAPI + Uvicorn
- SQLite + SQLAlchemy
- Caddy（反向代理）
- 密码哈希：PBKDF2-HMAC-SHA256（避免 bcrypt/passlib 兼容性问题）

## 3. 目录结构
```text
api-playground/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── deps.py
│   ├── utils/
│   │   ├── response.py
│   │   ├── auth.py
│   │   ├── validators.py
│   │   └── seed.py
│   └── routers/
│       ├── auth.py
│       ├── users.py
│       ├── items.py
│       ├── orders.py
│       ├── upload.py
│       ├── delay.py
│       ├── status.py
│       ├── echo.py
│       ├── idempotent.py
│       └── admin.py
├── data/
├── uploads/
├── requirements.txt
├── README.md
├── Caddyfile
├── start.sh
└── .env.example
```

## 4. 本地运行步骤
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
./start.sh
```

## 5. VPS 部署步骤（Linux）
1. 上传代码到服务器。
2. 安装 Python3.12、pip、虚拟环境。
3. 创建并激活虚拟环境，安装依赖。
4. 配置 `.env`。
5. `./start.sh` 启动服务（建议配合 systemd 守护）。
6. 安装 Caddy，并使用本文 `Caddyfile` 反代到 `127.0.0.1:8000`。

## 6. Caddy 配置说明
- `:80` 是纯 IP 访问写法。
- 域名写法见 `Caddyfile` 注释块，替换成你的实际域名。

## 7. Swagger 文档地址
- `http://<host>:8000/docs`
- `http://<host>:8000/redoc`
- `http://<host>:8000/` 为可视化首页（项目介绍 + 接口总览）

## 8. 默认账号
- 管理员：`admin / Admin123456`
- 普通用户：`tester / Test123456`

> 首次启动自动建表并初始化测试数据。

## 9. 如何在 Postman 中练习
1. 建立 Environment：`base_url`、`token`。
2. 先请求 `POST /auth/login`，Tests 脚本提取 token：
   ```js
   const json = pm.response.json();
   pm.environment.set("token", json.data.access_token);
   ```
3. 需要鉴权的请求头设置：`Authorization: Bearer {{token}}`。
4. 以 Collection 组织：auth/users/items/orders/upload/status/delay/idempotent/admin。

## 10. 各接口模块说明
- 基础：`GET /`（炫酷可视化首页）, `GET /health`（JSON 健康检查）
- 认证：`/auth/register`, `/auth/login`, `/auth/profile`, `/auth/logout`, `/auth/forbidden-demo`
- 用户：`/users` CRUD（软删除）
- 商品：`/items` CRUD（含分页过滤排序）
- 订单：`/orders` 创建/查询/支付/取消（含库存与状态流转）
- 上传：`/upload/single`, `/upload/multiple`, `/upload/files`
- 回显：`/echo/query|json|form|headers|cookies`
- 状态码演示：`/status/200|201|400|401|403|404|409|422|500`
- 稳定性：`/delay/{seconds}`, `/flaky`, `/unstable`
- 幂等：`POST /idempotent/orders` + `Idempotency-Key`
- 管理员：`/admin/stats`, `/admin/users`

## 11. 典型测试点说明
- 必填字段缺失/类型错误/长度超限/枚举非法。
- token 缺失、伪造、过期（通过缩短过期时间模拟）。
- 404（不存在 ID）、409（重复/冲突）、422（参数校验失败）。
- 订单场景：库存不足、重复支付、重复取消、非法状态流转。
- 文件上传：错误 content-type、缺文件字段、超大小、非法扩展名。

## 12. 常见报错说明
- `422 validation error`：请求体/参数结构不符合定义。
- `401 missing bearer token / invalid token`：未携带或 token 不合法。
- `403 admin required`：普通用户访问管理员接口。
- `409 stock not enough / already paid`：业务状态冲突。

---

## 《Postman / 接口测试练习路线》

### 第1阶段：基础请求
- `GET /health`
- `GET /echo/query?name=test`
- 断言：状态码、`code`、`message`、`data` 字段。

### 第2阶段：请求参数
- params：`GET /users?page=1&page_size=5`
- path：`GET /users/{id}`
- JSON body：`POST /items`
- form-data：`POST /upload/single`
- x-www-form-urlencoded：`POST /echo/form`

### 第3阶段：认证与鉴权
- 注册：`POST /auth/register`
- 登录：`POST /auth/login`
- 提取 token 后访问：`GET /auth/profile`
- 覆盖：token 缺失、token 错误、普通用户访问 admin。

### 第4阶段：CRUD
- users：新增→查询→更新(PUT/PATCH)→删除
- items：新增→查询→更新→删除
- 做前置依赖与后置断言（如总数、字段变化）。

### 第5阶段：分页/过滤/排序
- `page/page_size`
- `keyword`
- `sort_by/order`
- `status/category`

### 第6阶段：业务流测试
- 创建订单 `POST /orders`
- 支付 `POST /orders/{id}/pay`
- 再次支付（预期 409）
- 库存不足（预期 409）
- 取消订单（测试非法状态流转）

### 第7阶段：文件上传
- 单文件、多文件上传
- 非法类型（如 `.exe`）
- 超大文件（超过 `MAX_UPLOAD_SIZE_MB`）

### 第8阶段：异常测试
- `/status/*` 系列全覆盖
- 缺字段、类型错、越界值、非法 ID。

### 第9阶段：稳定性与超时
- `GET /delay/5`
- `GET /flaky`
- `GET /unstable`
- 在客户端配置 timeout + retry 观察行为。

### 第10阶段：幂等与权限
- `POST /idempotent/orders` 携带 `Idempotency-Key`
- 同 key + 同 body 重试应返回同结果
- 同 key + 不同 body 应 409
- admin 与普通用户访问 `/admin/*` 的差异。

### 第11阶段：自动化扩展（pytest + requests）
建议先写 3~5 个最小自动化用例：
1. 登录成功并缓存 token。
2. 未带 token 访问 `/auth/profile` 断言 401。
3. 创建商品后查询详情断言字段。
4. 订单重复支付断言 409 与业务码。
5. 幂等 key 重放断言返回同一订单 ID。

---

## 模块设计说明（简版）
- `config.py`: 环境变量配置中心。
- `database.py`: SQLite 引擎与会话。
- `models.py`: User/Item/Order/TokenBlacklist/IdempotencyRecord。
- `schemas.py`: Pydantic 请求响应模型与字段校验。
- `deps.py`: 鉴权依赖、管理员权限依赖。
- `utils/response.py`: 统一响应结构。
- `utils/auth.py`: 密码哈希、JWT 生成与解析。
- `utils/seed.py`: 首次数据初始化。
- `routers/*.py`: 按业务模块拆分路由，便于测试组织。

## 启动命令
```bash
./start.sh
```

## 访问地址示例
- 首页（可视化接口导航）：`http://127.0.0.1:8000/`
- 健康检查（JSON）：`http://127.0.0.1:8000/health`
- 文档：`http://127.0.0.1:8000/docs`

## 最值得优先练习的 10 个接口
1. `POST /auth/login`
2. `GET /auth/profile`
3. `GET /users`
4. `POST /items`
5. `POST /orders`
6. `POST /orders/{order_id}/pay`
7. `POST /upload/single`
8. `GET /status/422`
9. `GET /unstable`
10. `POST /idempotent/orders`
