<template>
    <div class="history-panel">
      <h3>历史记录</h3>
      <ul>
        <li
          v-for="(item, idx) in history"
          :key="idx"
          @click="$emit('select', item)"
        >
          {{ item.query.slice(0, 20) }}...
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    history: Array
  })
  
  defineEmits(['select'])
  </script>
  
  <style scoped>
  .history-panel {
    background: #1a1a1a;
    color: white;
    width: 250px;
    padding: 1rem;
    height: 100vh;
    overflow-y: auto;
    border-right: 1px solid #333;
  }
  
  .history-panel h3 {
    margin-bottom: 1rem;
  }
  
  .history-panel li {
    list-style: none;
    margin-bottom: 0.5rem;
    cursor: pointer;
  }
  
  .history-panel li:hover {
    color: #4a90e2;
  }
  </style>
  