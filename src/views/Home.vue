<template>
  <div class="home">
    <div class="hero-section">
      <h1>电商平台</h1>
      <p>现代化的前后端分离电商系统</p>
    </div>

    <div class="navigation-section">
      <h2>功能模块</h2>
      <div class="nav-grid">
        <div class="nav-card" @click="goToFlashSale">
          <el-icon class="nav-icon"><Timer /></el-icon>
          <h3>限时秒杀</h3>
          <p>正在进行的秒杀商品</p>
        </div>
        
        <div class="nav-card" @click="goToUpcoming">
          <el-icon class="nav-icon"><Clock /></el-icon>
          <h3>即将开始</h3>
          <p>即将开始的秒杀活动</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { Timer, Clock } from '@element-plus/icons-vue';

const router = useRouter();

const goToFlashSale = () => {
  router.push('/flashsale');
};

const goToUpcoming = () => {
  router.push('/upcoming-flashsale');
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-section {
  text-align: center;
  padding: 80px 20px;
  color: white;
}

.hero-section h1 {
  font-size: 48px;
  margin-bottom: 20px;
  font-weight: 700;
}

.hero-section p {
  font-size: 20px;
  opacity: 0.9;
}

.navigation-section {
  background: white;
  border-radius: 20px 20px 0 0;
  padding: 60px 20px;
  min-height: 60vh;
}

.navigation-section h2 {
  text-align: center;
  font-size: 32px;
  margin-bottom: 40px;
  color: #333;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 800px;
  margin: 0 auto;
}

.nav-card {
  background: white;
  border: 2px solid #f0f0f0;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.nav-card:hover {
  border-color: #667eea;
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
}

.nav-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 20px;
}

.nav-card h3 {
  font-size: 24px;
  margin-bottom: 12px;
  color: #333;
}

.nav-card p {
  color: #666;
  font-size: 16px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 20px;
  }
  
  .hero-section h1 {
    font-size: 32px;
  }
  
  .hero-section p {
    font-size: 16px;
  }
  
  .navigation-section {
    padding: 40px 20px;
  }
  
  .navigation-section h2 {
    font-size: 24px;
  }
  
  .nav-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .nav-card {
    padding: 30px 20px;
  }
  
  .nav-icon {
    font-size: 36px;
  }
  
  .nav-card h3 {
    font-size: 20px;
  }
}
</style>
