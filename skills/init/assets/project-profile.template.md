# 项目画像：工程证据与交付上下文

> 本画像为 `/probe` 和 `/align` 记录证据及待确认项，不替代生产事实源。`Unknown` 表示当前缺乏证据，不代表物理上没有限制或控制。

## 采集信息

- 更新时间：`Unknown`
- 采集者/工具版本：`Unknown`
- 仓库/修订版本：`Unknown`
- 采集方式：`人工 / 扫描 / 混合`

## 仓库事实

| 字段 | 值 | 置信状态 | 证据（路径/命令和日期） | 验证方式/冲突 |
|---|---|---|---|---|
| 语言与版本 | Unknown | Unknown | Unknown | 检查清单文件和 CI 运行时 |
| 框架与包管理器 | Unknown | Unknown | Unknown | 检查依赖声明和锁文件 |
| 构建、测试、Lint 命令 | Unknown | Unknown | Unknown | 优先核对 CI 实际使用命令 |
| 服务/部署形态 | Unknown | Unknown | Unknown | 向部署负责人确认 |
| 存储和外部依赖 | Unknown | Unknown | Unknown | 静态引用不等于生产接入 |
| Agent 指令及适用范围 | Unknown | Unknown | Unknown | 记录根目录和嵌套指令路径 |
| 受保护路径/迁移规则 | Unknown | Unknown | Unknown | 与当前项目规则核对 |

## 运行时与 AI 工作负载约束

| 约束 | 值 | 置信状态 | 证据/测量方式 | 负责人 |
|---|---|---|---|---|
| 部署目标与硬件 | Unknown | Unknown | Unknown | Unknown |
| RAM/GPU 显存限制 | Unknown | Unknown | 配置值不等于生产环境可用容量 | Unknown |
| 模型/供应商与端点类型 | Unknown | Unknown | 不记录凭据或密钥 URL | Unknown |
| 输入规模和流量分布 | Unknown | Unknown | 测量代表性样本 | Unknown |
| 并发/速率限制 | Unknown | Unknown | 压测或供应商限制 | Unknown |
| 延迟 SLO（含分位数与测量边界） | Unknown | Unknown | 说明是否含排队/网络/模型耗时 | Unknown |
| 成本预算 | Unknown | Unknown | 写明币种、周期和计算口径 | Unknown |

## 智能硬件 / 具身系统上下文（按产品形态填写）

| 字段 | 值 | 置信状态 | 证据/验证方式 | 负责人 |
|---|---|---|---|---|
| 产品形态、预期用途和使用环境 | Unknown | Unknown | 明确家庭/办公/户外/专业等场景 | Unknown |
| 硬件型号、板卡/器件与修订版本 | Unknown | Unknown | 以 BOM、硬件版本或设备清单为准 | Unknown |
| 处理器/加速器、内存/存储、供电/电池/散热预算 | Unknown | Unknown | 规格和目标设备实测需分别记录 | Unknown |
| 传感器、执行器和设备控制接口 | Unknown | Unknown | 写明单位、坐标/方向、限位与控制边界 | Unknown |
| 固件、操作系统、驱动与通信链路 | Unknown | Unknown | 记录兼容矩阵和断连/升级行为 | Unknown |
| AI 推理位置及设备/边缘/云端依赖 | Unknown | Unknown | 记录在线、离线和网络退化行为 | Unknown |
| 物理危险、保护措施、急停/安全停止 | Unknown | Unknown | 由产品安全/硬件负责人做风险分析 | Unknown |
| 验证阶段与证据等级 | Unknown | Unknown | 仿真、台架、实机受控测试、现场试点需区分 | Unknown |

## FDE / 交付上下文（按需填写）

| 字段 | 值 | 置信状态 | 证据/负责人 |
|---|---|---|---|
| 客户/业务问题与用户角色 | Unknown | Unknown | 使用脱敏记录；标明决策人 |
| 客户环境与集成边界 | Unknown | Unknown | 网络、身份、部署和数据约束 |
| 数据分类、驻留和留存 | Unknown | Unknown | 与客户/安全负责人确认 |
| Demo/试点/生产范围 | Unknown | Unknown | 记录明确不包含的事项 |
| 验收证据与验收人 | Unknown | Unknown | 定义可观察的成功标准 |
| 回滚/关闭机制 | Unknown | Unknown | 按 Web/API/CLI/Worker 形态选择 |

## 生命周期与决策记录

- 试点观察窗口：Unknown（由业务负责人确定）
- 最小代表性样本量：Unknown（由业务负责人确定）
- 业务效果/质量/可靠性指标和阈值：Unknown
- 去留决策人：Unknown
- 技术回滚/关闭负责人：Unknown
- 数据处置与留存规则：Unknown（按政策确认，不编造期限）
- 关闭/回滚方法及验证状态：Unknown

## 置信状态定义

- `Confirmed`：由当前配置、CI 执行、测量结果或负责人明确确认直接支持，并写明证据。若依赖人工陈述，记录确认人角色和日期。
- `Inferred`：由间接证据推断，需写明推断依据和验证办法。
- `Unknown`：尚未建立，保留为问题或验证任务，不用默认值悄悄替代。

这里的 `Confirmed` 只表示画像中的事实有直接证据支持，不代表业务批准、需求签字或安全授权。审批/决策状态应单独记录在项目的契约或决策记录中。

## 待裁决事项/证据冲突

| 决策或冲突 | 影响 | 各方证据 | 负责人 | 截止/验证方式 |
|---|---|---|---|---|
| 暂无记录 | — | — | — | — |
