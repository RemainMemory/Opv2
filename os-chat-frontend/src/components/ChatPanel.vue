<template>
    <div class="chat-container">
      <div class="chat-messages" ref="chatRef">
        <div v-for="(msg, index) in messages" :key="index" class="message" :class="msg.role">
          <strong>{{ msg.role === 'user' ? '你' : '助手' }}：</strong>
          <div class="markdown" v-html="renderMarkdown(msg.content)" />
        </div>
      </div>
      <div class="chat-input">
        <input
          class="input"
          :value="userInput"
          @input="e => emit('update:userInput', e.target.value)"
          @keydown.enter="$emit('send')"
          placeholder="请输入你的问题..."
        />
        <button class="send-button" @click="$emit('send')">发送</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onUpdated, ref, nextTick } from 'vue'
  import { marked } from 'marked'
  
  const props = defineProps({
    messages: Array,
    userInput: String
  })
  
  const emit = defineEmits(['send', 'update:userInput'])
  
  const chatRef = ref(null)
  
  onUpdated(() => {
    nextTick(() => {
      chatRef.value.scrollTop = chatRef.value.scrollHeight
    })
  })
  
  const renderMarkdown = (text) => {
    return marked.parse(text || '')
  }
  </script>
  
  <style scoped>
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 1rem;
    color: white;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 1rem;
  }
  
  .message {
    margin-bottom: 1rem;
  }
  
  .message.user {
    text-align: right;
  }
  
  .markdown {
    text-align: left;
    background-color: #1e1e1e;
    padding: 0.5rem;
    border-radius: 6px;
    white-space: pre-wrap;
  }
  
  .chat-input {
    display: flex;
    gap: 0.5rem;
  }
  
  .input {
    flex: 1;
    padding: 0.5rem;
    background: #2e2e2e;
    border: 1px solid #444;
    color: white;
    border-radius: 4px;
  }
  
  .send-button {
    background: #4a90e2;
    border: none;
    padding: 0.5rem 1rem;
    color: white;
    cursor: pointer;
    border-radius: 4px;
  }
  </style>
  