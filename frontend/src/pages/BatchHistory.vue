<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template><div class="page"><h1>估算记录</h1>
<table>
  <tr><th>编号</th><th>时间</th><th>房间</th><th>色号</th><th>升数</th><th></th></tr>
  <tr v-for="h in items" :key="h.id">
    <td>#{{ h.id }}</td>
    <td>{{ h.created_at }}</td>
    <td>{{ h.input?.room_id ?? '—' }}</td>
    <td>{{ h.result?.color_code ?? h.input?.color_code ?? '—' }}</td>
    <td>{{ h.result?.liters ?? '—' }} 升</td>
    <td><router-link :to="`/history/${h.id}`">打开</router-link></td>
  </tr>
</table>
</div></template>
