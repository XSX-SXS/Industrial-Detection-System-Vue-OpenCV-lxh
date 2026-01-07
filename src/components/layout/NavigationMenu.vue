<template>
  <q-list>
    <q-item
      v-for="route in routes"
      :key="route.path"
      :to="route.path"
      clickable
      v-ripple
      exact
      active-class="q-item--active"
    >
      <q-item-section avatar>
        <q-icon :name="route.meta.icon" size="24px" />
      </q-item-section>
      <q-item-section>
        {{ route.meta.title }}
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 获取路由配置中的主要导航项
const routes = computed(() => {
  return router.options.routes.filter(route => {
    // 过滤掉重定向和404页面
    return route.meta && route.meta.icon && route.name !== 'NotFound'
  })
})
</script>

<style lang="scss" scoped>
.q-list {
  padding: 8px;
}

.q-item {
  min-height: 56px;
  border-radius: 8px;
  margin-bottom: 4px;
  padding: 8px 12px;
  transition: all 0.3s ease;
  color: var(--text-primary);
  
  &:hover {
    background: var(--dark-surface-hover);
  }
  
  &.q-item--active {
    background: var(--industrial-blue-10);
    border-left: 4px solid var(--accent-blue);
    color: var(--accent-blue);
    
    .q-icon {
      color: var(--accent-blue);
    }
  }
  
  .q-item-section {
    .q-icon {
      color: var(--text-secondary);
      transition: color 0.3s ease;
    }
  }
}
</style>