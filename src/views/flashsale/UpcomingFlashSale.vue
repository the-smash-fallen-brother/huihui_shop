<template>
  <div class="upcoming-flash-sale">
    <div class="page-header">
      <h1>即将开始</h1>
      <p class="subtitle">精彩秒杀，敬请期待</p>
    </div>

    <div v-loading="loading" class="upcoming-sale-grid">
      <el-empty v-if="!loading && upcomingGoods.length === 0" description="暂无即将开始的秒杀商品" />
      
      <div v-else class="goods-grid">
        <div 
          v-for="goods in upcomingGoods" 
          :key="goods.goods_id"
          class="upcoming-item"
          @click="goToDetail(goods.goods_id)"
        >
          <!-- 即将开始标签 -->
          <div class="upcoming-tag">即将开始</div>
          
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
            
            <!-- 价格信息 -->
            <div class="price-info">
              <span class="upcoming-price">¥{{ goods.flash_sale_price }}</span>
              <span class="original-price">¥{{ goods.market_price }}</span>
              <span class="discount-tag">省¥{{ calculateDiscount(goods) }}</span>
            </div>
            
            <!-- 库存信息 -->
            <div class="stock-info">
              <el-icon><Box /></el-icon>
              <span>限量 {{ goods.flash_sale_stock }} 件</span>
            </div>
            
            <!-- 开始时间 -->
            <div class="time-info">
              <el-icon><Timer /></el-icon>
              <span>开始时间：{{ formatTime(goods.flash_sale_start_time) }}</span>
            </div>
          </div>
          
          <!-- 提醒按钮 -->
          <el-button 
            :type="isReminderSet(goods.goods_id) ? 'success' : 'primary'"
            class="reminder-btn"
            @click.stop="toggleReminder(goods)"
          >
            {{ isReminderSet(goods.goods_id) ? '已设置提醒' : '设置提醒' }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 设置提醒对话框 -->
    <el-dialog v-model="reminderDialogVisible" title="设置秒杀提醒" width="400px">
      <div class="reminder-content">
        <p>秒杀开始前将通过站内消息提醒您</p>
        <div class="goods-summary">
          <img :src="selectedGoods?.goods_cover_img_file_url || selectedGoods?.goods_cover_img" />
          <div class="summary-info">
            <h4>{{ selectedGoods?.goods_name }}</h4>
            <p class="price">¥{{ selectedGoods?.flash_sale_price }}</p>
            <p class="time">{{ formatTime(selectedGoods?.flash_sale_start_time) }}</p>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="reminderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReminder">确认设置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Box, Timer } from '@element-plus/icons-vue';
import { getUpcomingFlashSaleList } from '@/api/flashsale';
import type { UpcomingFlashSale } from '@/types/flashsale';

const router = useRouter();
const loading = ref(false);
const upcomingGoods = ref<UpcomingFlashSale[]>([]);
const reminderDialogVisible = ref(false);
const selectedGoods = ref<UpcomingFlashSale | null>(null);
const reminderSet = ref<Set<number>>(new Set());

// 获取即将开始的秒杀商品列表
const fetchUpcomingGoods = async () => {
  try {
    loading.value = true;
    const response = await getUpcomingFlashSaleList();
    upcomingGoods.value = response.data.results;
  } catch (error) {
    console.error('获取即将开始的秒杀商品失败:', error);
    ElMessage.error('获取即将开始的秒杀商品失败');
  } finally {
    loading.value = false;
  }
};

// 获取商品图片URL
const getImageUrl = (goods: UpcomingFlashSale) => {
  return goods.goods_cover_img_file_url || goods.goods_cover_img || '/placeholder.jpg';
};

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  img.src = '/placeholder.jpg';
};

// 计算折扣金额
const calculateDiscount = (goods: UpcomingFlashSale) => {
  const marketPrice = parseFloat(goods.market_price);
  const flashPrice = parseFloat(goods.flash_sale_price);
  return (marketPrice - flashPrice).toFixed(2);
};

// 格式化时间
const formatTime = (time: string | undefined) => {
  if (!time) return '';
  return new Date(time).toLocaleString('zh-CN');
};

// 跳转到商品详情页
const goToDetail = (goodsId: number) => {
  router.push(`/flashsale/${goodsId}`);
};

// 检查是否已设置提醒
const isReminderSet = (goodsId: number) => {
  return reminderSet.value.has(goodsId);
};

// 切换提醒状态
const toggleReminder = (goods: UpcomingFlashSale) => {
  if (isReminderSet(goods.goods_id)) {
    // 取消提醒
    reminderSet.value.delete(goods.goods_id);
    ElMessage.success('已取消提醒');
  } else {
    // 显示设置提醒对话框
    selectedGoods.value = goods;
    reminderDialogVisible.value = true;
  }
};

// 确认设置提醒
const confirmReminder = () => {
  if (selectedGoods.value) {
    reminderSet.value.add(selectedGoods.value.goods_id);
    ElMessage.success('提醒设置成功！秒杀开始前将通过站内消息通知您');
  }
  reminderDialogVisible.value = false;
  selectedGoods.value = null;
};

// 从本地存储加载提醒设置
const loadReminderSettings = () => {
  const saved = localStorage.getItem('flashSaleReminders');
  if (saved) {
    reminderSet.value = new Set(JSON.parse(saved));
  }
};

// 保存提醒设置到本地存储
const saveReminderSettings = () => {
  localStorage.setItem('flashSaleReminders', JSON.stringify(Array.from(reminderSet.value)));
};

onMounted(() => {
  loadReminderSettings();
  fetchUpcomingGoods();
});

// 监听提醒设置变化，自动保存
const reminderSetProxy = new Proxy(reminderSet.value, {
  set(target, property, value, receiver) {
    const result = Reflect.set(target, property, value, receiver);
    saveReminderSettings();
    return result;
  }
});

// 替换原来的reminderSet
reminderSet.value = reminderSetProxy as Set<number>;
</script>

<style scoped>
.upcoming-flash-sale {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  color: #409eff;
  font-size: 32px;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-size: 16px;
}

.upcoming-sale-grid {
  min-height: 400px;
}

.goods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.upcoming-item {
  position: relative;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.upcoming-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.upcoming-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: linear-gradient(135deg, #409eff, #337ecc);
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

.upcoming-item:hover .goods-image img {
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.upcoming-price {
  color: #409eff;
  font-size: 20px;
  font-weight: bold;
}

.original-price {
  color: #999;
  font-size: 14px;
  text-decoration: line-through;
}

.discount-tag {
  background: #f0f9ff;
  color: #409eff;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.stock-info {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}

.stock-info .el-icon {
  margin-right: 5px;
  color: #409eff;
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
  color: #409eff;
}

.reminder-btn {
  width: 100%;
  height: 40px;
  border-radius: 0 0 8px 8px;
  border: none;
  background: #409eff;
}

.reminder-btn:hover {
  background: #337ecc;
}

.reminder-btn.el-button--success {
  background: #67c23a;
}

.reminder-btn.el-button--success:hover {
  background: #5daf34;
}

.reminder-content {
  text-align: center;
}

.goods-summary {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  text-align: left;
}

.goods-summary img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
}

.summary-info {
  flex: 1;
}

.summary-info h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.summary-info .price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.summary-info .time {
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .upcoming-flash-sale {
    padding: 10px;
  }
  
  .goods-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 10px;
  }
  
  .page-header h1 {
    font-size: 24px;
  }
  
  .upcoming-price {
    font-size: 16px;
  }
  
  .goods-image {
    height: 150px;
  }
}
</style>
