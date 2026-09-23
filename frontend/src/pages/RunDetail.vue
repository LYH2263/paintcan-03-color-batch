<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON } from '../api'
const route = useRoute()
const r = ref(null)
const load = async () => { r.value = await getJSON(`/api/history/${route.params.id}`) }
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="r"><h1>测算记录 #{{ r.id }}</h1>
<p>写入时色号 <b>{{ r.color_batch || '—' }}</b></p>
<p>写入时升数 <span class="hero-num">{{ r.liters ?? '—' }} L</span></p>
<p>净面积 {{ r.net_m2 ?? '—' }} m² · 涂布率 {{ r.coverage ?? '—' }} m²/L · {{ r.coats ?? '—' }} 遍</p>
<p>房间 {{ r.room_id ?? '—' }} · {{ r.created_at }}</p>
</div></template>
