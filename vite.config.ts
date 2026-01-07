import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'
import type { UserConfig } from 'vite'
import { resolve } from 'path'
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue({
            template: { transformAssetUrls }
        }),
        quasar({
            sassVariables: resolve(__dirname, 'src/styles/quasar-variables.scss')
        })
    ],
    resolve: {
        alias: {
            '@': '/src'
        }
    },
    server: {
        port: 3000,
        open: true,
        host: '0.0.0.0', // 关键：监听所有网络接口，允许内网IP访问
        strictPort: false, // 端口被占用时自动换端口
        allowedHosts: true,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true
            }
        }
    },
    build: {
        target: 'es2015',
        chunkSizeWarningLimit: 2000,
        rollupOptions: {
            output: {
                manualChunks: {
                    'vendor': ['vue', 'vue-router', 'pinia', 'quasar'],
                    'echarts': ['echarts']
                }
            }
        }
    }
} as UserConfig)
