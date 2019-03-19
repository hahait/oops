import request from '@/utils/request'

export function getDashboardCountStatistics(params) {
  return request({
    url: '/dashboard/count/statistics/',
    method: 'get',
    params: params
  })
}

export function getDashboardSevenDaysStatistics(params) {
  return request({
    url: '/dashboard/sevendays/statistics/',
    method: 'get',
    params: params
  })
}
