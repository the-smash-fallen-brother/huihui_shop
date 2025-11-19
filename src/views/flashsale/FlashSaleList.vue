<template>
  <div class="flash-sale-list">
    <div class="page-header">
      <h1>限时秒杀</h1>
      <p class="subtitle">超值优惠，限时抢购</p>
    </div>

    <div v-loading="loading" class="flash-sale-grid">
      <el-empty v-if="!loading && flashSaleGoods.length === 0" description="暂无秒杀商品" />
      
      <div v-else class="goods-grid">
        <div 
          v-for="goods in flashSaleGoods" 
          :key="goods.goods_id"
          class="flash-sale-item"
          @click="goToDetail(goods.goods_id)"
        >
          <!-- 秒杀标签 -->
          <div class="flash-sale-tag">秒杀</div>
          
          <!-- 商品图片 -->
          <div class="goods-image">
            <img 
              :src="getImageUrl(goods)" 
              :alt="goods.goods_name"
              @error="handleImageError"
            />
          </div>
          
          <!-- 商品信息 -->
          <div class="goods-info">
            <h3 class="goods-name" :title="goods.goods_name">{{ goods.goods_name }}</h3>
            <div class="price-info">
              <span class="flash-sale-price">¥{{ goods.flash_sale_price }}</span>
              <span class="original-price">¥{{ goods.market_price }}</span>
            </div>
            
            <!-- 进度条 -->
            <div class="stock-info">
              <span class="stock-text">仅剩 {{ goods.flash_sale_stock }} 件</span>
              <el-progress 
                :percentage="getStockPercentage(goods)" 
                :show-text="false"
                :stroke-width="6"
                color="#f56c6c"
              />
            </div>
            
            <!-- 时间信息 -->
            <div class="time-info">
              <el-icon><Clock /></el-icon>
              <span>秒杀结束时间：{{ formatTime(goods.flash_sale_end_time) }}</span>
            </div>
          </div>
          
          <!-- 立即抢购按钮 -->
          <el-button 
            type="danger" 
            class="buy-btn"
            @click.stop="quickBuy(goods)"
          >
            立即抢购
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Clock } from '@element-plus/icons-vue';
import { getFlashSaleGoodsList } from '@/api/flashsale';
import type { FlashSaleGoods } from '@/types/flashsale';

const router = useRouter();
const loading = ref(false);
const flashSaleGoods = ref<FlashSaleGoods[]>([]);

// 获取秒杀商品列表
const fetchFlashSaleGoods = async () => {
  try {
    loading.value = true;
    const response = await getFlashSaleGoodsList();
    flashSaleGoods.value = response.data.results;
  } catch (error) {
    console.error('获取秒杀商品失败:', error);
    ElMessage.error('获取秒杀商品失败');
  } finally {
    loading.value = false;
  }
};

// 获取商品图片URL
const getImageUrl = (goods: FlashSaleGoods) => {
  return goods.goods_cover_img_file_url || goods.goods_cover_img || '/placeholder.jpg';
};

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  img.src = '/placeholder.jpg';
};

// 计算库存百分比
const getStockPercentage = (goods: FlashSaleGoods) => {
  // 这里假设总库存是原库存，可以根据实际情况调整
  const totalStock = parseInt(goods.goods_sales) + goods.flash_sale_stock;
  return totalStock > 0 ? ((goods.flash_sale_stock / totalStock) * 100) : 0;
};

// 格式化时间
const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN');
};

// 跳转到商品详情页
const goToDetail = (goodsId: number) => {
  router.push(`/flashsale/${goodsId}`);
};

// 快速购买
const quickBuy = (goods: FlashSaleGoods) => {
  // 这里可以实现快速购买逻辑，比如直接加入购物车并跳转到结算页
  ElMessage.info('快速购买功能开发中...');
};

onMounted(() => {
  fetchFlashSaleGoods();
});
</script>

<style scoped>
.flash-sale-list {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  color: #f56c6c;
  font-size: 32px;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-size: 16px;
}

.flash-sale-grid {
  min-height: 400px;
}

.goods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.flash-sale-item {
  position: relative;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.flash-sale-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.flash-sale-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: linear-gradient(135deg, #ff6b6b, #ff4757);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  z-index: 2;
}

.goods-image {
  height: 200px;
  overflow: hidden;
}

.goods-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.flash-sale-item:hover .goods-image img {
  transform: scale(1.1);
}

.goods-info {
  padding: 15px;
}

.goods-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
  line-height: 1.4;
  height: 44px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price-info {
  margin-bottom: 10px;
}

.flash-sale-price {
  color: #f56c6c;
  font-size: 24px;
  font-weight: bold;
  margin-right: 10px;
}

.original-price {
  color: #999;
  font-size: 14px;
  text-decoration: line-through;
}

.stock-info {
  margin-bottom: 10px;
}

.stock-text {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
  display: block;
}

.time-info {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #666;
  margin-bottom: 15px;
}

.time-info .el-icon {
  margin-right: 5px;
  color: #f56c6c;
}

.buy-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 0 0 8px 8px;
  border: none;
  background: linear-gradient(135deg, #ff6b6b, #ff4757);
}

.buy-btn:hover {
  background: linear-gradient(135deg, #ff5252, #ff3838);
}

@media (max-width: 768px) {
  .flash-sale-list {
    padding: 10px;
  }
  
  .goods-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 10px;
  }
  
  .page-header h1 {
    font-size: 24px;
  }
  
  .flash-sale-price {
    font-size: 18px;
  }
  
  .goods-image {
    height: 150px;
  }
}
</style>
