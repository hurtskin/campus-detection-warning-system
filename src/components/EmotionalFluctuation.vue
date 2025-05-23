<template>
  <div class="emotion-fluctuation-wrapper">
    <h1>情绪波动展示</h1>
    <canvas ref="emotionCanvas" width="400" height="200"></canvas>
  </div>
</template>

<script>
export default {
  mounted () {
    this.drawWave()
    setInterval(() => {
      this.drawWave()
    }, 1000)
  },
  methods: {
    drawWave () {
      const canvas = this.$refs.emotionCanvas
      const ctx = canvas.getContext('2d')
      const width = canvas.width
      const height = canvas.height
      // const numPoints = 50
      const amplitude = 30
      const frequency = 0.05
      const phase = Math.random() * 2 * Math.PI
      const color = `hsl(${Math.random() * 360}, 80%, 50%)`

      ctx.beginPath()
      ctx.moveTo(0, height / 2)
      for (let x = 0; x < width; x++) {
        const y = height / 2 + Math.sin(x * frequency + phase) * amplitude
        ctx.lineTo(x, y)
      }
      ctx.lineTo(width, height / 2)
      ctx.closePath()
      ctx.strokeStyle = color
      ctx.lineWidth = 3
      ctx.stroke()
    }
  }
}
</script>

<style scoped>
.emotion-fluctuation-wrapper {
  width: 100%;
  text-align: center;
  padding: 50px;
  background-color: #ccc;
}
</style>
