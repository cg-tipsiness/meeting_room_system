/**
 * 移动端优化工具类
 */

// 设置适当的viewport
export const setupViewport = () => {
  const viewport = document.querySelector('meta[name="viewport"]')
  const viewportContent =
    'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'

  if (viewport) {
    viewport.setAttribute('content', viewportContent)
  } else {
    const meta = document.createElement('meta')
    meta.name = 'viewport'
    meta.content = viewportContent
    document.head.appendChild(meta)
  }
}

// 禁用双击放大
export const disableDoubleTapZoom = () => {
  let lastTouchEnd = 0
  document.addEventListener(
    'touchend',
    (event) => {
      const now = Date.now()
      if (now - lastTouchEnd < 300) {
        event.preventDefault()
      }
      lastTouchEnd = now
    },
    { passive: false }
  )
}

// 移除移动端点击高亮
export const removeHighlight = () => {
  const style = document.createElement('style')
  style.innerHTML = `
    * {
      -webkit-tap-highlight-color: transparent;
      -webkit-touch-callout: none;
      touch-action: manipulation;
    }
  `
  document.head.appendChild(style)
}

// 禁用长按菜单
export const disableLongPressMenu = () => {
  document.addEventListener('contextmenu', (event) => {
    if (event.cancelable) {
      event.preventDefault()
    }
  })
}

// 修复iOS输入框问题
export const fixIOSInputs = () => {
  const style = document.createElement('style')
  style.innerHTML = `
    input, select, textarea {
      font-size: 16px !important; /* 防止iOS缩放 */
    }
  `
  document.head.appendChild(style)
}

// 检测移动设备
export const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  )
}

// 移动端完全优化
export const optimizeMobile = () => {
  if (isMobile()) {
    setupViewport()
    disableDoubleTapZoom()
    removeHighlight()
    disableLongPressMenu()
    fixIOSInputs()
  }
}

export default {
  setupViewport,
  disableDoubleTapZoom,
  removeHighlight,
  disableLongPressMenu,
  fixIOSInputs,
  isMobile,
  optimizeMobile
}
