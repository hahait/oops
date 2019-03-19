import request from '@/utils/request'

export function getCabinetObj(id) {
  return request({
    url: `/cabinet/${id}`,
    method: 'get'
  })
}

export function addCabinet(data) {
  return request({
    url: '/cabinet/',
    method: 'post',
    data
  })
}

export function editCabinet(id, data) {
  return request({
    url: `/cabinet/${id}/`,
    method: 'put',
    data
  })
}

export function deleteCabinet(id) {
  return request({
    url: `/cabinet/${id}/`,
    method: 'delete'
  })
}
