import request from '@/utils/request'

export function getTaskIntervalPeriodicList(params) {
  return request({
    url: '/task/interval/periodic/',
    method: 'get',
    params: params
  })
}

export function addTaskIntervalPeriodic(data) {
  return request({
    url: '/task/interval/periodic/',
    method: 'post',
    data
  })
}

export function editTaskIntervalPeriodic(id, data) {
  return request({
    url: `/task/interval/periodic/${id}/`,
    method: 'patch',
    data
  })
}

export function deleteTaskIntervalPeriodic(id) {
  return request({
    url: `/task/interval/periodic/${id}/`,
    method: 'delete'
  })
}

