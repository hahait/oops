import request from '@/utils/request'

export function getManufacturerObj(id) {
  return request({
    url: `/server/manufacturer/${id}`,
    method: 'get'
  })
}

export function getManufacturerList(params) {
  return request({
    url: '/server/manufacturer/',
    method: 'get',
    params: params
  })
}

