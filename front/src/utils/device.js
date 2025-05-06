/**
 * 检测当前设备类型的工具函数
 */

// 移动设备检测
export const isMobile = () => {
  return window.innerWidth < 768
}

// 平板设备检测
export const isTablet = () => {
  return window.innerWidth >= 768 && window.innerWidth < 992
}

// 桌面设备检测
export const isDesktop = () => {
  return window.innerWidth >= 992
}

// 创建响应式设备检测
export const useDeviceDetection = () => {
  const state = {
    isMobile: isMobile(),
    isTablet: isTablet(),
    isDesktop: isDesktop()
  }

  const updateDeviceState = () => {
    state.isMobile = isMobile()
    state.isTablet = isTablet()
    state.isDesktop = isDesktop()
  }

  // 添加窗口大小变化监听
  window.addEventListener('resize', updateDeviceState)

  return {
    ...state,
    updateDeviceState
  }
}

export default {
  isMobile,
  isTablet,
  isDesktop,
  useDeviceDetection
}
