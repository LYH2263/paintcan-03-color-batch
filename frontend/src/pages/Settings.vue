<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const default_color = ref('')
const msg = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  default_color.value = s.value.default_color_code || ''
})
const save = async () => {
  msg.value = ''
  try {
    s.value = await putJSON('/api/settings', { default_color_code: default_color.value })
    default_color.value = s.value.default_color_code || ''
    msg.value = '已保存'
  } catch (e) { msg.value = e.message }
}
</script>
<template><div class="page"><h1>设置</h1>
<p>每升可刷 {{ s.coverage }} m² · 默认 {{ s.coats }} 遍</p>
<label>默认色号批次 <input v-model="default_color" /></label>
<button @click="save">保存默认色号</button>
<p class="err" v-if="msg">{{ msg }}</p>
<p class="hint">修改默认色号只影响之后的新测算，历史记录的色号与升数不变。</p>
</div></template>
