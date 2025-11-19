export interface FlashSaleGoods {
  goods_id: number;
  goods_name: string;
  goods_price: string;
  market_price: string;
  goods_cover_img: string;
  goods_cover_img_file: string | null;
  goods_cover_img_file_url: string | null;
  goods_carousel: string[];
  goods_carousel_files: any[];
  goods_sales: number;
  goods_status: number;
  category_name: string;
  create_time: string;
  is_flash_sale: boolean;
  flash_sale_price: string;
  flash_sale_stock: number;
  flash_sale_start_time: string;
  flash_sale_end_time: string;
}

export interface FlashSaleGoodsDetail extends FlashSaleGoods {
  cost_price: string;
  goods_desc: string;
  goods_stock: number;
  update_time: string;
  category: {
    category_id: number;
    category_name: string;
    parent: number | null;
    category_level: number;
    category_icon: string;
    sort_order: number;
    status: boolean;
  };
  specs: Array<{
    spec_id: number;
    spec_name: string;
    spec_value: string;
  }>;
  params: Array<{
    param_id: number;
    param_name: string;
    param_value: string;
  }>;
}

export interface FlashSaleListResponse {
  count: number;
  results: FlashSaleGoods[];
}

export interface UpcomingFlashSale {
  goods_id: number;
  goods_name: string;
  goods_price: string;
  market_price: string;
  goods_cover_img: string;
  goods_cover_img_file: string | null;
  goods_cover_img_file_url: string | null;
  goods_carousel: string[];
  goods_carousel_files: any[];
  goods_sales: number;
  goods_status: number;
  category_name: string;
  create_time: string;
  is_flash_sale: boolean;
  flash_sale_price: string;
  flash_sale_stock: number;
  flash_sale_start_time: string;
  flash_sale_end_time: string;
}

export interface UpcomingFlashSaleResponse {
  count: number;
  results: UpcomingFlashSale[];
}
