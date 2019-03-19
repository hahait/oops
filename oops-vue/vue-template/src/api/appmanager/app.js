import request from '@/utils/request'

export function getAppConfigList(params) {
  return request({
    url: '/appmanager/config/relate/',
    method: 'get',
    params: params
  })
}

export function addAppConfig(data) {
  return request({
    url: '/appmanager/config/relate/',
    method: 'post',
    data
  })
}

export function editAppConfig(id, data) {
  return request({
    url: `/appmanager/config/relate/${id}/`,
    method: 'patch',
    data
  })
}

export function deleteAppConfig(id) {
  return request({
    url: `/appmanager/config/relate/${id}/`,
    method: 'delete'
  })
}

export function getAppConfigSimpleList(params) {
  return request({
    url: '/appmanager/config/',
    method: 'get',
    params: params
  })
}
