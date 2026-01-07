<template>
  <div class="modern-texture" :class="[`texture-${type}`, `size-${size}`]">
    <slot></slot>
  </div>
</template>

<script setup>
const props = defineProps({
  // 纹理类型: 'modern', 'gradient', 'subtle'
  type: {
    type: String,
    default: 'modern'
  },
  // 尺寸: 'sm', 'md', 'lg', 'full'
  size: {
    type: String,
    default: 'full'
  }
});
</script>

<style lang="scss" scoped>
.modern-texture {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  
  &.size-sm {
    width: 100px;
    height: 100px;
  }
  
  &.size-md {
    width: 200px;
    height: 200px;
  }
  
  &.size-lg {
    width: 400px;
    height: 400px;
  }
  
  &.size-full {
    width: 100%;
    height: 100%;
  }
  
  // 现代风格
  &.texture-brushed,
  &.texture-modern {
    background: linear-gradient(135deg, var(--dark-surface) 0%, #0F172A 100%);
    box-shadow: 
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  // 渐变风格
  &.texture-diamond,
  &.texture-gradient {
    background: linear-gradient(135deg, var(--industrial-blue) 0%, #1E293B 100%);
    box-shadow: 
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  // 简约风格
  &.texture-perforated,
  &.texture-subtle {
    background: linear-gradient(135deg, var(--dark-surface) 0%, #0F172A 100%);
    box-shadow: 
      0 1px 3px 0 rgba(0, 0, 0, 0.1),
      0 1px 2px 0 rgba(0, 0, 0, 0.06);
  }
  
  // 碳纤维纹理（简化版）
  &.texture-carbon {
    background: var(--dark-surface);
    box-shadow: 
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
}
</style>