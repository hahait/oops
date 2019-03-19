import request from '@/utils/request'

export function getServerList(params) {
  return request({
    url: '/server/',
    method: 'get',
    params: params
  })
}

export function getServerForRelateList(params) {
  return request({
    url: '/server/relate/',
    method: 'get',
    params: params
  })
}

export function getServerObj(id) {
  return request({
    url: `/server/${id}`,
    method: 'get'
  })
}

export function addServer(data) {
  return request({
    url: '/server/',
    method: 'post',
    data
  })
}

export function editServer(id, data) {
  return request({
    url: `/server/${id}/`,
    method: 'put',
    data
  })
}

export function deleteServer(id) {
  return request({
    url: `/server/${id}/`,
    method: 'delete'
  })
}
