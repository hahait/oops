import request from '@/utils/request'

export function getZabbixValueForServer(params) {
  return request({
    url: '/monitor/',
    method: 'get',
    params: params
  })
}

export function getMonitorItemList(params) {
  return request({
    url: '/monitor/config/',
    method: 'get',
    params: params
  })
}

export function getMonitorItemObj(id) {
  return request({
    url: `/monitor/config/${id}`,
    method: 'get'
  })
}

export function addMonitorItem(data) {
  return request({
    url: '/monitor/config/',
    method: 'post',
    data
  })
}

export function editMonitorItem(id, data) {
  return request({
    url: `/monitor/config/${id}/`,
    method: 'put',
    data
  })
}

export function deleteMonitorItem(id) {
  return request({
    url: `/monitor/config/${id}/`,
    method: 'delete'
  })
}

export function getMonitorItemBindServerList(params) {
  return request({
    url: `/monitor/server/`,
    method: 'get',
    params: params
  })
}

export function getMonitorAlertList(params) {
  return request({
    url: '/monitor/alert/',
    method: 'get',
    params: params
  })
}

export function getMonitorAlertObj(id) {
  return request({
    url: `/monitor/alert/${id}`,
    method: 'get'
  })
}

export function editMonitorAlert(id, data) {
  return request({
    url: `/monitor/alert/${id}/`,
    method: 'put',
    data
  })
}

export function delMonitorAlert(id) {
  return request({
    url: `/monitor/alert/${id}/`,
    method: 'delete'
  })
}

export function getMonitorAlertStatistics(params) {
  return request({
    url: '/monitor/alert/statistics',
    method: 'get',
    params: params
  })
}

export function getMonitorRelateApps(params) {
  return request({
    url: '/monitor/relate/apps/',
    method: 'get',
    params: params
  })
}
