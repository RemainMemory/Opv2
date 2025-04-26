// src/api/index.js
import axios from 'axios'


const API_BASE = 'http://127.0.0.1:8000/api'


export async function getAnswer(query) {
  try {
    const response = await axios.post(`${API_BASE}/get_answer`, {
      query: query
    })
    return response.data.answer
  } catch (error) {
    console.error('API 调用失败:', error)
    return '❌ 获取回答失败，请稍后重试。'
  }
}

export async function login(username, password) {
  try {
    const response = await axios.post(`${API_BASE}/login`, { username, password })
    return response.data
  } catch (err) {
    return { success: false, message: '网络错误' }
  }
}

export async function register(username, password) {
  try {
    const response = await axios.post(`${API_BASE}/register`, { username, password })
    return response.data
  } catch (err) {
    return { success: false, message: '网络错误' }
  }
}
