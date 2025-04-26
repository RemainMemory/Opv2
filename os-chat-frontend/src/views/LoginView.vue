<template>
  <div class="login-container">
    <h2>{{ isRegister ? '用户注册' : '用户登录' }}</h2>
    <input v-model="username" placeholder="用户名" />
    <input
      v-model="password"
      type="password"
      placeholder="密码"
      @keyup.enter="handleSubmit"
    />
    <button @click="handleSubmit">{{ isRegister ? '注册' : '登录' }}</button>
    <p class="switch-mode" @click="toggleMode">
      {{ isRegister ? '已有账号？点击登录' : '没有账号？点击注册' }}
    </p>
    <p class="error" v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '@/api'

const username = ref('')
const password = ref('')
const isRegister = ref(false)
const error = ref('')
const router = useRouter()

const toggleMode = () => {
  isRegister.value = !isRegister.value
  error.value = ''
}

const handleSubmit = async () => {
  if (!username.value || !password.value) {
    error.value = '用户名和密码不能为空'
    return
  }

  const api = isRegister.value ? register : login
  const res = await api(username.value, password.value)

  if (res.success) {
    localStorage.setItem('username', username.value)
    localStorage.setItem('token', res.token || 'mock-token')
    router.push('/')
  } else {
    error.value = res.message || (isRegister.value ? '注册失败' : '登录失败')
  }
}
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 120px auto;
  padding: 2rem;
  background: #1e1e1e;
  border-radius: 10px;
  box-shadow: 0 0 10px #000;
  display: flex;
  flex-direction: column;
  align-items: center;
}
input {
  margin: 0.5rem 0;
  padding: 0.5rem;
  width: 100%;
  background: #333;
  border: none;
  border-radius: 5px;
  color: white;
}
button {
  margin-top: 1rem;
  width: 100%;
  padding: 10px;
  background-color: #3a3a3a;           /* ✅ 改为灰色按钮 */
  border: 1px solid #555;
  color: white;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
button:hover {
  background-color: #4a4a4a;           /* ✅ 鼠标悬停变深 */
}
.switch-mode {
  margin-top: 1rem;
  font-size: 14px;
  color: #999;
  cursor: pointer;
}
.error {
  color: red;
  margin-top: 0.5rem;
  font-size: 14px;
}
</style>
