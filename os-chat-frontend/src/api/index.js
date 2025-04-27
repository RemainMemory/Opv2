import axios from 'axios'

// 根据当前访问地址，动态设置 API_BASE
let API_BASE = '';

if (window.location.hostname === 'localhost' || window.location.hostname.startsWith('192.168.') || window.location.hostname === '127.0.0.1') {
  // 本地开发环境
  API_BASE = 'http://127.0.0.1:8000/api';  // 或者换成内网IP
} else {
  // 外网环境，使用公网域名
  API_BASE = 'http://chenfeiyu.asuscomm.com:8000/api'; // 这里换成你的外网域名
}

console.log('当前API_BASE:', API_BASE);

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE,
})

// 封装 API 请求

export async function getAnswer(query) {
  try {
    const response = await api.post('/get_answer', { query });
    return response.data.answer;
  } catch (error) {
    console.error('API 调用失败:', error);
    return '❌ 获取回答失败，请稍后重试。';
  }
}

export async function login(username, password) {
  try {
    const response = await api.post('/login', { username, password });
    return response.data;
  } catch (error) {
    console.error('登录失败:', error);
    return { success: false, message: '网络错误' };
  }
}

export async function register(username, password) {
  try {
    const response = await api.post('/register', { username, password });
    return response.data;
  } catch (error) {
    console.error('注册失败:', error);
    return { success: false, message: '网络错误' };
  }
}
