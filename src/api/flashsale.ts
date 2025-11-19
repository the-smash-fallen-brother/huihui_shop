import request from '@/utils/request';
import type { FlashSaleListResponse, FlashSaleGoodsDetail, UpcomingFlashSaleResponse } from '@/types/flashsale';

/**
 * 获取正在进行的秒杀商品列表
 */
export function getFlashSaleGoodsList() {
  return request.get<FlashSaleListResponse>('/goods/flash-sale/');
}

/**
 * 获取秒杀商品详情
 * @param goods_id 商品ID
 */
export function getFlashSaleGoodsDetail(goods_id: number) {
  return request.get<FlashSaleGoodsDetail>(`/goods/flash-sale/${goods_id}/`);
}

/**
 * 获取即将开始的秒杀商品列表
 */
export function getUpcomingFlashSaleList() {
  return request.get<UpcomingFlashSaleResponse>('/goods/upcoming-flash-sale/');
}
