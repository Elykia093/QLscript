'use strict';

const DEFAULT_SEPARATORS = ['\n', '&', '#'];

function splitAccounts(rawValue, separators = DEFAULT_SEPARATORS) {
  if (!rawValue) {
    return [];
  }

  const normalized = rawValue.replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim();
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

function maskSecret(value, keep = 4) {
  const text = String(value || '').trim();
  if (text.length <= keep * 2) {
    return '***';
  }
  return `${text.slice(0, keep)}***${text.slice(-keep)}`;
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
    try {
      data = text ? JSON.parse(text) : {};
    } catch (error) {
      data = { raw: text };
    }

    if (!response.ok) {
      const detail = data && data.raw ? data.raw : JSON.stringify(data);
      throw new Error(`HTTP ${response.status}: ${detail}`);
    }

    return data;
  } finally {
    clearTimeout(timer);
  }
}

module.exports = {
  splitAccounts,
  maskSecret,
  sendNotification,
  requestJson,
};
