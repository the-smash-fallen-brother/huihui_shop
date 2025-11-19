<template>
  <div class="flash-sale-detail">
    <div v-loading="loading" class="detail-container">
      <el-empty v-if="!loading && !goodsDetail" description="商品不存在" />
      
      <div v-else-if="goodsDetail" class="goods-detail">
        <!-- 商品基本信息 -->
        <div class="goods-main">
          <!-- 商品图片轮播 -->
          <div class="goods-gallery">
            <el-carousel :autoplay="false" indicator-position="outside" height="400px">
              <el-carousel-item v-if="goodsDetail.goods_cover_img_file || goodsDetail.goods_cover_img">
                <img :src="getMainImageUrl()" :alt="goodsDetail.goods_name" />
              </el-carousel-item>
              <el-carousel-item 
                v-for="(image, index) in getCarouselImages()" 
                :key="index"
              >
                <img :src="image" :alt="`${goodsDetail.goods_name} ${index + 1}`" />
              </el-carousel-item>
            </el-carousel>
          </div>

        <!-- 商品信息 -->
        <div class="goods-info">
          <!-- 秒杀标签 -->
          <div class="flash-sale-header">
            <span class="flash-sale-badge">🔥 限时秒杀</span>
            <span class="time-info">
              <el-icon><Clock /></el-icon>
              距离结束还有：{{ getTimeRemaining() }}
            </span>
          </div>

          <h1 class="goods-name">{{ goodsDetail.goods_name }}</h1>

          <!-- 价格信息 -->
          <div class="price-section">
            <div class="flash-sale-price-info">
              <span class="price-label">秒杀价</span>
              <span class="flash-sale-price">¥{{ goodsDetail.flash_sale_price }}</span>
              <span class="savings">省¥{{ calculateDiscount() }}</span>
            </div>
            <div class="original-price-info">
              <span class="price-label">原价</span>
              <span class="original-price">¥{{ goodsDetail.market_price }}</span>
              <span class="discount-badge">{{ Math.round((1 - parseFloat(goodsDetail.flash_sale_price) / parseFloat(goodsDetail.market_price)) * 100) }}%OFF</span>
            </div>
          </div>

          <!-- 库存信息 -->
          <div class="stock-section">
            <div class="stock-info">
              <span class="stock-label">⚡ 秒杀库存</span>
              <span class="stock-count">仅剩 {{ goodsDetail.flash_sale_stock }} 件</span>
            </div>
            <el-progress 
              :percentage="getStockPercentage()" 
              :show-text="false"
              :stroke-width="10"
              color="#f56c6c"
            />
            <div class="stock-warning" v-if="goodsDetail.flash_sale_stock < 20">
              ⚠️ 库存紧张，即将售罄！
            </div>
          </div>

          <!-- 秒杀进度条 -->
          <div class="progress-section">
            <span class="progress-label">抢购进度</span>
            <el-progress 
              :percentage="getFlashSaleProgress()" 
              :color="getProgressColor()"
              :stroke-width="8"
            />
            <span class="progress-text">{{ getFlashSaleProgress() }}% 已抢购</span>
          </div>

          <!-- 销量信息 -->
          <div class="sales-info">
            <el-icon><ShoppingCart /></el-icon>
            <span>已售 {{ goodsDetail.goods_sales }} 件 | {{ goodsDetail.flash_sale_stock + goodsDetail.goods_sales }}人关注</span>
          </div>

          <!-- 分类信息 -->
          <div class="category-info">
            <el-icon><Folder /></el-icon>
            <span>{{ goodsDetail.category_name }}</span>
          </div>

          <!-- 秒杀规则 -->
          <div class="flash-rules">
            <h4>📋 秒杀规则</h4>
            <ul>
              <li>限时限量，每人限购1件</li>
              <li>秒杀商品不支持7天无理由退换</li>
              <li>请在{{ formatTime(goodsDetail.flash_sale_end_time) }}前完成支付</li>
              <li>库存有限，先到先得</li>
            </ul>
          </div>
        </div>
        </div>

        <!-- 详细信息标签页 -->
        <div class="goods-tabs">
          <el-tabs v-model="activeTab">
            <!-- 商品详情 -->
            <el-tab-pane label="商品详情" name="detail">
              <div class="goods-description">
                <div v-if="goodsDetail.goods_desc" v-html="goodsDetail.goods_desc"></div>
                <el-empty v-else description="暂无商品详情" />
              </div>
            </el-tab-pane>

            <!-- 商品规格 -->
            <el-tab-pane label="商品规格" name="specs">
              <div class="goods-specs">
                <div v-if="goodsDetail.specs && goodsDetail.specs.length > 0" class="specs-list">
                  <div v-for="spec in goodsDetail.specs" :key="spec.spec_id" class="spec-item">
                    <span class="spec-name">{{ spec.spec_name }}:</span>
                    <span class="spec-value">{{ spec.spec_value }}</span>
                  </div>
                </div>
                <el-empty v-else description="暂无商品规格" />
              </div>
            </el-tab-pane>

            <!-- 商品参数 -->
            <el-tab-pane label="商品参数" name="params">
              <div class="goods-params">
                <div v-if="goodsDetail.params && goodsDetail.params.length > 0" class="params-list">
                  <div v-for="param in goodsDetail.params" :key="param.param_id" class="param-item">
                    <span class="param-name">{{ param.param_name }}:</span>
                    <span class="param-value">{{ param.param_value }}</span>
                  </div>
                </div>
                <el-empty v-else description="暂无商品参数" />
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="large" @click="addToCart">
            <el-icon><ShoppingCart /></el-icon>
            加入购物车
          </el-button>
          <el-button type="danger" size="large" @click="buyNow">
            <el-icon><CreditCard /></el-icon>
            立即购买
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Clock, ShoppingCart, Folder, CreditCard } from '@element-plus/icons-vue';
import { getFlashSaleGoodsDetail } from '@/api/flashsale';
import type { FlashSaleGoodsDetail } from '@/types/flashsale';

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const goodsDetail = ref<FlashSaleGoodsDetail | null>(null);
const activeTab = ref('detail');

// 获取商品详情
const fetchGoodsDetail = async () => {
  try {
    loading.value = true;
    const goodsId = Number(route.params.id);
    const response = await getFlashSaleGoodsDetail(goodsId);
    goodsDetail.value = response.data;
  } catch (error) {
    console.error('获取商品详情失败:', error);
    ElMessage.error('获取商品详情失败');
  } finally {
    loading.value = false;
  }
};

// 获取主图URL
const getMainImageUrl = () => {
  if (!goodsDetail.value) return '';
  return goodsDetail.value.goods_cover_img_file_url || goodsDetail.value.goods_cover_img;
};

// 获取轮播图片
const getCarouselImages = () => {
  if (!goodsDetail.value) return [];
  return goodsDetail.value.goods_carousel.filter(img => img);
};

// 计算折扣金额
const calculateDiscount = () => {
  if (!goodsDetail.value) return '0.00';
  const marketPrice = parseFloat(goodsDetail.value.market_price);
  const flashPrice = parseFloat(goodsDetail.value.flash_sale_price);
  return (marketPrice - flashPrice).toFixed(2);
};

// 计算库存百分比
const getStockPercentage = () => {
  if (!goodsDetail.value) return 0;
  const totalStock = goodsDetail.value.goods_sales + goodsDetail.value.flash_sale_stock;
  return totalStock > 0 ? ((goodsDetail.value.flash_sale_stock / totalStock) * 100) : 0;
};

// 格式化时间
const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN');
};

// 加入购物车
const addToCart = () => {
  ElMessage.info('加入购物车功能开发中...');
};

// 立即购买
const buyNow = () => {
  ElMessage.info('立即购买功能开发中...');
};

onMounted(() => {
  fetchGoodsDetail();
});
</script>

<style scoped>
.flash-sale-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background: #f5f5f5;
  min-height: 100vh;
}

.detail-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.goods-detail {
  padding: 20px;
}

.goods-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.goods-gallery {
  border-radius: 8px;
  overflow: hidden;
}

.goods-gallery img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.goods-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.flash-sale-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #fff5f5, #fff0f0);
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ffeded;
}

.flash-sale-badge {
  background: linear-gradient(135deg, #ff6b6b, #ff4757);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
}

.time-info {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 14px;
}

.time-info .el-icon {
  margin-right: 5px;
  color: #f56c6c;
}

.goods-name {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
  margin: 0;
}

.price-section {
  background: #fafafa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.flash-sale-price-info {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 10px;
}

.flash-sale-price {
  font-size: 32px;
  font-weight: bold;
  color: #f56c6c;
}

.original-price-info {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.original-price {
  font-size: 18px;
  color: #999;
  text-decoration: line-through;
}

.discount {
  color: #67c23a;
  font-weight: bold;
  font-size: 16px;
}

.price-label {
  color: #666;
  font-size: 14px;
  min-width: 50px;
}

.stock-section {
  background: #fff5f5;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ffeded;
}

.stock-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.stock-label {
  color: #666;
  font-size: 14px;
}

.stock-count {
  color: #f56c6c;
  font-weight: bold;
}

.sales-info,
.category-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.goods-tabs {
  margin-bottom: 30px;
}

.goods-description,
.goods-specs,
.goods-params {
  padding: 20px;
  min-height: 200px;
}

.specs-list,
.params-list {
  display: grid;
  gap: 15px;
}

.spec-item,
.param-item {
  display: flex;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 6px;
  border-left: 3px solid #409eff;
}

.spec-name,
.param-name {
  font-weight: 500;
  color: #333;
  min-width: 100px;
}

.spec-value,
.param-value {
  color: #666;
  flex: 1;
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  padding: 20px;
  background: #f9f9f9;
  border-top: 1px solid #eee;
}

.action-buttons .el-button {
  min-width: 200px;
  height: 50px;
  font-size: 16px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .flash-sale-detail {
    padding: 10px;
  }
  
  .goods-main {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .goods-detail {
    padding: 15px;
  }
  
  .goods-name {
    font-size: 20px;
  }
  
  .flash-sale-price {
    font-size: 24px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .action-buttons .el-button {
    width: 100%;
    max-width: 300px;
  }
}
</style>
