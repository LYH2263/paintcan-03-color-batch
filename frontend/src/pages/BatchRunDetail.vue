<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON } from '../api'
const route = useRoute()
const run = ref(null)
const load = async () => { run.value = await getJSON(`/api/history/${route.params.id}`) }
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="run"><h1>记录 #{{ run.id }}</h1>
<p>时间 {{ run.created_at }}</p>
<p>房间ID {{ run.input?.room_id }}</p>
<table>
  <tr><th>写入时色号</th><th>升数</th><th>净面积</th><th>涂布率</th><th>遍数</th></tr>
  <tr>
    <td><b>{{ run.result?.color_code ?? run.input?.color_code }}</b></td>
    <td>{{ run.result?.liters }} 升</td>
    <td>{{ run.result?.net_m2 }} m²</td>
    <td>{{ run.result?.coverage }} m²/L</td>
    <td>{{ run.result?.coats }}</td>
  </tr>
</table>
<p><router-link to="/history">返回列表</router-link></p>
</div></template>
