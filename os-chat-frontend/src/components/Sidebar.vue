<template>
    <aside class="sidebar">
      <h2>历史问答</h2>
      <ul>
        <li
          v-for="item in history"
          :key="item.id"
          @click="$emit('select', item)"
        >
          {{ item.question }}
        </li>
      </ul>
    </aside>
  </template>
  
  <script setup>
  defineProps({ history: Array })
  </script>
  
  <style scoped>
  .sidebar {
    width: 280px;
    background: #1f1f1f;
    padding: 1rem;
    border-right: 1px solid #333;
    color: white;
    overflow-y: auto;
  }
  
  .sidebar h2 {
    margin-bottom: 1rem;
    font-size: 1.1rem;
    color: #bbb;
  }
  
  .sidebar li {
    padding: 0.5rem;
    cursor: pointer;
    border-radius: 4px;
  }
  
  .sidebar li:hover {
    background-color: #333;
  }
  </style>
  