import request from '@/utils/request'

export const postSchoolOpinion = (paramsObj) => {
  return request({
    baseURL: 'http://localhost:5000',
    url: '/predict',
    method: 'post',
    data: { ...paramsObj }
  })
}
