<template>
  <div class="industrial-icon" :class="[`icon-${type}`, `size-${size}`]">
    <!-- 状态指示灯 -->
    <template v-if="type === 'status-light'">
      <div class="status-light" :class="status">
        <div class="light-glow"></div>
      </div>
    </template>
    
    <!-- 仪表盘 -->
    <template v-else-if="type === 'gauge'">
      <div class="gauge-container">
        <svg viewBox="0 0 120 120" class="gauge">
          <path class="gauge-bg" d="M20,100 A 60,60 0 1,1 100,100" />
          <path class="gauge-fill" :style="{strokeDasharray: `${gaugeValue}, 188.5`}" d="M20,100 A 60,60 0 1,1 100,100" />
          <text x="60" y="80" class="gauge-value">{{ displayValue }}</text>
          <text x="60" y="95" class="gauge-label">{{ label }}</text>
        </svg>
      </div>
    </template>
    
    <!-- 工业按钮 -->
    <template v-else-if="type === 'industrial-button'">
      <div class="ind-button" :class="{active: active}" @click="$emit('click')">
        <div class="button-frame"></div>
        <div class="button-surface">
          <slot></slot>
        </div>
      </div>
    </template>
    
    <!-- 金属面板 -->
    <template v-else-if="type === 'metal-panel'">
      <div class="metal-panel">
        <div class="panel-frame">
          <slot></slot>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // 图标类型: 'status-light', 'gauge', 'industrial-button', 'metal-panel'
  type: {
    type: String,
    default: 'status-light'
  },
  // 尺寸: 'sm', 'md', 'lg'
  size: {
    type: String,
    default: 'md'
  },
  // 状态灯状态: 'normal', 'warning', 'error', 'inactive'
  status: {
    type: String,
    default: 'normal'
  },
  // 仪表盘值 (0-100)
  value: {
    type: Number,
    default: 0
  },
  // 仪表盘最大值
  max: {
    type: Number,
    default: 100
  },
  // 仪表盘标签
  label: {
    type: String,
    default: '%'
  },
  // 按钮是否激活
  active: {
    type: Boolean,
    default: false
  }
});

const gaugeValue = computed(() => {
  // 计算仪表盘填充值 (最大188.5)
  return (props.value / props.max) * 188.5;
});

const displayValue = computed(() => {
  // 显示值
  return Math.round(props.value);
});

defineEmits(['click']);
</script>

<style lang="scss" scoped>
.industrial-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  
  &.size-sm {
    width: 24px;
    height: 24px;
  }
  
  &.size-md {
    width: 48px;
    height: 48px;
  }
  
  &.size-lg {
    width: 80px;
    height: 80px;
  }
}

/* 状态指示灯样式 */
.status-light {
  position: relative;
  width: 80%;
  height: 80%;
  border-radius: 50%;
  background: var(--dark-surface);
  border: 2px solid var(--border-color);
  overflow: hidden;
  transition: all 0.3s ease;
  
  &.normal {
    background: linear-gradient(135deg, var(--status-green) 0%, #166534 100%);
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.6);
    
    .light-glow {
      background: radial-gradient(circle, var(--status-green) 0%, transparent 70%);
    }
  }
  
  &.warning {
    background: linear-gradient(135deg, var(--status-yellow) 0%, #92400E 100%);
    box-shadow: 0 0 20px rgba(234, 179, 8, 0.6);
    
    .light-glow {
      background: radial-gradient(circle, var(--status-yellow) 0%, transparent 70%);
    }
  }
  
  &.error {
    background: linear-gradient(135deg, var(--status-red) 0%, #991B1B 100%);
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
    
    .light-glow {
      background: radial-gradient(circle, var(--status-red) 0%, transparent 70%);
    }
  }
  
  &.inactive {
    background: linear-gradient(135deg, var(--border-color) 0%, #475569 100%);
    
    .light-glow {
      display: none;
    }
  }
  
  .light-glow {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    opacity: 0.5;
    animation: pulse 2s infinite;
  }
}

/* 仪表盘样式 */
.gauge-container {
  width: 100%;
  height: 100%;
}

.gauge {
  width: 100%;
  height: 100%;
  
  .gauge-bg {
    fill: none;
    stroke: var(--border-color);
    stroke-width: 12;
    stroke-linecap: round;
  }
  
  .gauge-fill {
    fill: none;
    stroke: var(--accent-blue);
    stroke-width: 12;
    stroke-linecap: round;
    transition: stroke-dasharray 0.5s ease;
  }
  
  .gauge-value {
    font-size: 24px;
    font-weight: bold;
    text-anchor: middle;
    fill: var(--text-primary);
  }
  
  .gauge-label {
    font-size: 14px;
    text-anchor: middle;
    fill: var(--text-secondary);
  }
}

/* 工业按钮样式 */
.ind-button {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
  user-select: none;
  
  .button-frame {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--dark-surface) 0%, var(--dark-page) 100%);
    border: 2px solid var(--border-color);
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  }
  
  .button-surface {
    position: absolute;
    top: 4px;
    left: 4px;
    right: 4px;
    bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--industrial-blue) 100%);
    border-radius: 6px;
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
  }
  
  &.active .button-surface {
    top: 6px;
    box-shadow: inset 0 4px 12px rgba(0,0,0,0.3);
    background: linear-gradient(135deg, var(--industrial-blue) 0%, var(--accent-blue) 100%);
  }
  
  &:hover .button-surface {
    background: linear-gradient(135deg, var(--accent-blue) 0%, #60A5FA 100%);
    box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
    transform: translateY(-1px);
  }
  
  &:active .button-surface {
    transform: translateY(1px);
  }
}

/* 金属面板样式 */
.metal-panel {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--dark-surface) 0%, var(--dark-page) 100%);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
  }
  
  .panel-frame {
    width: 100%;
    height: 100%;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

@keyframes pulse {
  0% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.2);
  }
  100% {
    opacity: 0.5;
    transform: scale(1);
  }
}
</style>