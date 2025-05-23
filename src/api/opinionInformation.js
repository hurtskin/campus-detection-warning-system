import request from '@/utils/request'

export const getOpinionInformation = (paramsObj) => {
  return request({
    url: '/opinionInformation/page',
    method: 'post',
    data: { ...paramsObj }
  })
}

export const addOpinionInformation = (paramsObj) => {
  return request({
    url: '/opinionInformation/add',
    method: 'post',
    data: { ...paramsObj }
  })
}

export const deleteOpinionInformation = (ids) => {
  return request({
    url: '/opinionInformation/delete',
    method: 'post',
    data: ids
  })
}
export const uploadText = (paramsObj) => {
  return request({
    baseURL: 'https://localhost:5000',
    url: '/predict',
    method: 'post',
    data: { ...paramsObj }
  })
}
