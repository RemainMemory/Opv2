<template>
  <div class="chat-container">
    <!-- 左侧历史记录栏 -->
    <div class="history-panel">
      <h3>历史记录</h3>
      <button class="new-chat" @click="createNewChat">＋ 新建聊天</button>
      <ul>
        <li
          v-for="(item, index) in chatHistories"
          :key="index"
          :class="{ active: index === currentSessionIndex }"
          @click="loadSession(index)"
        >
          {{ item.title }}
        </li>
      </ul>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="chat-area">
      <!-- 顶部导航栏 -->
      <header class="top-header">
        <button class="export-btn" @click="exportChat">导出对话</button>
        <div class="dropdown-wrapper" @click="toggleDropdown">
          <div class="dropdown-trigger">
            {{ username }}
            <span class="arrow">▾</span>
          </div>
          <div class="dropdown" v-if="showDropdown">
            <div @click.stop="logout">退出登录</div>
            <div @click.stop="switchUser">切换用户</div>
          </div>
        </div>
      </header>

      <!-- 聊天区域 -->
      <div class="chat-panel">
        <div class="chat-box" ref="chatBoxRef" @scroll="handleScroll">
          <div v-for="(item, index) in currentChat" :key="index" class="chat-item">
            <div class="message user">
              <div class="user-message">
                <span>{{ item.question }}</span>
              </div>
            </div>
            <div class="message bot">
              <div v-if="item.loading" class="bot-message">
                <div class="spinner"></div>
              </div>
              <div v-else class="bot-message">
                <span v-html="renderMarkdown(item.answer)"></span>
              </div>
            </div>
          </div>
          <button v-if="showScrollButton" class="scroll-bottom" @click="scrollToBottom">⬇️</button>
        </div>

        <!-- 输入区域 -->
        <div class="chat-input">
          <textarea
            ref="textareaRef"
            v-model="userInput"
            @input="autoResize"
            @keydown.enter.exact.prevent="sendQuestion"
            @keydown.shift.enter.exact.stop
            placeholder="请输入你的问题..."
          />
          <button @click="sendQuestion">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getAnswer } from '@/api'
import { marked } from 'marked'

const router = useRouter()
const username = ref('')
const userInput = ref('')
const chatHistories = ref([])
const currentSessionIndex = ref(0)
const currentChat = ref([])
const showDropdown = ref(false)
const showScrollButton = ref(false)

const chatBoxRef = ref(null)
const textareaRef = ref(null)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBoxRef.value) {
      chatBoxRef.value.scrollTo({
        top: chatBoxRef.value.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

const handleScroll = () => {
  if (!chatBoxRef.value) return
  const { scrollTop, scrollHeight, clientHeight } = chatBoxRef.value
  showScrollButton.value = scrollTop + clientHeight < scrollHeight - 50
}

const autoResize = () => {
  if (textareaRef.value) {
    const value = textareaRef.value.value.trim()
    if (value === '') {
      textareaRef.value.style.height = '50px'
    } else {
      textareaRef.value.style.height = 'auto'
      textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
    }
  }
}

onMounted(() => {
  const saved = localStorage.getItem('username')
  if (!saved) router.push('/login')
  username.value = saved
  chatBoxRef.value?.addEventListener('scroll', handleScroll)
  createNewChat()
})

onUnmounted(() => {
  chatBoxRef.value?.removeEventListener('scroll', handleScroll)
})

const logout = () => {
  localStorage.clear()
  router.push('/login')
}

const switchUser = () => {
  localStorage.removeItem('username')
  localStorage.removeItem('token')
  router.push('/login')
}

const renderMarkdown = (text) => marked.parse(text || '')

const createNewChat = () => {
  const title = `新对话 ${chatHistories.value.length + 1}`
  chatHistories.value.push({ title, records: [] })
  currentSessionIndex.value = chatHistories.value.length - 1
  currentChat.value = chatHistories.value[currentSessionIndex.value].records
  scrollToBottom()
}

const loadSession = (index) => {
  currentSessionIndex.value = index
  currentChat.value = chatHistories.value[index].records
  scrollToBottom()
}

const exportChat = () => {
  const session = chatHistories.value[currentSessionIndex.value]
  const blob = new Blob([JSON.stringify(session, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${session.title.replace(/\s+/g, '_')}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const sendQuestion = async () => {
  const question = userInput.value.trim()
  if (!question) return

  const newRecord = { question, answer: '', loading: true }
  currentChat.value.push(newRecord)
  userInput.value = ''
  await nextTick()
  autoResize()

  const index = currentChat.value.length - 1

  try {
    const answer = await getAnswer(question)
    currentChat.value[index].loading = false
    currentChat.value[index].answer = ''

    // 打字机效果
    for (let i = 0; i < answer.length; i++) {
      currentChat.value[index].answer += answer[i]
      await new Promise(resolve => setTimeout(resolve, 20))
      scrollToBottom()
    }

    await nextTick()
    textareaRef.value?.focus()
  } catch (err) {
    currentChat.value[index].answer = '❌ 获取回答失败，请稍后重试。'
    currentChat.value[index].loading = false
    scrollToBottom()
    await nextTick()
    textareaRef.value?.focus()
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background-color: #1e1e1e;
  color: white;
  font-family: 'Segoe UI', sans-serif;
  overflow: hidden;
}
.history-panel {
  width: 260px;
  background-color: #2a2a2a;
  border-right: 1px solid #333;
  padding: 16px;
  box-sizing: border-box;
  overflow-y: auto;
}
.history-panel h3 {
  margin: 0 0 12px;
}
.history-panel ul {
  list-style: none;
  padding: 0;
  margin: 8px 0 0 0;
}
.history-panel li {
  padding: 10px;
  border-bottom: 1px solid #3a3a3a;
  cursor: pointer;
  color: #ccc;
}
.history-panel li.active,
.history-panel li:hover {
  background-color: #3a3a3a;
  color: white;
}
.new-chat {
  background-color: #3a3a3a;
  color: white;
  border: none;
  width: 100%;
  padding: 8px;
  margin-bottom: 8px;
  border-radius: 6px;
  cursor: pointer;
}
.new-chat:hover {
  background-color: #4a4a4a;
}
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #1e1e1e;
}
.top-header {
  height: 48px;
  background-color: #151515;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
}
.export-btn {
  background-color: #3a3a3a;
  color: white;
  border: 1px solid #555;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.dropdown-wrapper {
  position: relative;
  display: inline-block;
}
.dropdown-trigger {
  background-color: #3a3a3a;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  user-select: none;
  display: flex;
  align-items: center;
}
.arrow {
  margin-left: 6px;
  font-size: 12px;
}
.dropdown {
  position: absolute;
  top: 36px;
  right: 0;
  background-color: #2f2f2f;
  border: 1px solid #444;
  border-radius: 6px;
  width: max-content;
  min-width: 120px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.6);
  z-index: 999;
}
.dropdown div {
  padding: 8px 12px;
  cursor: pointer;
  text-align: center;
}
.dropdown div:hover {
  background-color: #444;
}
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  position: relative;
}
.scroll-bottom {
  position: absolute;
  right: 16px;
  bottom: 16px;
  background: #444;
  border: none;
  color: white;
  padding: 6px 10px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
}

/* ✅ 一左一右 */
.message {
  display: flex;
  margin: 8px 0;
}
.message.user {
  justify-content: flex-end;
}
.message.bot {
  justify-content: flex-start;
}

/* ✅ 气泡宽度自适应 */
.user-message,
.bot-message {
  display: inline-block;
  padding: 10px 14px;
  border-radius: 10px;
  word-break: break-word;
  white-space: pre-wrap;
  max-width: 70%;
  min-width: 50px;
  width: fit-content;
}
.user-message {
  background-color: #444;
}
.bot-message {
  background-color: #2f2f2f;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #ccc;
  border-top: 3px solid #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.chat-input {
  display: flex;
  border-top: 1px solid #333;
  padding: 12px;
  background-color: #1e1e1e;
}
.chat-input textarea {
  flex: 1;
  resize: none;
  min-height: 50px;
  max-height: 200px;
  padding: 10px;
  background-color: #333;
  color: white;
  border: none;
  font-size: 16px;
  border-radius: 6px 0 0 6px;
  line-height: 1.5;
  overflow-y: hidden;
}
.chat-input button {
  background-color: #3a3a3a;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
  font-size: 16px;
  border-left: 1px solid #555;
}
</style>
