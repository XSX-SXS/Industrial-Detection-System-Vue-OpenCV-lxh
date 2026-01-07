<template>
  <div class="col-12 col-sm-6">
    <q-input 
      v-model="param.name" 
      dense 
      outlined 
      :label="t('cv.parameter.name')"
      :rules="[val => !!val || t('cv.parameter.nameRequired')]"
    />
  </div>
  <div class="col-12 col-sm-6">
    <q-select 
      v-model="param.type" 
      :options="paramTypeOptions" 
      dense 
      outlined 
      :label="t('cv.parameter.type')"
      :rules="[val => !!val || t('cv.parameter.typeRequired')]"
      emit-value
      map-options
      options-dense
    >
      <template v-slot:option="{ itemProps, opt }">
        <q-item v-bind="itemProps">
          <q-item-section avatar>
            <q-icon :name="opt.icon" />
          </q-item-section>
          <q-item-section>
            {{ opt.label }}
          </q-item-section>
        </q-item>
      </template>
    </q-select>
  </div>
  <div class="col-12">
    <q-input 
      v-model="param.description" 
      dense 
      outlined 
      :label="t('cv.parameter.description')"
    />
  </div>
  <div class="col-grow">
    <q-input 
      v-model="param.default" 
      dense 
      outlined 
      :label="t('cv.parameter.defaultValue')"
    />
  </div>
  <div class="col-auto">
    <q-checkbox v-model="param.required" :label="t('cv.parameter.required')" />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  param: {
    type: Object,
    required: true
  },
  paramTypeOptions: {
    type: Array,
    required: true
  }
})
</script>

<style lang="scss" scoped>
// 表单元素的现代工业风格
.q-input,
.q-select,
.q-checkbox {
  margin-bottom: 16px;
  
  .q-field__control {
    border-color: var(--border-color);
    background: var(--dark-surface);
    border-radius: 8px;
    
    &:hover {
      border-color: var(--accent-blue);
    }
    
    &--focused {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
  }
  
  .q-field__input {
    color: var(--text-primary);
    
    &::placeholder {
      color: var(--text-muted);
    }
  }
  
  .q-field__label {
    color: var(--text-secondary);
  }
}

.q-select {
  .q-field__control {
    &:after {
      color: var(--text-secondary);
    }
  }
}

.q-checkbox {
  .q-checkbox__label {
    color: var(--text-primary);
  }
  
  .q-checkbox__inner {
    border-color: var(--border-color);
    background: var(--dark-surface);
    
    &--checked {
      background: var(--accent-blue);
      border-color: var(--accent-blue);
    }
  }
}
</style>
