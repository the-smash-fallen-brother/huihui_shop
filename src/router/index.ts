import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/flashsale',
    name: 'FlashSaleList',
    component: () => import('@/views/flashsale/FlashSaleList.vue'),
    meta: {
      title: '限时秒杀',
    },
  },
  {
    path: '/flashsale/:id',
    name: 'FlashSaleDetail',
    component: () => import('@/views/flashsale/FlashSaleDetail.vue'),
    meta: {
      title: '秒杀商品详情',
    },
  },
  {
    path: '/upcoming-flashsale',
    name: 'UpcomingFlashSale',
    component: () => import('@/views/flashsale/UpcomingFlashSale.vue'),
    meta: {
      title: '即将开始',
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta?.title) {
    document.title = `${to.meta.title} - 电商平台`;
  }
  next();
});

export default router;
