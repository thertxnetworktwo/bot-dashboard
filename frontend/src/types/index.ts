export enum ProductStatus {
  ACTIVE = 'Active',
  EXPIRED = 'Expired',
  EXPIRING_SOON = 'ExpiringSoon',
}

export interface Product {
  id: string
  name: string
  description?: string
  bot_username?: string
  website_link?: string
  contract_months: number
  contract_start_date: string
  contract_end_date: string
  is_renewed: boolean
  status: ProductStatus
  customer_telegram?: string
  customer_link?: string
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  name: string
  description?: string
  bot_username?: string
  website_link?: string
  contract_months: number
  contract_start_date?: string
  customer_telegram?: string
  customer_link?: string
}

export interface ProductUpdate {
  name?: string
  description?: string
  bot_username?: string
  website_link?: string
  contract_months?: number
  customer_telegram?: string
  customer_link?: string
  is_renewed?: boolean
}

export interface ProductListResponse {
  total: number
  page: number
  per_page: number
  products: Product[]
}

export interface DashboardStats {
  total_products: number
  active_products: number
  expired_products: number
  expiring_soon_7_days: number
  expiring_soon_30_days: number
}

export interface PhoneCheckResponse {
  exists: boolean
  phone_number: string
}

export interface PhoneRegisterResponse {
  success: boolean
  phone_number: string
  message?: string
}

export interface PhoneBulkRegisterResponse {
  success: boolean
  registered_count: number
  failed_count: number
  failed_numbers?: string[]
}

export interface PhoneCleanupResponse {
  success: boolean
  deleted_count: number
  message?: string
}
