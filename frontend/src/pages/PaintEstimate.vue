<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const room_id = ref(1)
const color_code = ref('')
const out = ref(null)
const err = ref('')
const preset_colors = ['N001', 'N002-象牙白', 'R118-珊瑚红', 'B205-雾霾蓝', 'G330-灰豆绿']
onMounted(async () => {
  const s = await getJSON('/api/settings')
  color_code.value = s.default_color_code || ''
})
const run = async (persist) => {
  err.value = ''; out.value = null
  try {
    out.value = await postJSON('/api/estimate', { room_id: room_id.value, color_code: color_code.value || null, persist })
  } catch (e) { err.value = e.message }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<label>色号批次
  <input v-model="color_code" list="preset-colors" placeholder="默认色号" />
  <datalist id="preset-colors">
    <option v-for="c in preset_colors" :key="c" :value="c" />
  </datalist>
</label>
<button @click="run(false)">试算（不落库）</button>
<button @click="run(true)">估算并记录</button>
<p v-if="err" class="err">{{ err }}</p>
<p v-if="out">色号 <b>{{ out.color_code }}</b> · 净 {{ out.net_m2 }} m² · {{ out.liters }} 升 · 涂布率 {{ out.coverage }} · {{ out.coats }} 遍
  <span v-if="out.run_id">（记录 #{{ out.run_id }}）</span><span v-else>（未落库）</span></p>
</div></template>
