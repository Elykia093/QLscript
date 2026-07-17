'use strict';

const DEFAULT_SEPARATORS = ['\n', '&', '#'];
const ERROR_DETAIL_LIMIT = 1000;
const SENSITIVE_FIELD_PATTERN = /token|cookie|authorization|password|secret|signature|^sign$|api[_-]?key/i;

function splitAccounts(rawValue, separators = DEFAULT_SEPARATORS) {
  if (!rawValue) {
    return [];
  }

  const normalized = rawValue.replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();
  if (!normalized) {
    return [];
  }

  for (const separator of separators) {
    if (normalized.includes(separator)) {
      return normalized
        .split(separator)
        .map(item => item.trim())
        .filter(Boolean);
    }
  }

  return [normalized];
}

function splitJsonAccounts(rawValue) {
  if (!rawValue) {
    return [];
  }

  const normalized = rawValue.replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();
  if (!normalized) {
    return [];
  }

  try {
    JSON.parse(normalized);
    return [normalized];
  } catch {
    return splitAccounts(normalized);
  }
}

function maskSecret(value, keep = 4) {
  const text = String(value || '').trim();
  if (text.length <= keep * 2) {
    return '***';
  }
  return `${text.slice(0, keep)}***${text.slice(-keep)}`;
}

function errorMessage(error) {
  const message = error instanceof Error ? error.message : String(error);
  return message.replace(/([?&][^=\s&]+)=([^&\s]+)/g, '$1=***');
}

function safeErrorDetail(data, isJson) {
  const detail = isJson
    ? JSON.stringify(data, (key, value) => (
      key && SENSITIVE_FIELD_PATTERN.test(key) ? '***' : value
    ))
    : data.raw;
  const safeDetail = errorMessage(detail);
  return safeDetail.length > ERROR_DETAIL_LIMIT
    ? `${safeDetail.slice(0, ERROR_DETAIL_LIMIT)}...`
    : safeDetail;
}

function formatResults(results) {
  return results
    .map(result => `${result.ok ? '成功' : '失败'} | 账号${result.index} | ${result.title}: ${result.message}`)
    .join('\n');
}

async function sendNotification(title, content) {
  console.log(`\n${title}\n${content}`);

  let sendNotify;
  try {
    ({ sendNotify } = require('../sendNotify'));
  } catch (error) {
    console.log('未检测到青龙 sendNotify.js，已降级为控制台输出。');
    return;
  }

  try {
    await sendNotify(title, content);
  } catch (error) {
    console.log(`通知发送失败: ${error.message || error}`);
  }
}

async function requestJson(url, options = {}) {
  const timeout = options.timeout || 15000;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      method: options.method || 'GET',
      headers: options.headers,
      body: options.body,
      signal: controller.signal,
    });

    const text = await response.text();
    let data;
    let isJson = true;
    try {
      data = text ? JSON.parse(text) : {};
    } catch (error) {
      data = { raw: text };
      isJson = false;
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${safeErrorDetail(data, isJson)}`);
    }

    return data;
  } finally {
    clearTimeout(timer);
  }
}

module.exports = {
  splitAccounts,
  splitJsonAccounts,
  maskSecret,
  errorMessage,
  formatResults,
  sendNotification,
  requestJson,
};
