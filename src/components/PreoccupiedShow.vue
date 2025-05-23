<template>
  <div class="preoccupied-wrapper">
    <h1>心事重重展示</h1>
    <div class="preoccupied-content" :style="preoccupiedStyle">
      <p>{{ preoccupiedText }}</p >
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      preoccupiedStyle: {
        backgroundColor: '#333',
        color: 'white',
        padding: '50px',
        textAlign: 'left',
        opacity: 0.8
      },
      preoccupiedText: '那些藏在心底的事儿，总是挥之不去...'
    }
  }
}
</script>

<style scoped>
.preoccupied-wrapper {
  width: 100%;
}

.preoccupied-content {
  animation: fade-in-out 5s infinite alternate;
}

@keyframes fade-in-out {
  from {
    opacity: 0.6;
  }
  to {
    opacity: 0.8;
  }
}
</style>
