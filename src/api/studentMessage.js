import request from '@/utils/request'

export const postStudentOpinion = (paramsObj) => {
  return request({
    url: '/studentMessage/page',
    method: 'post',
    data: { ...paramsObj }
  })
}
