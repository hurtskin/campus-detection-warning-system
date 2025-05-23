import request from '@/utils/request'

export const postRiskPerson = (paramsObj) => {
  return request({
    baseURL: 'https://localhost:5000',
    url: '/get_label',
    method: 'post',
    data: { ...paramsObj }
  })
}
