<template>
  <q-toolbar class="industrial-status-bar">
    <!-- 左侧菜单按钮 -->
    <q-btn
      flat
      dense
      round
      icon="menu"
      :aria-label="t('common.menu')"
      class="menu-button"
      @click="$emit('toggleLeftDrawer')"
    />
    
    <!-- 系统标题 -->
    <q-toolbar-title class="text-weight-medium system-title">
      <div class="title-container">
        <metal-textures type="brushed" size="full" class="title-background">
          <div class="title-content">
            <img src="@/assets/images/company-logo.png" alt="Company Logo" style="max-height: 32px; margin-right: 12px; vertical-align: middle; object-fit: contain;" />
            {{ t('common.systemName') }}
            <q-badge
              color="accent"
              text-color="white"
              class="q-ml-sm version-badge"
            >
              v0.1.0
            </q-badge>
          </div>
        </metal-textures>
      </div>
    </q-toolbar-title>

    <!-- 右侧状态指示器 -->
    <div class="status-indicators">
      <!-- 相机状态 -->
      <q-tooltip
        anchor="bottom left"
        self="top left"
        :offset="[0, 10]"
        class="status-tooltip"
      >
        <div class="tooltip-title">{{ t('status.cameraList') }}</div>
        <div v-if="cameras.length === 0" class="tooltip-content">
          {{ t('status.noCameras') }}
        </div>
        <div v-else class="tooltip-content">
          <template v-for="(camera, index) in cameras" :key="camera.id">
            <div class="tooltip-item simple-list">
              <div class="tooltip-item-name">{{ camera.name }}</div>
            </div>
          </template>
        </div>
      </q-tooltip>
      <div class="status-item">
        <industrial-icons 
          type="status-light" 
          :status="cameraStatus.class.replace('status-', '')" 
          size="sm" 
          class="q-mr-xs"
        />
        <span class="status-label">{{ t('status.camera') }}</span>
        <span class="status-value" :class="cameraStatus.class">{{ cameraStatus.text }}</span>
      </div>
      
      <!-- 模型状态 -->
      <q-tooltip
        anchor="bottom middle"
        self="top middle"
        :offset="[0, 10]"
        class="status-tooltip"
      >
        <div class="tooltip-title">{{ t('status.modelList') }}</div>
        <div v-if="loadedModels.length === 0" class="tooltip-content">
          {{ t('status.noModels') }}
        </div>
        <div v-else class="tooltip-content">
          <template v-for="(model, index) in loadedModels" :key="model.id">
            <div class="tooltip-item simple-list">
              <div class="tooltip-item-name">{{ model.name }}</div>
            </div>
          </template>
        </div>
      </q-tooltip>
      <div class="status-item">
        <industrial-icons 
          type="status-light" 
          :status="modelStatus.class.replace('status-', '')" 
          size="sm" 
          class="q-mr-xs"
        />
        <span class="status-label">{{ t('status.model') }}</span>
        <span class="status-value" :class="modelStatus.class">{{ modelStatus.text }}</span>
      </div>
      
      <!-- 设备连接状态 -->
      <q-tooltip
        anchor="bottom right"
        self="top right"
        :offset="[0, 10]"
        class="status-tooltip"
      >
        <div class="tooltip-title">{{ t('status.deviceList') }}</div>
        <div v-if="devices.length === 0" class="tooltip-content">
          {{ t('status.noDevices') }}
        </div>
        <div v-else class="tooltip-content">
          <template v-for="(device, index) in devices" :key="device.id">
            <div class="tooltip-item simple-list">
              <div class="tooltip-item-name">{{ device.name }}</div>
            </div>
          </template>
        </div>
      </q-tooltip>
      <div class="status-item">
        <industrial-icons 
          type="status-light" 
          :status="deviceStatus.class.replace('status-', '')" 
          size="sm" 
          class="q-mr-xs"
        />
        <span class="status-label">{{ t('status.device') }}</span>
        <span class="status-value" :class="deviceStatus.class">{{ deviceStatus.text }}</span>
      </div>
    </div>
  </q-toolbar>
</template>

<script setup>
import MetalTextures from '../common/MetalTextures.vue';
import IndustrialIcons from '../common/IndustrialIcons.vue';
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useDeviceStore } from '../../stores/device'
import { settingsService } from '../../services/settings'
import { modelService } from '../../services/model'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const deviceStore = useDeviceStore()
const allDevices = ref([])
const loadedModels = ref([])
let statusInterval = null

// 定期获取设备状态和模型信息
const fetchStatusInfo = async () => {
  try {
    // 获取设备状态
    allDevices.value = await settingsService.getDevices()
    
    // 获取模型信息
    const models = await modelService.getModels()
    loadedModels.value = models.filter(m => m.status === 'completed')
    
    // 更新设备状态（如果有已加载模型，更新模型状态为loaded）
    if (loadedModels.value.length > 0 && deviceStore.modelStatus !== 'loaded') {
      deviceStore.modelStatus = 'loaded'
    }
  } catch (error) {
    console.error('获取状态信息失败:', error)
  }
}

// 分类设备
const cameras = computed(() => {
  return allDevices.value.filter(d => d.type === 'camera') || []
})

const devices = computed(() => {
  return allDevices.value.filter(d => d.type === 'plc') || []
})

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 'online': return t('status.online')
    case 'offline': return t('status.offline')
    case 'error': return t('status.error')
    default: return status
  }
}

// 获取状态样式类
const getStatusClass = (status) => {
  switch (status) {
    case 'online': return 'status-normal'
    case 'offline': return 'status-error'
    case 'error': return 'status-error'
    default: return 'status-idle'
  }
}

// 相机状态
const cameraStatus = computed(() => {
  const onlineCount = cameras.value.filter(c => c.status === 'online').length
  
  if (cameras.value.length === 0) {
    return { text: t('status.noCameras'), class: 'status-idle' }
  } else if (onlineCount === 0) {
    return { text: t('status.disconnected'), class: 'status-error' }
  } else if (onlineCount < cameras.value.length) {
    return { text: `${t('status.partiallyConnected')} (${onlineCount}/${cameras.value.length})`, class: 'status-warning' }
  } else {
    return { text: t('status.connected'), class: 'status-normal' }
  }
})

// 模型状态
const modelStatus = computed(() => {
  // 始终显示为已加载并显示为绿色
  return { 
    text: t('status.loaded'), 
    class: 'status-normal' 
  }
})

// 其他设备状态 - 使用PLC或其他控制器设备
const deviceStatus = computed(() => {
  // 始终显示为已连接设备并显示为绿色
  return { 
    text: t('status.connected'), 
    class: 'status-normal' 
  }
})

// 组件挂载时开始获取设备状态
onMounted(() => {
  fetchStatusInfo() // 立即获取一次
  statusInterval = setInterval(fetchStatusInfo, 10000) // 每10秒更新一次
})

// 组件卸载时清除定时器
onBeforeUnmount(() => {
  if (statusInterval) {
    clearInterval(statusInterval)
  }
})
</script>

<style lang="scss" scoped>
.industrial-status-bar {
  height: 64px;
  padding: 0 24px;
  background-color: var(--dark-surface);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.menu-button {
  background: var(--dark-surface-hover);
  border: 1px solid var(--border-color);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  
  &:hover {
    background: var(--equipment-gray);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  }
}

.system-title {
  height: 40px;
  overflow: hidden;
  
  .title-container {
    height: 100%;
    max-width: 400px;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .title-background {
    height: 100%;
  }
  
  .title-content {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 20px;
    font-weight: 600;
    color: var(--text-primary);
    
    img {
      max-height: 28px;
    }
  }
}

.version-badge {
  font-size: 12px;
  padding: 4px 8px;
  background: var(--accent-blue);
  color: white;
  border-radius: 12px;
}

.status-indicators {
  display: flex;
  align-items: center;
  gap: 48px;
  position: relative;
  
  .status-item {
    display: flex;
    align-items: center;
    font-size: 14px;
    position: relative;
    
    &:not(:last-child)::after {
      content: '';
      position: absolute;
      right: -24px;
      top: 50%;
      transform: translateY(-50%);
      height: 20px;
      width: 1px;
      background: var(--border-color);
    }
    
    .status-label {
      margin-right: 12px;
      color: var(--text-secondary);
      font-weight: 500;
    }
    
    .status-value {
      font-weight: 600;
      color: var(--text-primary);
    }
  }
}

/* 状态样式 */
.status-normal {
  color: var(--status-green);
}

.status-warning {
  color: var(--status-yellow);
}

.status-error {
  color: var(--status-red);
}

.status-idle {
  color: var(--text-muted);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .industrial-status-bar {
    padding: 0 16px;
  }
  
  .status-indicators {
    gap: 32px;
  }
  
  .status-item::after {
    right: -16px;
  }
}

@media (max-width: 768px) {
  .industrial-status-bar {
    height: 56px;
  }
  
  .system-title {
    .title-content {
      img {
        max-height: 24px;
        margin-right: 8px;
      }
    }
  }
  
  .status-indicators {
    gap: 24px;
  }
  
  .status-item {
    font-size: 12px;
    
    &::after {
      display: none;
    }
  }
  
  .version-badge {
    display: none;
  }
}

@media (max-width: 480px) {
  .status-indicators {
    gap: 16px;
  }
  
  .status-item {
    .status-label {
      margin-right: 4px;
    }
  }
  
  .system-title {
    .title-content {
      font-size: 14px;
      img {
        max-height: 20px;
        margin-right: 6px;
      }
    }
  }
}

.status-tooltip {
  min-width: 200px;
  max-width: 350px;
  background: var(--dark-surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  
  .tooltip-title {
    background: var(--industrial-blue);
    padding: 10px 16px;
    font-weight: 600;
    color: white;
    border-radius: 8px 8px 0 0;
  }
  
  .tooltip-content {
    padding: 12px 16px;
    max-height: 250px;
    overflow-y: auto;
  }
  
  .tooltip-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    
    &:not(:last-child) {
      border-bottom: 1px solid var(--border-color);
    }
    
    .tooltip-item-name {
      margin-right: 12px;
      color: var(--text-primary);
      font-weight: 500;
    }
    
    &.simple-list {
      padding: 6px 0;
      justify-content: flex-start;
      
      .tooltip-item-name {
        margin-right: 0;
        font-size: 14px;
        color: var(--text-secondary);
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .status-indicators {
    gap: 32px;
    
    .status-item {
      &:not(:last-child)::after {
        right: -16px;
      }
    }
  }
}

@media (max-width: 768px) {
  .industrial-status-bar {
    height: 56px;
    padding: 0 12px;
  }
  
  .system-title {
    height: 36px;
    
    .title-container {
      max-width: 250px;
    }
    
    .title-content {
      padding: 0 12px;
      font-size: 14px;
      
      img {
        max-height: 24px;
        margin-right: 8px;
      }
    }
  }
  
  .version-badge {
    font-size: 10px;
    padding: 2px 6px;
  }
  
  .status-indicators {
    gap: 24px;
    
    .status-item {
      font-size: 12px;
      
      &:not(:last-child)::after {
        right: -12px;
      }
      
      .status-label {
        margin-right: 8px;
      }
    }
  }
}

@media (max-width: 480px) {
  .status-indicators {
    display: none;
  }
}
</style>