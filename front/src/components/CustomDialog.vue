<template>
  <Transition name="dialog-fade">
    <div v-if="modelValue" class="dialog-container" @click.self="handleClose">
      <div class="dialog-wrapper" :class="{ 'dialog-center': center }">
        <div class="dialog-content" :style="{ width }">
          <div class="dialog-header">
            <h3 class="dialog-title">{{ title }}</h3>
            <button class="dialog-close" @click="handleClose">
              <i class="el-icon-close">×</i>
            </button>
          </div>
          <div class="dialog-body">
            <slot></slot>
          </div>
          <div class="dialog-footer">
            <slot name="footer">
              <el-button @click="handleCancel">{{ cancelText }}</el-button>
              <el-button
                type="primary"
                @click="handleConfirm"
                :loading="confirmLoading"
              >
                {{ confirmText }}
              </el-button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '提示'
  },
  width: {
    type: String,
    default: '420px'
  },
  center: {
    type: Boolean,
    default: true
  },
  confirmText: {
    type: String,
    default: '确定'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  confirmLoading: {
    type: Boolean,
    default: false
  },
  closeOnClickModal: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const handleClose = () => {
  if (props.closeOnClickModal) {
    emit('update:modelValue', false)
    emit('cancel')
  }
}

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('update:modelValue', false)
  emit('cancel')
}
</script>

<style lang="scss" scoped>
@import '@/assets/mobile.scss';

.dialog-container {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 2000;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  overflow: auto;
}

.dialog-wrapper {
  position: relative;
  margin: 15vh auto 50px;
  padding: 20px;

  &.dialog-center {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: calc(100% - 40px);
    margin: 0;
  }
}

.dialog-content {
  position: relative;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  margin: 0 auto;
  overflow: hidden;
}

.dialog-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .dialog-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin: 0;
    line-height: 1.5;
  }

  .dialog-close {
    border: none;
    background: transparent;
    font-size: 20px;
    color: #999;
    cursor: pointer;
    padding: 0;
    line-height: 1;
    transition: color 0.2s;

    &:hover {
      color: #666;
    }
  }
}

.dialog-body {
  padding: 20px;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.dialog-footer {
  padding: 10px 20px 16px;
  text-align: right;
  border-top: 1px solid #eee;

  .el-button + .el-button {
    margin-left: 12px;
  }
}

// 动画效果
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: all 0.3s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.dialog-fade-enter-to,
.dialog-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

// 移动端适配
@include responsive(mobile) {
  .dialog-content {
    width: 90% !important;
    max-width: 320px;
    margin: 0 auto;
  }

  .dialog-header {
    padding: 12px 15px;

    .dialog-title {
      font-size: 15px;
    }
  }

  .dialog-body {
    padding: 15px;
    font-size: 13px;
  }

  .dialog-footer {
    padding: 8px 15px 12px;
    display: flex;
    justify-content: flex-end;
    gap: 8px;

    .el-button {
      flex: 1;
      max-width: 120px;
      padding: 6px 15px;
      font-size: 13px;
    }
  }
}
</style>
