<script setup>
defineProps({
  connected: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <header class="topbar">
    <div class="brand">
      <div class="brand-mark">RM</div>

      <div>
        <strong>Ruta Médica</strong>
        <span>Control de tráfico inteligente</span>
      </div>
    </div>

    <div class="header-right">
      <span class="scope-pill">
        <span class="pulse-dot"></span>
        Delimitación · Lima Metropolitana
      </span>

      <span
        class="connection"
        :class="connected ? 'online' : 'offline'"
      >
        <span class="status-dot"></span>

        {{ connected
          ? 'Conectado'
          : 'Desconectado'
        }}
      </span>
    </div>
  </header>
</template>
