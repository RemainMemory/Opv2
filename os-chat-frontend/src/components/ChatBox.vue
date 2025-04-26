<!-- src/components/ChatBox.vue -->
<template>
  <div class="chat-container">
    <div class="chat-history">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <strong>{{ msg.role === 'user' ? '你' : '助手' }}</strong>: {{ msg.text }}
      </div>
    </div>

    <div class="chat-input">
      <input
        v-model="input"
        @keydown.enter="sendMessage"
        placeholder="请输入你的问题..."
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import { getAnswer } from '../api'

export default {
  data() {
    return {
      input: '',
      messages: [],
    }
  },
  methods: {
    async sendMessage() {
      if (!this.input.trim()) return

      const question = this.input.trim()
      this.messages.push({ role: 'user', text: question })
      this.input = ''

      try {
        const reply = await getAnswer(question)
        this.messages.push({ role: 'assistant', text: reply })
      } catch (err) {
        this.messages.push({
          role: 'assistant',
          text: '❌ 回答失败，请稍后再试',
        })
      }
    },
  },
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 1rem;
  font-family: sans-serif;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 1rem;
  background: #f9f9f9;
}

.message {
  margin-bottom: 1rem;
}

.message.user {
  text-align: right;
}

.message.assistant {
  text-align: left;
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.chat-input input {
  flex: 1;
  padding: 0.5rem;
  font-size: 16px;
}

.chat-input button {
  padding: 0.5rem 1rem;
  font-size: 16px;
}
</style>
