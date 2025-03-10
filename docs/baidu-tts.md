# 百度语音合成免费额度获取指南 / Baidu Speech Synthesis Free Quota Guide

## 简介 / Introduction
本文档详细说明如何通过百度智能云平台获取语音合成（TTS）服务的免费额度（每日200次请求），并获取应用所需的 `APP_ID`、`API_KEY` 和 `SECRET_KEY`。  
This document explains how to obtain the free quota (200 daily requests) for Baidu's Speech Synthesis (TTS) service through Baidu Intelligent Cloud, and how to get the required `APP_ID`, `API_KEY`, and `SECRET_KEY`.

---

## 准备工作 / Prerequisites
### 中文
1. **注册百度账号**
   - 访问 [百度智能云官网](https://cloud.baidu.com/)
   - 点击右上角"注册"按钮，完成账号注册
2. **实名认证（必需）**
   - 登录后进入"控制台"
   - 点击顶部导航栏"实名认证"
   - 选择个人/企业认证方式并完成验证

### English
1. **Create a Baidu Account**
   - Visit [Baidu Intelligent Cloud](https://cloud.baidu.com/)
   - Click "Sign Up" at the top-right corner
2. **Real-Name Verification (Mandatory)**
   - After login, go to the **Console**
   - Click "Real-Name Verification" in the top navigation bar
   - Complete verification as an individual or enterprise

---

## 创建语音合成应用 / Create a Speech Synthesis Application
### 步骤1：进入语音合成服务 / Step 1: Access the TTS Service
**中文**  
1. 登录后进入[控制台](https://console.bce.baidu.com/)
2. 导航至：左侧栏"产品服务" → "人工智能" → "语音技术"
3. 选择"语音合成"

**English**  
1. Log in to the [Console](https://console.bce.baidu.com/)
2. Navigate to: Left sidebar → "Products" → "AI Services" → "Speech Technology"
3. Select "Speech Synthesis"

---

### 步骤2：创建新应用 / Step 2: Create a New Application
**中文**  
1. 点击"创建应用"
2. 填写信息：
   - 应用名称：自定义（如 `MyTTSApp`）
   - 应用分类：选择"工具类"
   - 接口选择：勾选"语音合成 REST API"
3. 勾选协议并点击"立即创建"

**English**  
1. Click "Create Application"
2. Fill in details:
   - **Application Name**: Custom (e.g., `MyTTSApp`)
   - **Category**: Select "Tools"
   - **APIs**: Check "Speech Synthesis REST API"
3. Agree to the terms and click "Create"

---

## 获取密钥信息 / Obtain API Credentials
**中文**  
1. 进入[应用列表](https://console.bce.baidu.com/ai/#/ai/speech/app/list)
2. 找到目标应用，点击"查看应用详情"
3. 获取以下信息：