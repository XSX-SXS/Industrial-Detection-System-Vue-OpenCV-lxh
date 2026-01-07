<template>
  <div class="report-center-container">
    <div class="page-header">
      <h1>{{ $t('reportCenter.title') }}</h1>
      <div class="header-actions">
        <el-button
          type="primary"
          size="small"
          @click="exportReport"
          class="export-btn"
          :icon="Download"
        >
          {{ $t('reportCenter.export') }}
        </el-button>
        <el-button
          type="success"
          size="small"
          @click="printReport"
          class="print-btn"
          :icon="Printer"
        >
          {{ $t('reportCenter.print') }}
        </el-button>
      </div>
    </div>

    <!-- 筛选控件区域 -->
    <div class="filter-section">
      <!-- 日期范围选择 -->
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        format="YYYY-MM-DD"
        value-format="YYYY-MM-DD"
        class="date-picker"
      ></el-date-picker>

      <!-- 产品型号选择 -->
      <el-select v-model="selectedProduct" placeholder="选择产品型号" class="filter-select">
        <el-option label="YT15-160408" value="YT15-160408"></el-option>
        <el-option label="YT15-120404" value="YT15-120404"></el-option>
        <el-option label="YG8-160408" value="YG8-160408"></el-option>
        <el-option label="YW2-160408" value="YW2-160408"></el-option>
      </el-select>

      <!-- 班组选择 -->
      <el-select v-model="selectedTeam" placeholder="选择班组" class="filter-select">
        <el-option label="全部" value="all"></el-option>
        <el-option label="甲班" value="甲班"></el-option>
        <el-option label="乙班" value="乙班"></el-option>
        <el-option label="丙班" value="丙班"></el-option>
      </el-select>

      <!-- 产线选择 -->
      <el-select v-model="selectedLine" placeholder="选择产线" class="filter-select">
        <el-option label="全部" value="all"></el-option>
        <el-option label="1号线（PVD）" value="1号线（PVD）"></el-option>
        <el-option label="2号线（CVD）" value="2号线（CVD）"></el-option>
        <el-option label="3号线（混合涂层）" value="3号线（混合涂层）"></el-option>
      </el-select>

      <!-- 设备类型选择 -->
      <el-select v-model="selectedEquipment" placeholder="选择设备类型" class="filter-select">
        <el-option label="全部" value="all"></el-option>
        <el-option label="PVD物理涂层设备" value="PVD物理涂层设备"></el-option>
        <el-option label="CVD化学涂层设备" value="CVD化学涂层设备"></el-option>
        <el-option label="检测包装设备" value="检测包装设备"></el-option>
      </el-select>

      <!-- 筛选按钮 -->
      <el-button type="primary" size="small" @click="applyFilters" class="filter-btn">
        应用筛选
      </el-button>
      <el-button size="small" @click="resetFilters" class="filter-btn">
        重置
      </el-button>
    </div>

    <el-tabs v-model="activeTab" type="card" class="mb-md">
      <!-- 当班数据分析报表 -->
      <el-tab-pane label="当班数据分析" name="shift">
        <div class="row gutter-sm mb-md">
          <div class="col-xs-12 col-sm-6 col-md-3">
            <el-card class="metric-card">
              <div class="el-card__body">
                <div class="text-subtitle1 mb-xs">FPY（一次通过率）</div>
                <div class="row items-center">
                  <div class="text-h6">衡量产品质量水平</div>
                  <span class="success-tag ml-sm">{{ shiftData.fpy }}%</span>
                </div>
                <div class="text-caption">当前值：<span class="text-positive">{{ shiftData.fpy }}%</span></div>
              </div>
            </el-card>
          </div>

          <div class="col-xs-12 col-sm-6 col-md-3">
            <el-card class="metric-card">
              <div class="el-card__body">
                <div class="text-subtitle1 mb-xs">Cpk（工序能力指数）</div>
                <div class="row items-center">
                  <div class="text-h6">衡量生产控制水平</div>
                  <span class="warning-tag ml-sm">{{ shiftData.cpk }}</span>
                </div>
                <div class="text-caption">当前值：<span class="text-warning">{{ shiftData.cpk }}</span></div>
              </div>
            </el-card>
          </div>
        </div>

        <div class="row gutter-sm">
          <!-- 图表1：当班FPY可视化图 -->
          <div class="col-xs-12 col-sm-12 col-md-6">
            <el-card class="chart-card">
              <div class="el-card__body">
                <div class="text-subtitle1 mb-xs">当班FPY（一次通过率）可视化图</div>
                <div class="text-center mb-md">
                  <div class="text-h2 text-positive">{{ shiftData.fpy }}%</div>
                  <div class="text-caption">当班总FPY</div>
                </div>
                <canvas ref="fpyChartCanvas" class="chart-canvas"></canvas>
              </div>
            </el-card>
          </div>

          <!-- 图表2：当班Cpk趋势图 -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">当班Cpk（工序能力指数）趋势图</div>
                  <canvas ref="cpkChartCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>
          </div>

          <div class="row gutter-sm">
            <!-- 图表3：产品尺寸分布直方图 -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">产品尺寸分布直方图</div>
                  <canvas ref="histogramChartCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>

            <!-- 图表4：X-MR控制图 -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">X-MR控制图（均值-移动极差控制图）</div>
                  <canvas ref="xmrChartCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>
          </div>

          <div class="row gutter-sm">
            <!-- 图表5：缺陷帕累托图 -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">缺陷帕累托图</div>
                  <canvas ref="paretoChartCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>

            <!-- 图表6：当班计数型控制图（np图） -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">当班计数型控制图（np图）</div>
                  <canvas ref="npControlChartCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>

      <!-- 周/月度数据统计报表 -->
      <el-tab-pane name="period" label="周/月度统计">
        <div class="row gutter-sm mb-md">
          <div class="col-xs-12 col-sm-6 col-md-3">
            <el-card class="metric-card">
              <div class="el-card__body">
                <div class="text-subtitle1 mb-xs">总体 FPY</div>
                <div class="row items-center">
                  <div class="text-h6">总一次通过率</div>
                  <span class="success-tag ml-sm">{{ periodData.overall.fpy }}%</span>
                </div>
                <div class="text-caption">当前值：<span class="text-positive">{{ periodData.overall.fpy }}%</span></div>
              </div>
            </el-card>
          </div>

          <div class="col-xs-12 col-sm-6 col-md-3">
            <el-card class="metric-card">
              <div class="el-card__body">
                <div class="text-subtitle1 mb-xs">总体 Cpk</div>
                <div class="row items-center">
                  <div class="text-h6">总工序能力指数</div>
                  <span class="warning-tag ml-sm">{{ periodData.overall.cpk }}</span>
                </div>
                <div class="text-caption">当前值：<span class="text-warning">{{ periodData.overall.cpk }}</span></div>
              </div>
            </el-card>
          </div>
        </div>

        <div class="row gutter-sm">
          <!-- 图表7：周/月度FPY对比图（总 + 班组级） -->
          <div class="col-xs-12 col-sm-12 col-md-6">
            <el-card class="chart-card">
              <div class="el-card__body">
                <div class="text-subtitle1 mb-xs">周/月度FPY对比图</div>
                <canvas ref="fpyComparisonCanvas" class="chart-canvas"></canvas>
              </div>
            </el-card>
          </div>

          <!-- 图表8：周/月度Cpk雷达图（总 + 班组级） -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">周/月度Cpk雷达图</div>
                  <canvas ref="cpkComparisonCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>
          </div>

          <div class="row gutter-sm">
            <!-- 图表9：周/月度产品尺寸分布直方图 -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">周/月度产品尺寸分布直方图</div>
                  <canvas ref="periodHistogramCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>

          <!-- 图表10：周/月度缺陷帕累托图 -->
            <div class="col-xs-12 col-sm-12 col-md-6">
              <el-card class="chart-card">
                <div class="el-card__body">
                  <div class="text-subtitle1 mb-xs">周/月度缺陷帕累托图</div>
                  <div class="chart-controls mb-sm">
                    <el-select v-model="selectedParetoView" placeholder="选择视图" class="w-full">
                      <el-option label="总缺陷" value="total"></el-option>
                      <el-option label="甲班" value="team_甲班"></el-option>
                      <el-option label="乙班" value="team_乙班"></el-option>
                      <el-option label="丙班" value="team_丙班"></el-option>
                      <el-option label="1号线（PVD）" value="line_1号线（PVD）"></el-option>
                      <el-option label="2号线（CVD）" value="line_2号线（CVD）"></el-option>
                      <el-option label="3号线（混合涂层）" value="line_3号线（混合涂层）"></el-option>
                    </el-select>
                  </div>
                  <canvas ref="periodParetoCanvas" class="chart-canvas"></canvas>
                </div>
              </el-card>
            </div>
          </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'
import 'chartjs-plugin-datalabels'

// 响应式数据
const activeTab = ref('shift')
const dateRange = ref([])
// 筛选条件
const selectedProduct = ref('')
const selectedTeam = ref('all')
const selectedLine = ref('all')
const selectedEquipment = ref('all')
const selectedParetoView = ref('total') // 周/月度帕累托图视图选择

// Canvas 引用
const fpyChartCanvas = ref(null) // 当班FPY可视化图
const cpkChartCanvas = ref(null) // 当班Cpk趋势图
const histogramChartCanvas = ref(null) // 产品尺寸分布直方图
const xmrChartCanvas = ref(null) // X-MR控制图
const paretoChartCanvas = ref(null) // 缺陷帕累托图
const npControlChartCanvas = ref(null) // 当班计数型控制图（np图）
const periodHistogramCanvas = ref(null)
const periodParetoCanvas = ref(null)
const fpyComparisonCanvas = ref(null)
const cpkComparisonCanvas = ref(null)

// 图表实例
let fpyChart = null
let cpkChart = null
let histogramChart = null
let xmrChart = null
let paretoChart = null
let npControlChart = null
let periodHistogramChart = null
let periodParetoChart = null
let fpyComparisonChart = null
let cpkComparisonChart = null

// 伪造数据 - 当班数据
const shiftData = ref({
  fpy: 99.99, // 当班总FPY（用户要求：99.99%）
  hourlyFpy: [100.00, 100.00, 99.92, 100.00, 100.00, 100.00, 100.00, 100.00], // 按每小时分段的FPY趋势（用户要求的8个区间）
  hourlyProduction: [1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250], // 每小时生产数量
  hourlyPass: [1250, 1250, 1249, 1250, 1250, 1250, 1250, 1250], // 每小时合格数量
  cpk: 1.65, // 当班Cpk（用户要求：1.65）
  hourlyCpk: [1.68, 1.64, 1.65, 1.69, 1.67, 1.63, 1.66, 1.67], // 按每小时分段的Cpk趋势
  hourlyMean: [4.9998, 4.9999, 5.0000, 5.0001, 4.9999, 5.0000, 4.9999, 5.0001], // 每小时过程均值
  hourlyStdDev: [0.00027, 0.00029, 0.00028, 0.00026, 0.00027, 0.00029, 0.00028, 0.00027], // 每小时过程标准差
  histogram: {
    mean: 4.9999, // 均值
    stdDev: 0.00028, // 标准差
    specMin: 4.998, // 下规格限
    specMax: 5.002, // 上规格限
    bins: [80, 2920, 6000, 900, 100], // 频次分布（用户要求的5个区间）
    binLabels: ['4.9983-4.9990', '4.9990-4.9997', '4.9997-5.0004', '5.0004-5.0011', '5.0011-5.0017'], // 尺寸范围标签
    normalDistribution: [65, 2800, 6100, 1000, 35] // 正态分布拟合数据
  },
  xmr: {
    data: [4.9997, 4.9998, 4.9999, 5.0000, 5.0001, 4.9999, 4.9998, 4.9997, 4.9998, 4.9999, 5.0000, 5.0001, 5.0002, 5.0001, 5.0000, 4.9999, 4.9998, 4.9997, 4.9998, 4.9999, 5.0000, 5.0001, 5.0002, 5.0001, 5.0000, 4.9999, 5.0000, 5.0000, 4.9999, 4.9998, 4.9997, 4.9998, 4.9999, 5.0000, 5.0001, 5.0002, 5.0001, 5.0000, 4.9999, 4.9998, 4.9997, 4.9998, 4.9999, 5.0000, 5.0001, 5.0002, 5.0001, 5.0000, 4.9999, 5.0001], // 均值数据（50组）
    mrData: [0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0000, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002], // 移动极差数据（49组）
    ucl: 5.0007, // 上控制限
    lcl: 4.9993, // 下控制限
    uclMr: 0.0008, // 移动极差上控制限
    clMr: 0.0002 // 移动极差中心线
  },
  pareto: [
    { name: '粘炉灰', value: 1, percentage: 100.0, cumulative: 100.0, teams: ['乙班'], lines: ['2号线（CVD）'], location: '产品表面', severity: '轻微', suggestion: '检查炉内清洁度' },
    { name: '涂层前缺', value: 0, percentage: 0.0, cumulative: 100.0, teams: [], lines: [], location: '', severity: '', suggestion: '' },
    { name: '涂层后缺', value: 0, percentage: 0.0, cumulative: 100.0, teams: [], lines: [], location: '', severity: '', suggestion: '' },
    { name: '白点', value: 0, percentage: 0.0, cumulative: 100.0, teams: [], lines: [], location: '', severity: '', suggestion: '' },
    { name: '倒棱不均匀', value: 0, percentage: 0.0, cumulative: 100.0, teams: [], lines: [], location: '', severity: '', suggestion: '' },
    { name: '色差', value: 0, percentage: 0.0, cumulative: 100.0, teams: [], lines: [], location: '', severity: '', suggestion: '' },
    { name: '表面脏', value: 0, percentage: 0.0, cumulative: 100.0, teams: [], lines: [], location: '', severity: '', suggestion: '' }
  ],
  npControl: {
    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 缺陷数（50组）
    ucl: 2.1, // 上控制限
    lcl: 0, // 下控制限
    cl: 0.02 // 中心线（平均缺陷数）
  },
  productionInfo: {
    shift: '乙班', // 用户要求：乙班
    startTime: '16:00', // 用户要求：16:00-00:00
    endTime: '00:00',
    totalProducts: 10000, // 用户要求：10000件
    defectiveProducts: 1, // 用户要求：1件缺陷（粘炉灰）
    batchSize: 200 // 每批检测数量
  },
  dimensions: {
    name: 'YT15-160408', // 产品型号
    specMin: 4.998, // 下规格限（用户要求：4.998mm）
    specMax: 5.002, // 上规格限（用户要求：5.002mm）
    target: 5.000 // 目标值
  }
})

// 伪造数据 - 周/月度数据
const periodData = ref({
  overall: {
    fpy: 99.96, // 月度总FPY
    cpk: 1.57, // 月度总Cpk
    totalProducts: 200000, // 总生产数量
    defectiveProducts: 80 // 总缺陷数量
  },
  teams: {
    '甲班': {
      fpy: 99.98,
      cpk: 1.66,
      totalProducts: 66667,
      defectiveProducts: 13,
      dailyFpy: [99.99, 99.98, 99.97, 99.99, 99.98, 99.99, 99.98, 99.97, 99.99, 99.98, 99.99, 99.98, 99.97, 99.99, 99.98, 99.99, 99.98, 99.97, 99.99, 99.98] // 月度20个工作日的FPY数据
    },
    '乙班': {
      fpy: 99.96,
      cpk: 1.55,
      totalProducts: 66666,
      defectiveProducts: 33,
      dailyFpy: [99.97, 99.95, 99.96, 99.97, 99.95, 99.96, 99.97, 99.95, 99.96, 99.97, 99.95, 99.96, 99.97, 99.95, 99.96, 99.97, 99.95, 99.96, 99.97, 99.95] // 月度20个工作日的FPY数据
    },
    '丙班': {
      fpy: 99.94,
      cpk: 1.51,
      totalProducts: 66667,
      defectiveProducts: 34,
      dailyFpy: [99.96, 99.93, 99.94, 99.95, 99.93, 99.94, 99.95, 99.93, 99.94, 99.95, 99.93, 99.94, 99.95, 99.93, 99.94, 99.95, 99.93, 99.94, 99.95, 99.93] // 月度20个工作日的FPY数据
    }
  },
  histogram: {
    mean: 5.0001, // 均值
    stdDev: 0.00032, // 标准差
    specMin: 4.998, // 下规格限
    specMax: 5.002, // 上规格限
    bins: [800, 19200, 144000, 32000, 4000], // 频次分布（5个区间）
    binLabels: ['4.9980-4.9987', '4.9987-4.9994', '4.9994-5.0001', '5.0001-5.0008', '5.0008-5.0019'], // 尺寸范围标签
    normalDistribution: [600, 18000, 146000, 33000, 2400], // 正态分布拟合数据
    rSquared: 0.98 // 拟合度
  },
  pareto: {
    total: [
      { name: '粘炉灰', value: 30, percentage: 37.5, cumulative: 37.5 },
      { name: '倒棱不均匀', value: 20, percentage: 25.0, cumulative: 62.5 },
      { name: '表面脏', value: 10, percentage: 12.5, cumulative: 75.0 },
      { name: '涂层后缺', value: 8, percentage: 10.0, cumulative: 85.0 },
      { name: '白点', value: 6, percentage: 7.5, cumulative: 92.5 },
      { name: '涂层前缺', value: 4, percentage: 5.0, cumulative: 97.5 },
      { name: '色差', value: 2, percentage: 2.5, cumulative: 100.0 }
    ],
    teams: {
      '甲班': [
        { name: '粘炉灰', value: 8, percentage: 61.5, cumulative: 61.5 },
        { name: '倒棱不均匀', value: 3, percentage: 23.1, cumulative: 84.6 },
        { name: '表面脏', value: 2, percentage: 15.4, cumulative: 100.0 },
        { name: '涂层后缺', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '白点', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '涂层前缺', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '色差', value: 0, percentage: 0.0, cumulative: 100.0 }
      ],
      '乙班': [
        { name: '粘炉灰', value: 10, percentage: 30.3, cumulative: 30.3 },
        { name: '倒棱不均匀', value: 8, percentage: 24.2, cumulative: 54.5 },
        { name: '表面脏', value: 4, percentage: 12.1, cumulative: 66.7 },
        { name: '涂层后缺', value: 3, percentage: 9.1, cumulative: 75.8 },
        { name: '白点', value: 2, percentage: 6.1, cumulative: 81.9 },
        { name: '涂层前缺', value: 2, percentage: 6.1, cumulative: 88.0 },
        { name: '色差', value: 2, percentage: 6.1, cumulative: 94.1 },
        { name: '其他', value: 2, percentage: 6.1, cumulative: 100.0 }
      ],
      '丙班': [
        { name: '粘炉灰', value: 12, percentage: 35.3, cumulative: 35.3 },
        { name: '倒棱不均匀', value: 9, percentage: 26.5, cumulative: 61.8 },
        { name: '表面脏', value: 4, percentage: 11.8, cumulative: 73.6 },
        { name: '涂层后缺', value: 5, percentage: 14.7, cumulative: 88.3 },
        { name: '白点', value: 4, percentage: 11.8, cumulative: 100.0 },
        { name: '涂层前缺', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '色差', value: 0, percentage: 0.0, cumulative: 100.0 }
      ]
    },
    lines: {
      '1号线（PVD）': [
        { name: '倒棱不均匀', value: 18, percentage: 69.2, cumulative: 69.2 },
        { name: '涂层后缺', value: 6, percentage: 23.1, cumulative: 92.3 },
        { name: '表面脏', value: 2, percentage: 7.7, cumulative: 100.0 },
        { name: '粘炉灰', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '白点', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '涂层前缺', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '色差', value: 0, percentage: 0.0, cumulative: 100.0 }
      ],
      '2号线（CVD）': [
        { name: '粘炉灰', value: 28, percentage: 82.4, cumulative: 82.4 },
        { name: '白点', value: 5, percentage: 14.7, cumulative: 97.1 },
        { name: '涂层前缺', value: 1, percentage: 2.9, cumulative: 100.0 },
        { name: '倒棱不均匀', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '表面脏', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '涂层后缺', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '色差', value: 0, percentage: 0.0, cumulative: 100.0 }
      ],
      '3号线（混合涂层）': [
        { name: '表面脏', value: 8, percentage: 80.0, cumulative: 80.0 },
        { name: '色差', value: 2, percentage: 20.0, cumulative: 100.0 },
        { name: '粘炉灰', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '倒棱不均匀', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '涂层后缺', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '白点', value: 0, percentage: 0.0, cumulative: 100.0 },
        { name: '涂层前缺', value: 0, percentage: 0.0, cumulative: 100.0 }
      ]
    }
  },
  dimensions: {
    name: 'YT15-160408', // 产品型号
    specMin: 4.998, // 下规格限
    specMax: 5.002, // 上规格限
    target: 5.000 // 目标值
  }
})

// 初始化所有图表
const initCharts = () => {
  if (activeTab.value === 'shift') {
    initFpyChart()
    initCpkChart()
    initHistogramChart()
    initXMRChart()
    initParetoChart()
    initNPControlChart() // 添加图表6：当班计数型控制图
  } else {
    initPeriodFpyChart() // 图表7：周/月度FPY对比图
    initPeriodCpkChart() // 图表8：周/月度Cpk雷达图
    initPeriodHistogramChart() // 图表9：周/月度产品尺寸分布直方图
    initPeriodParetoChart() // 图表10：周/月度缺陷帕累托图
  }
}

// 图表6：当班计数型控制图（np图）
const initNPControlChart = () => {
  const ctx = npControlChartCanvas.value.getContext('2d')
  const groupNumbers = Array.from({ length: 50 }, (_, i) => i + 1) // 1-50组
  
  // 准备数据点样式
  const dataPoints = shiftData.value.npControl.data.map((value, index) => {
    return {
      x: index,
      y: value,
      backgroundColor: value === 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 205, 86, 1)',
      borderColor: value === 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 205, 86, 1)',
      borderWidth: 2,
      pointRadius: 5,
      pointStyle: value === 0 ? 'circle' : 'triangle',
      animation: value === 1 ? {
        duration: 2000,
        easing: 'easeInOutSine',
        loop: true,
        animateScale: true
      } : false
    }
  })
  
  npControlChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: groupNumbers,
      datasets: [{
        label: '缺陷数量（件）',
        data: shiftData.value.npControl.data,
        backgroundColor: dataPoints.map(point => point.backgroundColor),
        borderColor: 'rgba(75, 192, 192, 0.3)',
        borderWidth: 1,
        pointBackgroundColor: dataPoints.map(point => point.backgroundColor),
        pointBorderColor: dataPoints.map(point => point.borderColor),
        pointBorderWidth: dataPoints.map(point => point.borderWidth),
        pointRadius: dataPoints.map(point => point.pointRadius),
        pointStyle: dataPoints.map(point => point.pointStyle),
        fill: false
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          min: 0,
          max: 3,
          title: {
            display: true,
            text: '缺陷数量（件）'
          },
          ticks: {
            stepSize: 1
          }
        },
        x: {
          title: {
            display: true,
            text: '组号（每组200件）'
          },
          ticks: {
            maxRotation: 0
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `乙班（${shiftData.value.productionInfo.startTime}-${shiftData.value.productionInfo.endTime}）计数型控制图（np图）`
        },
        legend: {
          display: false
        },
        annotation: {
          annotations: {
            // 上控制限（UCL）
            uclLine: {
              type: 'line',
              yMin: shiftData.value.npControl.ucl,
              yMax: shiftData.value.npControl.ucl,
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `UCL=2.1件`,
                enabled: true,
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                color: 'white'
              }
            },
            // 中心线（CL）
            clLine: {
              type: 'line',
              yMin: shiftData.value.npControl.cl,
              yMax: shiftData.value.npControl.cl,
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 2,
              label: {
                content: `CL=0.02件`,
                enabled: true,
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                color: 'white'
              }
            },
            // 下控制限（LCL）
            lclLine: {
              type: 'line',
              yMin: shiftData.value.npControl.lcl,
              yMax: shiftData.value.npControl.lcl,
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `LCL=0件`,
                enabled: true,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                color: 'white'
              }
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.parsed.y
              const group = context.parsed.x + 1
              const status = value === 0 ? '正常' : value === 1 ? '预警' : '异常'
              return [
                `组号: ${group}`,
                `缺陷数量: ${value}件`,
                `状态: ${status}`
              ]
            }
          }
        }
      },
      onClick: function(event, elements) {
        if (elements.length > 0) {
          const element = elements[0]
          const index = element.index
          const value = shiftData.value.npControl.data[index]
          const group = index + 1
          
          // 显示详细信息
          ElMessage({
            message: `组号: ${group}\n缺陷数量: ${value}件\n每组样本量: 200件\n状态: ${value === 0 ? '正常' : value === 1 ? '预警' : '异常'}`,
            type: value === 0 ? 'success' : value === 1 ? 'warning' : 'error',
            duration: 3000
          })
        }
      }
    }
  })
}

// 图表7：周/月度FPY对比图
const initPeriodFpyChart = () => {
  if (!fpyComparisonCanvas.value) return
  const ctx = fpyComparisonCanvas.value.getContext('2d')
  
  // 准备数据
  const labels = ['月度总览', '甲班', '乙班', '丙班']
  const fpyValues = [
    periodData.value.overall.fpy,
    periodData.value.teams['甲班'].fpy,
    periodData.value.teams['乙班'].fpy,
    periodData.value.teams['丙班'].fpy
  ]
  
  // 准备周趋势数据（月度按周）
  const weeklyTrendData = [99.95, 99.96, 99.97, 99.96]
  const weeklyLabels = ['第1周', '第2周', '第3周', '第4周']
  
  fpyComparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'FPY值',
        data: fpyValues,
        backgroundColor: [
          'rgba(153, 102, 255, 0.6)', // 月度总览 - 紫色
          'rgba(75, 192, 192, 0.6)',   // 甲班 - 绿色
          'rgba(54, 162, 235, 0.6)',   // 乙班 - 蓝色
          'rgba(255, 205, 86, 0.6)'    // 丙班 - 黄色
        ],
        borderColor: [
          'rgba(153, 102, 255, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 205, 86, 1)'
        ],
        borderWidth: 1
      }, {
        label: '周FPY趋势',
        data: weeklyTrendData,
        type: 'line',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false,
        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        yAxisID: 'y'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          min: 99.90,
          max: 100.00,
          title: {
            display: true,
            text: 'FPY值（%）'
          },
          ticks: {
            stepSize: 0.01,
            callback: function(value) {
              return value.toFixed(2) + '%'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '维度'
          }
        }
      },
      plugins: {
          title: {
            display: true,
            text: '11月月度FPY对比图'
          },
          legend: {
            position: 'top'
          }
        }
      }
    })
  }

// 图表8：周/月度Cpk雷达图
const initPeriodCpkChart = () => {
  if (!cpkComparisonCanvas.value) return
  const ctx = cpkComparisonCanvas.value.getContext('2d')
  
  // 准备雷达图数据
  const radarData = {
    labels: ['尺寸 Cpk', '色差 Cpk', '涂层厚度 Cpk'],
    datasets: [
      {
        label: '甲班',
        data: [1.66, 1.62, 1.58], // 甲班各指标Cpk值（最高）
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      },
      {
        label: '乙班',
        data: [1.55, 1.52, 1.49], // 乙班各指标Cpk值
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      },
      {
        label: '丙班',
        data: [1.51, 1.48, 1.45], // 丙班各指标Cpk值（最低）
        backgroundColor: 'rgba(255, 205, 86, 0.2)',
        borderColor: 'rgba(255, 205, 86, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(255, 205, 86, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      }
    ]
  }
  
  cpkComparisonChart = new Chart(ctx, {
    type: 'radar',
    data: radarData,
    options: {
      responsive: true,
      scales: {
        r: {
          beginAtZero: true,
          min: 1.0,
          max: 2.0,
          ticks: {
            stepSize: 0.2,
            callback: function(value) {
              return value.toFixed(2)
            }
          },
          grid: {
            color: 'rgba(200, 200, 200, 0.2)'
          },
          angleLines: {
            color: 'rgba(200, 200, 200, 0.3)'
          },
          pointLabels: {
            font: {
              size: 12
            }
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '11月月度Cpk雷达图'
        },
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const datasetLabel = context.dataset.label
              const value = context.parsed.r
              const dimension = context.label
              
              return [
                `${datasetLabel} ${dimension}: ${value.toFixed(2)}`,
                `合格标准: 1.33`,
                `状态: ${value >= 1.33 ? '合格' : '不合格'}`
              ]
            }
          }
        },
        // 添加数值标注
        datalabels: {
          display: true,
          formatter: function(value) {
            return value.toFixed(2)
          },
          font: {
            size: 10,
            weight: 'bold'
          },
          color: '#fff',
          backgroundColor: function(context) {
            return context.dataset.borderColor
          },
          borderRadius: 10,
          padding: 5
        },
        // 添加合格标准线
        annotation: {
          annotations: {
            standardCircle: {
              type: 'line',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              backgroundColor: 'rgba(255, 99, 132, 0.1)',
              borderRadius: 0,
              x0: '50%',
              y0: '50%',
              x1: '50%',
              y1: '0%',
              radius: (1.33 - 1.0) / (2.0 - 1.0) * 100 + '%',
              rotation: 0,
              label: {
                content: '合格标准 Cpk=1.33',
                enabled: true,
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                color: 'white',
                font: {
                  size: 12
                }
              }
            }
          }
        }
      },
      // 启用图表点击事件
      onClick: function(event, elements) {
        if (elements.length > 0) {
          const element = elements[0]
          const datasetIndex = element.datasetIndex
          const dataIndex = element.index
          const datasetLabel = radarData.datasets[datasetIndex].label
          const label = radarData.labels[dataIndex]
          const value = radarData.datasets[datasetIndex].data[dataIndex]
          
          // 显示详细信息
          ElMessage({
            message: `${datasetLabel} ${label}: ${value.toFixed(2)}\n合格标准: 1.33\n状态: ${value >= 1.33 ? '合格' : '不合格'}`,
            type: value >= 1.33 ? 'success' : 'error',
            duration: 3000
          })
        }
      }
    }
  })
}

// 图表9：周/月度产品尺寸分布直方图
const initProductSizeHistogramChart = () => {
  if (!periodHistogramCanvas.value) return
  const ctx = periodHistogramCanvas.value.getContext('2d')
  
  // 准备直方图数据
  const histogramData = {
    labels: periodData.value.histogram.rangeLabels,
    datasets: [
      {
        label: '频次（件）',
        data: periodData.value.histogram.frequencies,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        order: 2
      },
      {
        label: '正态分布拟合',
        data: periodData.value.histogram.normalDistribution,
        type: 'line',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        fill: false,
        tension: 0.4,
        order: 1
      }
    ]
  }
  
  periodHistogramChart = new Chart(ctx, {
    type: 'bar',
    data: histogramData,
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 150000,
          title: {
            display: true,
            text: '频次（件）'
          },
          ticks: {
            stepSize: 10000,
            callback: function(value) {
              return value.toLocaleString()
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '尺寸区间（mm）'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '11月月度产品尺寸分布直方图'
        },
        legend: {
          position: 'top'
        },
        annotation: {
          annotations: {
            // 公差中心区（4.999-5.001mm）
            centerZone: {
              type: 'box',
              xMin: 1,
              xMax: 3,
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 0.5)',
              borderWidth: 1,
              label: {
                content: '公差中心区',
                enabled: true,
                position: 'top',
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                color: 'white',
                font: {
                  size: 12
                }
              }
            },
            // 右上角标注信息
            statsAnnotation: {
              type: 'label',
              content: [
                `均值 = ${periodData.value.histogram.mean} mm`,
                `标准差 = ${periodData.value.histogram.stdDev} mm`,
                `R² = ${periodData.value.histogram.rSquared}`
              ],
              position: 'top-right',
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              color: 'white',
              font: {
                size: 12
              },
              padding: {
                x: 10,
                y: 10
              },
              borderRadius: 5
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const datasetLabel = context.dataset.label
              const value = context.parsed.y
              const label = context.label
              
              if (datasetLabel === '频次（件）') {
                const index = context.dataIndex
                const frequency = periodData.value.histogram.frequencies[index]
                const percentage = periodData.value.histogram.percentages[index]
                
                return [
                  `${datasetLabel}: ${frequency.toLocaleString()}件`,
                  `占比: ${percentage.toFixed(1)}%`
                ]
              } else if (datasetLabel === '正态分布拟合') {
                return `${datasetLabel}: ${value.toFixed(2)}`
              }
              
              return `${datasetLabel}: ${value}`
            }
          }
        }
      },
      // 启用图表点击事件
      onClick: function(event, elements) {
        if (elements.length > 0) {
          const element = elements[0]
          const datasetIndex = element.datasetIndex
          const index = element.index
          
          if (datasetIndex === 0) { // 只处理柱状图点击
            const rangeLabel = periodData.value.histogram.rangeLabels[index]
            const frequency = periodData.value.histogram.frequencies[index]
            const percentage = periodData.value.histogram.percentages[index]
            
            // 显示详细信息
            ElMessage({
              message: `尺寸区间: ${rangeLabel}\n频次: ${frequency.toLocaleString()}件\n占比: ${percentage.toFixed(1)}%`,
              type: 'info',
              duration: 3000
            })
          }
        }
      }
    }
  })
}

// 图表10：周/月度缺陷帕累托图
const initProductDefectParetoChart = () => {
  if (!periodParetoCanvas.value) return
  const ctx = periodParetoCanvas.value.getContext('2d')
  
  // 根据选择的视图获取数据
  const getFilteredData = () => {
    let filteredData = []
    
    if (selectedParetoView.value === 'total') {
      // 总缺陷数据
      filteredData = periodData.value.pareto.total.map(defect => ({
        name: defect.name,
        count: defect.value,
        percentage: defect.percentage
      }))
    } else if (periodData.value.pareto.teams[selectedParetoView.value]) {
      // 按班组筛选
      filteredData = periodData.value.pareto.teams[selectedParetoView.value].map(defect => ({
        name: defect.name,
        count: defect.value,
        percentage: defect.percentage
      })).filter(defect => defect.count > 0)
    }
    
    // 按数量降序排序
    return filteredData.sort((a, b) => b.count - a.count)
  }
  
  // 计算累计百分比
  const calculateCumulativePercentage = (data) => {
    let cumulative = 0
    return data.map(item => {
      cumulative += item.percentage
      return cumulative
    })
  }
  
  // 获取筛选后的数据
  const filteredData = getFilteredData()
  const cumulativePercentages = calculateCumulativePercentage(filteredData)
  
  // 准备帕累托图数据
  const paretoData = {
    labels: filteredData.map(item => item.name),
    datasets: [
      {
        label: '缺陷数量（件）',
        data: filteredData.map(item => item.count),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        yAxisID: 'y'
      },
      {
        label: '累计占比（%）',
        data: cumulativePercentages,
        type: 'line',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        fill: false,
        yAxisID: 'y1',
        tension: 0.1,
        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 1,
        pointRadius: 5
      }
    ]
  }
  
  // 销毁旧图表
  if (periodParetoChart) {
    periodParetoChart.destroy()
  }
  
  periodParetoChart = new Chart(ctx, {
    type: 'bar',
    data: paretoData,
    options: {
      responsive: true,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          beginAtZero: true,
          max: 35,
          title: {
            display: true,
            text: '缺陷数量（件）'
          },
          grid: {
            drawBorder: true
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: '累计占比（%）'
          },
          grid: {
            drawOnChartArea: false
          },
          ticks: {
            callback: function(value) {
              return value + '%'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '缺陷类型'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `11月月度缺陷帕累托图 - ${selectedParetoView.value === 'total' ? '总缺陷' : selectedParetoView.value}`
        },
        legend: {
          position: 'top'
        },
        annotation: {
          annotations: {
            // 80%累计占比线
            eightyPercentLine: {
              type: 'line',
              yMin: 80,
              yMax: 80,
              yAxisID: 'y1',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '80%累计占比线',
                enabled: true,
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                color: 'white',
                font: {
                  size: 12
                },
                position: 'right'
              }
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const datasetLabel = context.dataset.label
              const value = context.parsed.y
              const label = context.label
              const index = context.dataIndex
              
              if (datasetLabel === '缺陷数量（件）') {
                const percentage = filteredData[index].percentage
                const cumulative = cumulativePercentages[index]
                
                return [
                  `${datasetLabel}: ${value}件`,
                  `占比: ${percentage.toFixed(1)}%`,
                  `累计占比: ${cumulative.toFixed(1)}%`
                ]
              } else if (datasetLabel === '累计占比（%）') {
                return `${datasetLabel}: ${value.toFixed(1)}%`
              }
              
              return `${datasetLabel}: ${value}`
            }
          }
        }
      },
      // 启用图表点击事件
      onClick: function(event, elements) {
        if (elements.length > 0) {
          const element = elements[0]
          const datasetIndex = element.datasetIndex
          const index = element.index
          
          if (datasetIndex === 0) { // 只处理柱状图点击
            const defectName = filteredData[index].name
            const count = filteredData[index].count
            
            // 显示该缺陷在各班组/产线的分布明细
            const defectDetails = periodData.value.pareto.defects.find(d => d.name === defectName)
            if (defectDetails) {
              let message = `缺陷类型: ${defectName}\n总数量: ${defectDetails.total}件\n`
              message += `分布明细:\n`
              message += `- 甲班: ${defectDetails.a}件\n`
              message += `- 乙班: ${defectDetails.b}件\n`
              message += `- 丙班: ${defectDetails.c}件\n`
              message += `- 1号线: ${defectDetails.line1}件\n`
              message += `- 2号线: ${defectDetails.line2}件\n`
              message += `- 3号线: ${defectDetails.line3}件\n`
              message += `- 4号线: ${defectDetails.line4}件`
              
              ElMessage({
                message: message,
                type: 'info',
                duration: 5000
              })
            }
          }
        }
      }
    }
  })
}

// 监听帕累托图视图变化
watch(selectedParetoView, () => {
  if (activeTab.value === 'period') {
    initProductDefectParetoChart()
  }
})

// 图表1：当班FPY可视化图
const initFpyChart = () => {
  const ctx = fpyChartCanvas.value.getContext('2d')
  const timeLabels = ['16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-00:00']
  
  fpyChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: timeLabels,
      datasets: [{
        label: 'FPY(%)',
        data: shiftData.value.hourlyFpy,
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          min: 99.90,
          max: 100.00,
          title: {
            display: true,
            text: 'FPY(%)'
          },
          ticks: {
            stepSize: 0.01,
            callback: function(value) {
              return value + '%'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '时间分段'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `乙班（${shiftData.value.productionInfo.startTime}-${shiftData.value.productionInfo.endTime}）FPY趋势`
        },
        annotation: {
          annotations: {
            // 合格线（99.90%）
            qualifiedLine: {
              type: 'line',
              yMin: 99.90,
              yMax: 99.90,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '合格线（99.90%）',
                enabled: true,
                position: 'end'
              }
            },
            // 优秀线（99.98%）
            excellentLine: {
              type: 'line',
              yMin: 99.98,
              yMax: 99.98,
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '优秀线（99.98%）',
                enabled: true,
                position: 'end'
              }
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) {
                label += ': '
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y + '%'
              }
              return label
            },
            afterLabel: function(context) {
              const index = context.dataIndex
              const production = shiftData.value.hourlyProduction[index]
              const pass = shiftData.value.hourlyPass[index]
              const defect = production - pass
              
              return [
                `生产数量: ${production}件`,
                `合格数量: ${pass}件`,
                `缺陷数量: ${defect}件`,
                defect > 0 ? `缺陷类型: 粘炉灰` : `无缺陷`
              ]
            }
          }
        }
      }
    }
  })
}

// 图表2：当班Cpk趋势图
const initCpkChart = () => {
  const ctx = cpkChartCanvas.value.getContext('2d')
  const timeLabels = ['16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-00:00']
  
  cpkChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: timeLabels,
      datasets: [{
        label: 'Cpk值',
        data: shiftData.value.hourlyCpk,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.3,
        borderWidth: 3,
        fill: true,
        pointBackgroundColor: function(context) {
          // 根据Cpk值设置点的颜色
          const value = context.dataset.data[context.dataIndex];
          if (value < 1.33) {
            return 'rgba(255, 0, 0, 1)'; // 不合格 - 红色
          } else if (value < 1.67) {
            return 'rgba(255, 159, 64, 1)'; // 合格但未达优秀 - 橙色
          } else {
            return 'rgba(75, 192, 192, 1)'; // 优秀 - 绿色
          }
        },
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          min: 1.33,
          max: 1.80,
          title: {
            display: true,
            text: 'Cpk值'
          }
        },
        x: {
          title: {
            display: true,
            text: '时间分段'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `乙班（${shiftData.value.productionInfo.startTime}-${shiftData.value.productionInfo.endTime}）Cpk趋势`
        },
        subtitle: {
          display: true,
          text: `尺寸标准：LSL=${shiftData.value.dimensions.specMin}mm，USL=${shiftData.value.dimensions.specMax}mm`
        },
        annotation: {
          annotations: {
            // 合格线（1.33）
            qualifiedLine: {
              type: 'line',
              yMin: 1.33,
              yMax: 1.33,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '合格线（1.33）',
                enabled: true,
                position: 'end'
              }
            },
            // 优秀线（1.67）
            excellentLine: {
              type: 'line',
              yMin: 1.67,
              yMax: 1.67,
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '优秀线（1.67）',
                enabled: true,
                position: 'end'
              }
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) {
                label += ': '
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y.toFixed(2)
              }
              return label
            },
            afterLabel: function(context) {
              const index = context.dataIndex
              const mean = shiftData.value.hourlyMean[index]
              const stdDev = shiftData.value.hourlyStdDev[index]
              
              return [
                `过程均值: ${mean.toFixed(4)}mm`,
                `过程标准差: ${stdDev.toFixed(6)}mm`,
                `状态: ${context.parsed.y >= 1.67 ? '优秀' : (context.parsed.y >= 1.33 ? '合格' : '不合格')}`
              ]
            }
          }
        }
      }
    }
  })
}

// 图表3：产品尺寸分布直方图
const initHistogramChart = () => {
  const ctx = histogramChartCanvas.value.getContext('2d')
  histogramChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: shiftData.value.histogram.binLabels,
      datasets: [
        {
          label: '频次',
          data: shiftData.value.histogram.bins,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          yAxisID: 'y'
        },
        {
          label: '正态分布',
          data: shiftData.value.histogram.normalDistribution,
          type: 'line',
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          yAxisID: 'y'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '频次'
          },
          min: 0,
          max: 6500, // 用户要求的最大值
          ticks: {
            stepSize: 500 // 用户要求的刻度间隔
          }
        },
        x: {
          title: {
            display: true,
            text: '尺寸(mm)'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `产品尺寸分布直方图 - ${shiftData.value.dimensions.name}`
        },
        subtitle: {
          display: true,
          text: `尺寸范围：${shiftData.value.histogram.binLabels[0]}mm-${shiftData.value.histogram.binLabels[shiftData.value.histogram.binLabels.length-1]}mm`
        },
        annotation: {
          annotations: {
            // 公差中心区阴影
            centerZone: {
              type: 'box',
              xMin: 1, // 对应 binLabels 中 '4.9990-4.9997'
              xMax: 3, // 对应 binLabels 中 '5.0004-5.0011'
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 0.5)',
              borderWidth: 1,
              borderDash: [5, 5],
              label: {
                content: '公差中心区',
                enabled: true
              }
            },
            // 公差边界区阴影（左）
            leftBoundary: {
              type: 'box',
              xMin: 0, // 对应 binLabels 中 '4.9983-4.9990'
              xMax: 1,
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              borderColor: 'rgba(255, 206, 86, 0.5)',
              borderWidth: 1,
              borderDash: [5, 5],
              label: {
                content: '公差边界区',
                enabled: true
              }
            },
            // 公差边界区阴影（右）
            rightBoundary: {
              type: 'box',
              xMin: 3, // 对应 binLabels 中 '5.0004-5.0011'
              xMax: 4, // 对应 binLabels 中 '5.0011-5.0017'
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              borderColor: 'rgba(255, 206, 86, 0.5)',
              borderWidth: 1,
              borderDash: [5, 5]
            },
            // 标注均值和标准差
            meanLabel: {
              type: 'label',
              content: `均值: ${shiftData.value.histogram.mean.toFixed(4)}mm`,
              position: {
                x: 'left',
                y: 'top'
              },
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              color: 'white',
              padding: 10,
              borderRadius: 5
            },
            stdDevLabel: {
              type: 'label',
              content: `标准差: ${shiftData.value.histogram.stdDev.toFixed(6)}mm`,
              position: {
                x: 'left',
                y: 'top'
              },
              yAdjust: 30,
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              color: 'white',
              padding: 10,
              borderRadius: 5
            }
          }
        },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              if (context.dataset.label === '频次') {
                const binIndex = context.dataIndex
                const binLabel = context.label
                const frequency = context.parsed.y
                const total = shiftData.value.histogram.bins.reduce((sum, val) => sum + val, 0)
                const percentage = ((frequency / total) * 100).toFixed(2)
                
                return [
                  `尺寸区间: ${binLabel}`,
                  `占比: ${percentage}%`
                ]
              }
              return []
            }
          }
        }
      }
    }
  })
}

// X-MR 控制图
// 图表4：X-MR控制图（均值-移动极差控制图）
const initXMRChart = () => {
  const ctx = xmrChartCanvas.value.getContext('2d')
  xmrChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: shiftData.value.xmr.data.length }, (_, i) => i + 1),
      datasets: [{
        label: 'X (均值)',
        data: shiftData.value.xmr.data,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.1,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        yAxisID: 'y'
      }, {
        label: 'MR (移动极差)',
        data: shiftData.value.xmr.mrData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.1,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointStyle: 'rect',
        yAxisID: 'y1'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: '均值X(mm)'
          },
          min: 4.9992, // 用户要求的LCL-0.0001
          max: 5.0008, // 用户要求的UCL+0.0001
          grid: {
            drawBorder: true
          },
          ticks: {
            callback: function(value) {
              return value.toFixed(4);
            }
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: '移动极差MR(mm)'
          },
          min: 0,
          max: 0.0010, // 用户要求的最大值
          grid: {
            drawOnChartArea: false
          },
          ticks: {
            callback: function(value) {
              return value.toFixed(6);
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '组号'
          },
          max: 50, // 用户要求的50组
          ticks: {
            stepSize: 5
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'X-MR控制图（均值-移动极差控制图）'
        },
        subtitle: {
          display: true,
          text: `组数据：每200件为1组，共50组 - ${shiftData.value.dimensions.name}`
        },
        annotation: {
          annotations: {
            // X图控制限
            uclX: {
              type: 'line',
              yMin: shiftData.value.xmr.ucl,
              yMax: shiftData.value.xmr.ucl,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `UCL: ${shiftData.value.xmr.ucl.toFixed(4)}mm`,
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y'
            },
            lclX: {
              type: 'line',
              yMin: shiftData.value.xmr.lcl,
              yMax: shiftData.value.xmr.lcl,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `LCL: ${shiftData.value.xmr.lcl.toFixed(4)}mm`,
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y'
            },
            clX: {
              type: 'line',
              yMin: shiftData.value.histogram.mean,
              yMax: shiftData.value.histogram.mean,
              borderColor: 'rgba(0, 0, 255, 1)',
              borderWidth: 2,
              label: {
                content: `CL: ${shiftData.value.histogram.mean.toFixed(4)}mm`,
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y'
            },
            // MR图控制限
            uclMr: {
              type: 'line',
              yMin: shiftData.value.xmr.uclMr,
              yMax: shiftData.value.xmr.uclMr,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `UCL_MR: ${shiftData.value.xmr.uclMr.toFixed(6)}mm`,
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y1'
            },
            clMr: {
              type: 'line',
              yMin: shiftData.value.xmr.clMr,
              yMax: shiftData.value.xmr.clMr,
              borderColor: 'rgba(0, 0, 255, 1)',
              borderWidth: 2,
              label: {
                content: `CL_MR: ${shiftData.value.xmr.clMr.toFixed(6)}mm`,
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y1'
            }
          }
        },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const value = context.parsed.y;
              const groupNumber = context.dataIndex + 1;
              const productionTime = shiftData.value.hourlyTime[Math.floor((groupNumber * 200) / 1250)];
              
              const result = [
                `组号: ${groupNumber}`,
                `生产时间: ${productionTime}`,
                `产品型号: ${shiftData.value.productionInfo.productModel}`,
                `设备编号: ${shiftData.value.productionInfo.device}`
              ];
              
              if (context.dataset.label.includes('X')) {
                if (value > shiftData.value.xmr.ucl) {
                  result.push('状态: 超出上控制限');
                  result.push('建议: 检查工艺参数');
                } else if (value < shiftData.value.xmr.lcl) {
                  result.push('状态: 超出下控制限');
                  result.push('建议: 检查设备稳定性');
                } else {
                  result.push('状态: 正常');
                }
              } else if (context.dataset.label.includes('MR')) {
                if (value > shiftData.value.xmr.uclMr) {
                  result.push('状态: 超出移动极差上控制限');
                  result.push('建议: 检查测量系统');
                } else {
                  result.push('状态: 正常');
                }
              }
              return result;
            }
          }
        },
        // 添加点击交互
        onClick: (evt, elements) => {
          if (elements.length > 0) {
            const element = elements[0];
            const index = element.index;
            const groupNumber = index + 1;
            const dataValue = element.parsed.y;
            const productionTime = shiftData.value.hourlyTime[Math.floor((groupNumber * 200) / 1250)];
            
            // 显示详细信息
            alert(`组号: ${groupNumber}\n数据值: ${dataValue.toFixed(6)}mm\n生产时间: ${productionTime}\n产品型号: ${shiftData.value.productionInfo.productModel}\n设备编号: ${shiftData.value.productionInfo.device}`);
          }
        }
      }
    }
  })
}

// 图表5：缺陷帕累托图（Pareto图）
const initParetoChart = () => {
  // 计算累计占比（使用现有数据中的cumulative字段）
  const total = shiftData.value.pareto.reduce((sum, item) => sum + item.value, 0)

  const ctx = paretoChartCanvas.value.getContext('2d')
  paretoChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: shiftData.value.pareto.map(item => item.name),
      datasets: [{
        label: '缺陷数',
        data: shiftData.value.pareto.map(item => item.value),
        backgroundColor: function(context) {
          // 重点缺陷（占比超80%）用红色标注
          const value = context.dataset.data[context.dataIndex]
          const percentage = (value / total) * 100
          return percentage > 80 ? 'rgba(255, 99, 132, 0.8)' : 'rgba(255, 99, 132, 0.4)'
        },
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        yAxisID: 'y'
      }, {
        label: '累计占比 (%)',
        data: shiftData.value.pareto.map(item => item.cumulative),
        type: 'line',
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        yAxisID: 'y1',
        tension: 0.1,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '缺陷数'
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          min: 0,
          max: 2, // 用户要求的最大值
          ticks: {
            stepSize: 1
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: '累计占比 (%)'
          },
          min: 0,
          max: 100,
          grid: {
            drawOnChartArea: false
          },
          ticks: {
            callback: function(value) {
              return value + '%'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '缺陷类型（按占比降序）'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '缺陷帕累托图（Pareto图）'
        },
        subtitle: {
          display: true,
          text: '缺陷涉及批次：第 38 组（7601-7800 件），产品型号：YT15-120404，关联设备：2 号线 CVD 设备'
        },
        annotation: {
          annotations: {
            // 80%累计占比线
            eightyPercentLine: {
              type: 'line',
              yMin: 80,
              yMax: 80,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '80%累计占比线（关键少数）',
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y1'
            },
            // 80%重点改善线
            eightyPercent: {
              type: 'line',
              yMin: 80,
              yMax: 80,
              borderColor: 'rgba(255, 159, 64, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '重点改善线（80%）',
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y1'
            }
          }
        },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              if (context.dataset.label === '缺陷数') {
                const value = context.parsed.y
                const percentage = (value / total) * 100
                return [
                  `占比: ${percentage.toFixed(2)}%`,
                  `累计占比: ${shiftData.value.pareto[context.dataIndex].cumulative.toFixed(2)}%`
                ]
              }
              return []
            }
          }
        },
        legend: {
          position: 'top'
        }
      }
    }
  })
}

// 计数型控制图
const initCountControlChart = () => {
  const ctx = countControlChartCanvas.value.getContext('2d')
  countControlChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: shiftData.value.countControl.data.length }, (_, i) => `批次 ${i + 1}`),
      datasets: [{
        label: '缺陷数',
        data: shiftData.value.countControl.data,
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        tension: 0.1,
        borderWidth: 2,
        pointBackgroundColor: function(context) {
          // 超界点用红色标记
          const value = context.dataset.data[context.dataIndex]
          if (value > shiftData.value.countControl.ucl || value < shiftData.value.countControl.lcl) {
            return 'rgba(255, 0, 0, 1)'
          }
          return 'rgba(153, 102, 255, 1)'
        },
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '缺陷数'
          },
          min: Math.max(0, shiftData.value.countControl.lcl - 2),
          max: shiftData.value.countControl.ucl + 2
        },
        x: {
          title: {
            display: true,
            text: '检测批次（每200件/批）'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '计数型控制图（np图 - 缺陷数监控）'
        },
        legend: {
          position: 'top'
        },
        annotation: {
          annotations: {
            ucl: {
              type: 'line',
              yMin: shiftData.value.countControl.ucl,
              yMax: shiftData.value.countControl.ucl,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `UCL: ${shiftData.value.countControl.ucl}`,
                enabled: true,
                position: 'end'
              }
            },
            lcl: {
              type: 'line',
              yMin: shiftData.value.countControl.lcl,
              yMax: shiftData.value.countControl.lcl,
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `LCL: ${shiftData.value.countControl.lcl}`,
                enabled: true,
                position: 'end'
              }
            },
            cl: {
              type: 'line',
              yMin: shiftData.value.countControl.cl,
              yMax: shiftData.value.countControl.cl,
              borderColor: 'rgba(0, 255, 0, 1)',
              borderWidth: 2,
              label: {
                content: `CL: ${shiftData.value.countControl.cl}`,
                enabled: true,
                position: 'end'
              }
            }
          }
        },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const value = context.parsed.y
              const isOutOfControl = value > shiftData.value.countControl.ucl || value < shiftData.value.countControl.lcl
              let status = '状态: 正常'
              let suggestion = ''
              
              if (isOutOfControl) {
                status = '状态: 超界异常'
                suggestion = '建议: 立即停止生产，检查设备参数和生产工艺'
              }
              
              return [status, suggestion]
            }
          }
        },
        onClick: function(event, elements) {
          if (elements.length > 0) {
            const index = elements[0].index
            const batchData = shiftData.value.countControl.batchDetails[index]
            const isOutOfControl = batchData.value > shiftData.value.countControl.ucl || batchData.value < shiftData.value.countControl.lcl
            
            // 显示批次详情
            ElMessageBox.alert(`
              检测批次: ${index + 1}\n              检测数量: ${batchData.inspected}\n              缺陷数: ${batchData.value}\n              缺陷率: ${batchData.defectRate}%\n              检测时间: ${batchData.time}\n              检测设备: ${batchData.device}\n              检测人员: ${batchData.inspector}\n              状态: ${isOutOfControl ? '超界异常' : '正常'}\n              处理建议: ${isOutOfControl ? '立即停止生产，检查设备参数和生产工艺' : '继续生产，保持监控'}\n            `, '批次详情', {
              confirmButtonText: '确定',
              type: isOutOfControl ? 'warning' : 'info'
            })
          }
        }
      }
    }
  })
}

// 周/月度直方图
const initPeriodHistogramChart = () => {
  if (!periodHistogramCanvas.value) return
  const ctx = periodHistogramCanvas.value.getContext('2d')
  periodHistogramChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: periodData.value.histogram.binLabels,
      datasets: [{
        label: '频次',
        data: periodData.value.histogram.bins,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        yAxisID: 'y'
      }, {
        label: '正态分布',
        data: periodData.value.histogram.normalDistribution,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',
        borderWidth: 2,
        fill: true,
        type: 'line',
        yAxisID: 'y'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '频次'
          }
        },
        x: {
          title: {
            display: true,
            text: '尺寸(mm)'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `月度产品尺寸分布直方图 - ${periodData.value.dimensions.name}`
        },
        annotation: {
          annotations: {
            // 公差区间阴影
            toleranceZone: {
              type: 'box',
              xMin: 1, // 对应 binLabels 中 '4.998-4.999'
              xMax: 4, // 对应 binLabels 中 '5.001-5.002'
              backgroundColor: 'rgba(0, 255, 0, 0.1)',
              borderColor: 'rgba(0, 255, 0, 0.5)',
              borderWidth: 1,
              borderDash: [5, 5]
            },
            specMin: {
              type: 'line',
              xMin: 1,
              xMax: 1,
              borderColor: 'red',
              borderWidth: 2,
              label: {
                content: `规格下限: ${periodData.value.histogram.specMin}mm`,
                enabled: true
              }
            },
            specMax: {
              type: 'line',
              xMin: 4,
              xMax: 4,
              borderColor: 'red',
              borderWidth: 2,
              label: {
                content: `规格上限: ${periodData.value.histogram.specMax}mm`,
                enabled: true
              }
            },
            target: {
              type: 'line',
              xMin: 2.5, // 对应 binLabels 中 '5.000-5.001' 中间
              xMax: 2.5,
              borderColor: 'blue',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: `目标值: ${periodData.value.dimensions.target}mm`,
                enabled: true
              }
            }
          }
        }
      }
    }
  })
}

// 周/月度帕累图
const initPeriodParetoChart = () => {
  if (!periodParetoCanvas.value) return
  
  // 根据选择的视图获取对应的帕累托图数据
  let paretoData;
  const viewValue = selectedParetoView.value;
  
  if (viewValue === 'total') {
    paretoData = periodData.value.pareto.total;
  } else if (viewValue.startsWith('team_')) {
    // 处理班组视图
    const teamName = viewValue.substring(5); // 去掉 'team_' 前缀
    paretoData = periodData.value.pareto.teams[teamName] || periodData.value.pareto.total;
  } else if (viewValue.startsWith('line_')) {
    // 处理产线视图
    const lineName = viewValue.substring(5); // 去掉 'line_' 前缀
    paretoData = periodData.value.pareto.lines[lineName] || periodData.value.pareto.total;
  } else {
    // 默认使用总缺陷数据
    paretoData = periodData.value.pareto.total;
  }
  
  // 计算总缺陷数
  const total = paretoData.reduce((sum, item) => sum + item.value, 0)
  
  const ctx = periodParetoCanvas.value.getContext('2d')
  periodParetoChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: paretoData.map(item => item.name),
      datasets: [{
        label: '缺陷数',
        data: paretoData.map(item => item.value),
        backgroundColor: function(context) {
          // 重点缺陷（占比超25%）用红色标注
          const value = context.dataset.data[context.dataIndex]
          const percentage = (value / total) * 100
          return percentage > 25 ? 'rgba(255, 99, 132, 0.8)' : 'rgba(255, 99, 132, 0.4)'
        },
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        yAxisID: 'y'
      }, {
        label: '累计占比 (%)',
        data: paretoData.map(item => item.cumulative),
        type: 'line',
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        yAxisID: 'y1',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '缺陷数'
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: '累计占比 (%)'
          },
          min: 0,
          max: 100,
          grid: {
            drawOnChartArea: false
          },
          ticks: {
            callback: function(value) {
              return value + '%'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '缺陷类型（按占比降序）'
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: '帕累图（缺陷分布分析）'
        },
        legend: {
          position: 'top'
        },
        annotation: {
          annotations: {
            // 80%重点改善线
            eightyPercent: {
              type: 'line',
              yMin: 80,
              yMax: 80,
              borderColor: 'rgba(255, 159, 64, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                content: '重点改善线（80%）',
                enabled: true,
                position: 'end'
              },
              yAxisID: 'y1'
            }
          }
        },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              if (context.dataset.label === '缺陷数') {
                const value = context.parsed.y
                const percentage = ((value / total) * 100).toFixed(2)
                return [`占比: ${percentage}%`]
              }
              return []
            }
          }
        },
        onClick: function(event, elements) {
          if (elements.length > 0) {
            const index = elements[0].index
            const defect = periodData.value.pareto[index]
            const percentage = (defect.value / total * 100).toFixed(2)
            
            // 显示缺陷详情
            ElMessageBox.alert(`
              缺陷类型: ${defect.name}\n              缺陷数量: ${defect.value}\n              占比: ${percentage}%\n              累计占比: ${defect.cumulative}%\n              涉及班组: ${defect.teams.join(', ')}\n              涉及产线: ${defect.lines.join(', ')}\n              发生位置: ${defect.location}\n              严重程度: ${defect.severity}\n              处理建议: ${defect.suggestion}
            `, '缺陷详情', {
              confirmButtonText: '确定',
              type: 'info'
            })
          }
        }
      }
    }
  })
}

// FPY 班组对比
const initFPYComparison = () => {
  const ctx = fpyComparisonCanvas.value.getContext('2d')
  fpyComparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'], // 按周数据
      datasets: [
        {
          label: '甲班FPY(%)',
          data: [99.98, 99.97, 99.99, 99.98, 99.99, 99.97, 99.98],
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          order: 2
        },
        {
          label: '乙班FPY(%)',
          data: [99.95, 99.96, 99.97, 99.94, 99.96, 99.95, 99.97],
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          order: 2
        },
        {
          label: '丙班FPY(%)',
          data: [99.92, 99.93, 99.94, 99.91, 99.93, 99.92, 99.94],
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          order: 2
        },
        {
          label: '周平均FPY(%)',
          data: [99.95, 99.95, 99.97, 99.94, 99.96, 99.95, 99.96],
          type: 'line',
          borderColor: 'rgba(255, 159, 64, 1)',
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderWidth: 3,
          fill: true,
          tension: 0.1,
          order: 1,
          pointBackgroundColor: 'rgba(255, 159, 64, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          min: 99.85,
          max: 100,
          title: {
            display: true,
            text: 'FPY(%)'
          },
          ticks: {
            callback: function(value) {
              return value + '%'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: '日期'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'FPY 班组对比（按周）'
        },
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) {
                label += ': '
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y + '%'
              }
              return label
            }
          }
        }
      }
    }
  })
}

// Cpk 班组对比
const initCPKComparison = () => {
  const ctx = cpkComparisonCanvas.value.getContext('2d')
  cpkComparisonChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['尺寸控制', '表面质量', '涂层厚度', '刃口精度', '几何公差', '稳定性'],
      datasets: [
        {
          label: '甲班Cpk',
          data: [1.68, 1.65, 1.69, 1.67, 1.64, 1.66],
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(75, 192, 192, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        },
        {
          label: '乙班Cpk',
          data: [1.56, 1.54, 1.58, 1.55, 1.53, 1.57],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(54, 162, 235, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        },
        {
          label: '丙班Cpk',
          data: [1.52, 1.50, 1.54, 1.51, 1.49, 1.53],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(255, 99, 132, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        r: {
          beginAtZero: false,
          min: 1.3,
          max: 1.8,
          ticks: {
            stepSize: 0.1,
            callback: function(value) {
              return value
            }
          },
          pointLabels: {
            font: {
              size: 12
            }
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          angleLines: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          // 添加合格线和优秀线
          suggestedMin: 1.3,
          suggestedMax: 1.8
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Cpk 班组对比（多维度雷达图）'
        },
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) {
                label += ': '
              }
              if (context.parsed.r !== null) {
                label += context.parsed.r.toFixed(2)
              }
              return label
            }
          }
        },
        annotation: {
          annotations: {
            // 合格线（1.33）
            qualifiedLine: {
              type: 'line',
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              radius: '95%',
              label: {
                content: '合格线: 1.33',
                enabled: true,
                position: 'right'
              }
            },
            // 优秀线（1.67）
            excellentLine: {
              type: 'line',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              borderDash: [5, 5],
              radius: '105%',
              label: {
                content: '优秀线: 1.67',
                enabled: true,
                position: 'right'
              }
            }
          }
        }
      }
    }
  })
}

// 应用筛选
const applyFilters = () => {
  console.log('应用筛选条件', {
    product: selectedProduct.value,
    team: selectedTeam.value,
    line: selectedLine.value,
    equipment: selectedEquipment.value,
    dateRange: dateRange.value
  })
  // 实际项目中，这里可以调用API获取筛选后的数据
}

// 重置筛选
const resetFilters = () => {
  selectedProduct.value = ''
  selectedTeam.value = 'all'
  selectedLine.value = 'all'
  selectedEquipment.value = 'all'
  dateRange.value = []
  console.log('重置筛选条件')
  // 实际项目中，这里可以重新获取全部数据
}

// 导出报表
const exportReport = () => {
  alert('导出功能已触发')
  // 实际项目中，这里可以实现 Excel 或 PDF 导出逻辑
}

// 打印报表
const printReport = () => {
  window.print()
}

// 监听标签页切换
watch(activeTab, () => {
  // 销毁当前标签页的图表
  if (fpyChart) fpyChart.destroy()
  if (cpkChart) cpkChart.destroy()
  if (histogramChart) histogramChart.destroy()
  if (xmrChart) xmrChart.destroy()
  if (paretoChart) paretoChart.destroy()
  if (npControlChart) npControlChart.destroy()
  if (periodHistogramChart) periodHistogramChart.destroy()
  if (periodParetoChart) periodParetoChart.destroy()
  if (fpyComparisonChart) fpyComparisonChart.destroy()
  if (cpkComparisonChart) cpkComparisonChart.destroy()
  
  // 初始化新标签页的图表
  setTimeout(() => {
    initCharts()
  }, 100)
})

// 组件挂载时初始化图表
onMounted(() => {
  initCharts()
})
</script>

<style scoped>
.report-center-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-section {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.metrics-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.metric-card {
  height: 100%;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.metric-description {
  color: #666;
}

.highlight {
  color: #409eff;
  font-weight: bold;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 20px;
}

.chart-card {
  height: 100%;
}

.card-header {
  font-weight: bold;
}

.chart-canvas {
  height: 300px !important;
  width: 100% !important;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>