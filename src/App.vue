<template>
  <q-layout view="hHh lpR fFf" class="industrial-app">
    <!-- UI切换按钮 -->
    <div class="ui-switch-container">
      <q-btn
        flat
        round
        icon="swap_horiz"
        size="lg"
        color="accent-blue"
        :text-color="isLegacyUI ? 'white' : 'white'"
        @click="toggleUI"
        class="ui-switch-btn"
        :title="isLegacyUI ? t('common.newUI') : t('common.legacyUI')"
      >
        <q-tooltip position="left">
          {{ isLegacyUI ? t('common.newUI') : t('common.legacyUI') }}
        </q-tooltip>
      </q-btn>
    </div>

    <!-- 全局紧急停止按钮 -->
    <div class="emergency-stop-container">
      <industrial-icons type="industrial-button" size="lg" :active="false" @click="confirmEmergencyStop" class="emergency-stop-btn">
        <q-icon name="power_settings_new" color="negative" size="32px" />
      </industrial-icons>
    </div>

    <!-- 顶部状态栏 -->
    <q-header elevated class="bg-dark-page header-container">
      <metal-textures type="brushed" size="full" class="header-texture">
        <status-bar />
      </metal-textures>
    </q-header>

    <!-- 左侧导航抽屉 -->
    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      :width="240"
      :breakpoint="700"
      class="industrial-drawer bg-dark"
    >
      <metal-textures type="carbon" size="full" class="drawer-texture">
        <q-scroll-area class="fit">
          <div class="drawer-header">
            <div class="system-logo">
              <img src="@/assets/images/company-logo.png" alt="Company Logo" style="max-width: 50px; max-height: 50px; object-fit: contain;" />
            </div>
            <div class="system-title">{{ t('common.systemName') }}</div>
          </div>
          
          <navigation-menu />
        </q-scroll-area>
      </metal-textures>
    </q-drawer>

    <!-- 主内容区域 -->
    <q-page-container class="page-container">
      <metal-textures type="perforated" size="full" class="page-texture">
        <router-view />
      </metal-textures>
    </q-page-container>

    <!-- 全局告警面板 -->
    <alarm-panel v-if="hasActiveAlarms" :level="currentAlarmLevel" />
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'
import StatusBar from './components/layout/StatusBar.vue'
import NavigationMenu from './components/layout/NavigationMenu.vue'
import AlarmPanel from './components/common/AlarmPanel.vue'
import MetalTextures from './components/common/MetalTextures.vue'
import IndustrialIcons from './components/common/IndustrialIcons.vue'
import { useAlarmStore } from './stores/alarm'

// 处理加载指示器
onMounted(() => {
  const loadingIndicator = document.getElementById('loading-indicator')
  if (loadingIndicator) {
    loadingIndicator.style.opacity = '0'
    setTimeout(() => {
      loadingIndicator.style.display = 'none'
    }, 500)
  }
  
  // 初始化UI状态
  const savedUI = localStorage.getItem('uiVersion')
  if (savedUI) {
    isLegacyUI.value = savedUI === 'legacy'
    updateUIVersion()
  }
})

const { t } = useI18n()
const $q = useQuasar()
const leftDrawerOpen = ref(true)
const alarmStore = useAlarmStore()
const isLegacyUI = ref(false)

// 切换UI版本
const toggleUI = () => {
  isLegacyUI.value = !isLegacyUI.value
  updateUIVersion()
  localStorage.setItem('uiVersion', isLegacyUI.value ? 'legacy' : 'modern')
}

// 更新UI版本样式
const updateUIVersion = () => {
  if (isLegacyUI.value) {
    document.documentElement.classList.add('legacy-ui')
  } else {
    document.documentElement.classList.remove('legacy-ui')
  }
}

// 计算属性：是否有活跃告警
const hasActiveAlarms = computed(() => alarmStore.activeAlarms.length > 0)

// 计算属性：当前最高告警等级
const currentAlarmLevel = computed(() => alarmStore.highestAlarmLevel)

// 紧急停止确认
function confirmEmergencyStop() {
  $q.dialog({
    title: t('emergencyStop.title'),
    message: t('emergencyStop.message'),
    color: 'negative',
    icon: 'warning',
    persistent: true,
    ok: {
      label: t('emergencyStop.confirm'),
      color: 'negative',
      flat: false,
      'no-caps': true
    },
    cancel: {
      label: t('common.cancel'),
      color: 'dark',
      textColor: 'white',
      flat: true,
      'no-caps': true
    }
  }).onOk(() => {
    // 执行紧急停止逻辑
    alarmStore.triggerEmergencyStop()
    $q.notify({
      type: 'negative',
      message: t('emergencyStop.executed'),
      icon: 'warning'
    })
  })
}
</script>

<style lang="scss">
.industrial-app {
  height: 100vh;
  background-color: var(--dark-page);
  display: flex;
  flex-direction: column;
}

.ui-switch-container {
  position: fixed;
  bottom: 130px;
  right: 30px;
  z-index: 9999;
  transition: all 0.3s ease;
  
  @media (max-width: 768px) {
    bottom: 110px;
    right: 20px;
  }
}

.ui-switch-btn {
  width: 60px;
  height: 60px;
  border: 2px solid var(--accent-blue);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
  transition: all 0.3s ease;
  border-radius: 50%;
  background: linear-gradient(145deg, var(--accent-blue), var(--industrial-blue));
  
  &:hover {
    transform: scale(1.1);
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.8);
  }
  
  &:active {
    transform: scale(0.9);
  }
  
  @media (max-width: 768px) {
    width: 50px;
    height: 50px;
  }
}

.emergency-stop-container {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 9999;
  transition: all 0.3s ease;
  
  @media (max-width: 768px) {
    bottom: 20px;
    right: 20px;
  }
}

.emergency-stop-btn {
  width: 80px;
  height: 80px;
  border: 4px solid var(--status-red);
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
  transition: all 0.3s ease;
  border-radius: 50%;
  background: linear-gradient(145deg, #7F1D1D, #DC2626);
  
  &:hover {
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.8);
  }
  
  &:active {
    transform: scale(0.9);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: -8px;
    left: -8px;
    right: -8px;
    bottom: -8px;
    border: 2px dashed var(--status-red);
    border-radius: 50%;
    animation: rotate 8s linear infinite;
  }
  
  @media (max-width: 768px) {
    width: 60px;
    height: 60px;
    
    &::before {
      top: -6px;
      left: -6px;
      right: -6px;
      bottom: -6px;
    }
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.header-container {
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-texture {
  height: 64px;
}

.drawer-texture {
  height: 100%;
}

.drawer-header {
  display: flex;
  align-items: center;
  padding: 16px;
  height: 80px;
  border-bottom: 1px solid var(--border-color);
  
  .system-logo {
    margin-right: 12px;
    
    img {
      max-width: 40px;
      max-height: 40px;
    }
  }
  
  .system-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--accent-blue);
  }
}

.page-container {
  background-color: var(--dark-page);
  flex-grow: 1;
  overflow-y: scroll !important;
}

.page-texture {
  height: 100%;
  overflow-y: scroll !important;
}

.industrial-drawer {
  .q-item {
    min-height: 56px;
    border-radius: 8px;
    margin: 4px 8px;
    font-size: 16px;
    transition: all 0.2s ease;
    color: var(--text-primary);
    
    &:hover {
      background: var(--dark-surface-hover);
    }
    
    &.q-item--active {
      background: var(--industrial-blue-10);
      border-left: 4px solid var(--accent-blue);
      color: var(--accent-blue);
    }
    
    @media (max-width: 768px) {
      min-height: 48px;
      font-size: 14px;
    }
  }
}

/* 响应式布局 */
@media (max-width: 768px) {
  .q-header {
    padding-left: 8px;
    padding-right: 8px;
  }
  
  .q-drawer {
    width: 200px !important;
  }
  
  .drawer-header {
    height: 70px;
    padding: 12px;
    
    .system-title {
      font-size: 16px;
    }
  }
}
</style>