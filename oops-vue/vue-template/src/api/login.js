import request from '@/utils/request'

export function login(username, password) {
  return request({
    url: '/api-token-auth',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

